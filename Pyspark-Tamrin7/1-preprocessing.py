from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer
from pyspark.sql.functions import unix_timestamp, lit
from pyspark.ml.feature import VectorAssembler, StringIndexer, OneHotEncoder
from pyspark.ml.stat import Correlation
import seaborn as sns
import matplotlib.pyplot as plt
from pyspark.sql.functions import corr
from pyspark.sql.functions import *
import seaborn as sns
import matplotlib.pyplot as plt
from pyspark.ml.feature import PCA
from pyspark.ml.linalg import Vectors

spark = SparkSession.builder.appName("PreProcess").getOrCreate()
df = spark.read.options(inferSchema='True',header='True').csv("A:/uber-raw-data-aug14.csv")
df.show()
df.printSchema()

#Step 1:Date to seconds. starting from 8/1
start_time = "2014-08-01"
df = df.withColumn("Date/Time-seconds", unix_timestamp("Date/Time", "M/d/yyyy H:mm:ss") - 1406835000)
df=df.drop("Date/Time")
df.show()
df.printSchema()

#Step 2:Base to Numerical-Base.
indexer = StringIndexer(inputCol="Base", outputCol="Base-Numerical")
indexed_df = indexer.fit(df).transform(df)
indexed_df=indexed_df.drop("Base")
indexed_df.show()
indexed_df.printSchema()

#Step 3: Check Correlation and BoxPlot and Describe(min,max,mean,stddev):
#hame column ha ra be yek vector tabdil mikonim:
vector_col = "corr_features"
assembler = VectorAssembler(inputCols=indexed_df.columns, outputCol=vector_col)
df_vector = assembler.transform(indexed_df).select(vector_col)
#correlation:
matrix = Correlation.corr(df_vector, vector_col).collect()[0][0] 
corr_matrix = matrix.toArray().tolist() 
print(type(corr_matrix))
sns.heatmap(corr_matrix, cmap='coolwarm', annot=True)
plt.show()

pandas_df = indexed_df.toPandas()
sns.boxplot(data=pandas_df,y="Lat")
plt.show()
sns.boxplot(data=pandas_df,y="Lon")
plt.show()
sns.boxplot(data=pandas_df,y="Date/Time-seconds")
plt.show()
sns.boxplot(data=pandas_df,y="Base-Numerical")
plt.show()

indexed_df.describe().show()

#Step 4: save this new fresh data as csv for next steps:
indexed_df.coalesce(1).write.csv("A:/Preprocessed-Uber.csv", header=True, mode="overwrite")
