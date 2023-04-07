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

# Create a SparkSession
spark = SparkSession.builder.appName("CSV Normalization").getOrCreate()

# Read the CSV file
df = spark.read.options(inferSchema='True',delimiter=',',header='True').csv("A:/ML_hw_mydataset_numeric_positive.csv")

selected_cols = ["cons_price_idx", "nr_employed", "emp_var_rate","euribor3m"]
# Convert the selected columns to a single vector column
vector_col = "cacheForPCA"
assembler = VectorAssembler(inputCols=selected_cols, outputCol=vector_col)
df_vec = assembler.transform(df)

# Perform PCA on the vector column
pca = PCA(k=4, inputCol=vector_col, outputCol="pca_features")
model = pca.fit(df_vec)
transformed = model.transform(df_vec)

# Drop the old 4 columns from the transformed dataframe
transformed = transformed.drop(*selected_cols)
transformed = transformed.drop("cacheForPCA")
# Show the transformed dataframe
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
