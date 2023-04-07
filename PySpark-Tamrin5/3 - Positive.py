from pyspark.sql.functions import col, when
from pyspark.sql.types import *
from pyspark.sql import SparkSession
from pyspark.sql.functions import min


spark = SparkSession.builder.appName("GolyPositiveColumn").getOrCreate()
df = spark.read.options(inferSchema='True',delimiter=',',header='True').csv("A:/ML_hw_dataset_numeric.csv")

for x in df.columns:
    min_val = df.agg(min(col(x))).collect()[0][0]
    print(min_val)
    if min_val < 0:
        print("it is negative.")
        df = df.withColumn(x, col(x) + abs(min_val))
df.write.format("csv").option("header", "true").save("A:/ML_hw_dataset_numeric_positive.csv")
df.show()