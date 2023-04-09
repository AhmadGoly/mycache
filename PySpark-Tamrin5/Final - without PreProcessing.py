from pyspark.sql.functions import col
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml import Pipeline
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Final - Without Preprocess").getOrCreate()
df = spark.read.options(inferSchema='True',delimiter=',',header='True').csv("A:/hw_dataset.csv")

#first and last step: make all of it in 2 columns: Features and label.
label_indexer = StringIndexer(inputCol="y", outputCol="label").fit(df)
numeric_cols = [col for col, dtype in df.dtypes if dtype in ['int', 'double']]
df_numeric = df.select(numeric_cols)
#assembler = VectorAssembler(inputCols=df.columns[:-1], outputCol="features")
assembler = VectorAssembler(inputCols=df_numeric.columns[:-1], outputCol="features")
preprocessed_df = assembler.transform(label_indexer.transform(df_numeric)).select("features", "label")
preprocessed_df.show()

#LR:
train, test = preprocessed_df.randomSplit([0.7, 0.3], seed=42)
lr = LogisticRegression(featuresCol="features", labelCol="label")
pipeline = Pipeline(stages=[lr])
model = pipeline.fit(train)
#Test:
evaluator = BinaryClassificationEvaluator(labelCol="label", rawPredictionCol="rawPrediction")
predictions = model.transform(test)
auc = evaluator.evaluate(predictions)
print('Test Area Under ROC:', auc)
