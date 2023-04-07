from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler, StringIndexer, OneHotEncoder
from pyspark.ml.stat import Correlation
from pyspark.ml import Pipeline
import seaborn as sns
import matplotlib.pyplot as plt
from pyspark.sql.functions import corr
from pyspark.sql.functions import *
import xlsxwriter

spark = SparkSession.builder.appName("GolyCorrelation").getOrCreate()
df = spark.read.options(inferSchema='True',delimiter=',',header='True').csv("A:/ML_hw_dataset_numeric.csv")

#hame column ha ra be yek vector tabdil mikonim:
vector_col = "corr_features"
assembler = VectorAssembler(inputCols=df.columns, outputCol=vector_col)
df_vector = assembler.transform(df).select(vector_col)

#correlation:
matrix = Correlation.corr(df_vector, vector_col).collect()[0][0] 
corr_matrix = matrix.toArray().tolist() 
print(type(corr_matrix))

#save as xls:
with xlsxwriter.Workbook('correlation.xlsx') as workbook:
    worksheet = workbook.add_worksheet()

    for row_num, data in enumerate(corr_matrix):
        worksheet.write_row(row_num, 0, data)

#show:
sns.heatmap(corr_matrix, cmap='coolwarm', annot=True)
plt.show()
