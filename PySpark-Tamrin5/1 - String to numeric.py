from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler, StringIndexer, OneHotEncoder
from pyspark.ml.stat import Correlation
from pyspark.ml import Pipeline
import seaborn as sns
import matplotlib.pyplot as plt
from pyspark.sql.functions import *

spark = SparkSession.builder.appName("GolyStringToNumeric").getOrCreate()
df = spark.read.options(inferSchema='True',delimiter=',',header='True').csv("A:/hw_dataset.csv")


string_cols = [c for c, t in df.dtypes if t == "string"]
indexers = {c: StringIndexer(inputCol=c, outputCol=c+"_index") for c in string_cols}

indexed_df = df
for c, indexer in indexers.items():
    indexed_df = indexer.fit(indexed_df).transform(indexed_df)
print("Before:")
indexed_df.show(3)
numeric_cols = [c for c, t in indexed_df.dtypes if t in ["int", "double", "float", "long"]]
numeric_df = indexed_df.select(numeric_cols)
print("**********************************************************************************\nAfter:")

numeric_df.show(3)
numeric_df.coalesce(1).write.csv("hw_dataset_numeric.csv", header=True)
