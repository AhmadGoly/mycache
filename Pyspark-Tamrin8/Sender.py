from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from kafka import KafkaProducer
import json
import csv
import time
from pyspark.ml.feature import VectorAssembler

scala_version = '2.12'
spark_version = '3.3.2'
packages = [
        f'org.apache.spark:spark-sql-kafka-0-10_{scala_version}:{spark_version}',
        'org.apache.kafka:kafka-clients:3.2.1'
    ]
spark = SparkSession.builder\
    .master("local")\
    .appName("KafkaSender")\
    .config("spark.jars.packages", ",".join(packages))\
    .getOrCreate()

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

df = spark.read.options(inferSchema='True',header='True').csv("A:/Preprocessed-Uber.csv")
train_data, test_data = df.randomSplit([0.8, 0.2], seed=40)


print(f"Kafka : Sending Test_data rows using Kafka Producer. total rows: {test_data.count()}.")
for row in test_data.toJSON().collect():
    producer.send("finaltopic", row.encode('utf-8'))
producer.close()
print("Kafka : Sending Test_data Complete.")
