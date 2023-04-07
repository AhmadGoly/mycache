from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler, StringIndexer, OneHotEncoder
from pyspark.ml.stat import Correlation
from pyspark.ml import Pipeline
import seaborn as sns
import matplotlib.pyplot as plt
from pyspark.sql.functions import corr
from pyspark.sql.functions import *
import xlsxwriter

spark = SparkSession.builder.appName("GolyEDA").getOrCreate()

df = spark.read.options(inferSchema='True',delimiter=',',header='True').csv("A:/ML_hw_mydataset_numeric_positive.csv")

df.describe(df.columns[:5]).show()
df.describe(df.columns[5:10]).show()
df.describe(df.columns[10:15]).show()
df.describe(df.columns[15:20]).show()
df.describe(df.columns[20:25]).show()

#df.select(df.columns[:10]).summary("count", "mean", "stddev").show()
