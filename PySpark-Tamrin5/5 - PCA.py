from pyspark.sql.functions import col, when, min, max
from pyspark.sql.types import DoubleType
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler, StandardScaler,MinMaxScaler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.feature import PCA
from pyspark.ml.linalg import Vectors
from pyspark.sql.functions import array
from pyspark.sql.functions import concat

spark = SparkSession.builder.appName("GolyPCA").getOrCreate()
df = spark.read.options(inferSchema='True',delimiter=',',header='True').csv("A:/ML_hw_mydataset_numeric_positive.csv")

selected_cols = ["cons_price_idx", "nr_employed", "emp_var_rate","euribor3m"]
# in 4 sotun ro tabdil be vector mikonim (akhare tamrine 5 PCA roo hameye column ha anjam shode va k=9 hast.).
vector_col = "cacheForPCA"
assembler = VectorAssembler(inputCols=selected_cols, outputCol=vector_col)
df_vec = assembler.transform(df)

# Perform PCA on the vector column
pca = PCA(k=4, inputCol=vector_col, outputCol="pca_features")
model = pca.fit(df_vec)
transformed = model.transform(df_vec)

# 4 sotoone ghabli ro drop mikonim.
transformed = transformed.drop(*selected_cols)
transformed = transformed.drop("cacheForPCA")
# Showtime
transformed.show()

train, test = transformed.randomSplit([0.7, 0.3], seed=42)

print(transformed.columns[:-2]+transformed.columns[17:20])

assembler = VectorAssembler(inputCols=transformed.columns[:-2]+transformed.columns[17:20], outputCol='features')
train = assembler.transform(train)
test = assembler.transform(test)

lr = LogisticRegression(featuresCol='features', labelCol='y')
model = lr.fit(train)

predictions = model.transform(test)
evaluator = BinaryClassificationEvaluator(labelCol='y')
print('Test Area Under ROC:', evaluator.evaluate(predictions))
