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


scala_version = '2.12'
spark_version = '3.3.2'
packages = [
        f'org.apache.spark:spark-sql-kafka-0-10_{scala_version}:{spark_version}',
        'org.apache.kafka:kafka-clients:3.2.1']
spark = SparkSession.builder\
    .master("local")\
    .appName("KafkaReceiver")\
    .config("spark.jars.packages", ",".join(packages))\
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
model = KMeansModel.load("A:/10-beans-model")
#------------------------------------------------------------------

consumer = KafkaConsumer(
    'sodfkaofasmoas',
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

print("Kafka is ready to get rows.")
start_time = time.time()
unsaved=False
while True:
    messages = [msg for msg in consumer.poll(max_records=5000).values()]
    if messages:
        time.sleep(0.01)
        start_time = time.time()
        unsaved=True
        create_dataframe_and_predict(messages)
    if unsaved:
        if (time.time() - start_time)>10:
            print(f"Kafka : got nothing for 10 secs. Saving predicts in System.\nKafka : Total Predicts: {Final_df.count()} saved in path A:/Uber-Predicts.")
            time.sleep(0.01)
            Final_df.select("Lat", "Lon", "Date/Time-seconds","Base-Numerical", "prediction").coalesce(1).write.mode("overwrite").csv("A:/Uber-Predicts")
            unsaved=False


