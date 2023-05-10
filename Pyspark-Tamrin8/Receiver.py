from kafka import KafkaConsumer
import json
from pyspark.ml.clustering import KMeansModel
from pyspark.sql import SparkSession
from pyspark.ml.clustering import KMeans
from pyspark.sql import Row
from pyspark.ml.feature import VectorAssembler
from pyspark.sql.types import *
import time
from pyspark.sql.functions import *
from pyspark.ml.linalg import VectorUDT
import uuid
from pyspark.sql.functions import udf

#Cassandra
#-------------------------------------------------------------------
from cassandra.cluster import Cluster
table_name="savedpredicts"
Key_name="goly"
cluster = Cluster(['localhost'])
session = cluster.connect()
print("Connected to Cassandra on localhost:9042 successfully.")
session.execute("CREATE KEYSPACE IF NOT EXISTS goly \
WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };")
session.set_keyspace(Key_name)
session.execute("CREATE TABLE IF NOT EXISTS savedpredicts (Lat DOUBLE,Lon DOUBLE,\
DateTimeSeconds BIGINT,BaseNumerical DOUBLE,prediction INT,id TEXT,PRIMARY KEY (id));")
#we generate random uuid ids for primary keys:
def generate_uuid():
    return str(uuid.uuid4())
uuid_udf = udf(generate_uuid)
#-------------------------------------------------------------------
scala_version = '2.12'
spark_version = '3.3.2'
spark = SparkSession.builder \
    .appName("MyApp") \
    .config("spark.jars.packages", "com.datastax.spark:spark-cassandra-connector_2.12:3.3.0") \
    .config("spark.sql.extensions", "com.datastax.spark.connector.CassandraSparkExtensions") \
    .config("spark.cassandra.connection.host", "127.0.0.1")\
    .getOrCreate()

schema = StructType([
    StructField('Lat', DoubleType(), True),
    StructField('Lon', DoubleType(), True),
    StructField('Date/Time-seconds', IntegerType(), True),
    StructField('Base-Numerical', DoubleType(), True)])

finalschema = StructType([
    StructField('Lat', DoubleType(), True),
    StructField('Lon', DoubleType(), True),
    StructField('Date/Time-seconds', IntegerType(), True),
    StructField('Base-Numerical', DoubleType(), True),
    StructField('features', VectorUDT(), True),
    StructField('prediction', IntegerType(), True)])
Final_df = spark.createDataFrame([], finalschema)
# Load the k-means model
#-------------------------------------------------------------------
model=KMeans.load('A:/10-beans-model')
#------------------------------------------------------------------
consumer = KafkaConsumer(
    'finaltopic',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my_group'
)
input_col_order = ["Lat","Lon","Date/Time-seconds","Base-Numerical"]

row_counter=0
def create_dataframe_and_predict(messages):
    global Final_df
    global row_counter
    global table_name
    global Key_name
    global uuid_udf
    string_list = []
    for x in messages[0]:
        message_str = x.value.decode('utf-8')
        string_list.append(message_str)
    print(f"Kafka : Received {len(string_list)} rows.")
    dict_list = [json.loads(s) for s in string_list]
    df = spark.createDataFrame(dict_list)
    assembler = VectorAssembler(inputCols=input_col_order, outputCol="features")
    df = assembler.transform(df)
    predictions = model.transform(df)
    cache_df=Final_df.union(predictions)
    Final_df=cache_df
    row_counter=row_counter+len(string_list)
    print(f"Model : Predicting {len(string_list)} rows complete. appended to Final_df. Total rows predicted: {row_counter}")

    #New: Cassandra
    predictions = predictions.withColumnRenamed('Lat', 'lat')\
    .withColumnRenamed('Lon', 'lon')\
    .withColumnRenamed('Date/Time-seconds', 'datetimeseconds')\
    .withColumnRenamed('Base-Numerical', 'basenumerical')\
    .select("lat", "lon", "datetimeseconds","basenumerical", "prediction").withColumn("id", uuid_udf())
    predictions.write.format("org.apache.spark.sql.cassandra").mode('append').options(table=table_name, keyspace=Key_name).save()
    print(f"Cassandra : Saved {len(string_list)} rows on my_predicts_table in Cassandra.")


print("Kafka is ready to get rows.")
start_time = time.time()
#unsaved=False
while True:
    messages = [msg for msg in consumer.poll(max_records=5000).values()]
    if messages:
        time.sleep(0.01)
        #start_time = time.time()
        #unsaved=True
        create_dataframe_and_predict(messages)
    #Don't need to save on pc anymore. we'are saving it in cassandra.
    #if unsaved:
    #    if (time.time() - start_time)>10:
    #        print(f"Kafka : got nothing for 10 secs. Saving predicts in System.\nKafka : Total Predicts: {Final_df.count()} saved in path A:/Uber-Predicts.")
    #        time.sleep(0.01)
    #        Final_df.select("Lat", "Lon", "Date/Time-seconds","Base-Numerical", "prediction").coalesce(1).write.mode("overwrite").csv("A:/Uber-Predicts")
    #        unsaved=False


