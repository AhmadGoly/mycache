from pyspark.sql import SparkSession
from pyspark.ml.clustering import KMeans
from pyspark.ml.feature import VectorAssembler
import matplotlib.pyplot as plt
from pyspark.ml.evaluation import ClusteringEvaluator
from pyspark.ml.clustering import KMeansModel

spark = SparkSession.builder.appName("AfterPreProcess").getOrCreate()
df = spark.read.options(inferSchema='True',header='True').csv("A:/Preprocessed-Uber.csv")
train_data, test_data = df.randomSplit([0.8, 0.2], seed=40)
assembler = VectorAssembler(inputCols=df.columns, outputCol="features")
train_data = assembler.transform(train_data)
test_data = assembler.transform(test_data)


k_values = range(2, 11)
wcss = []
for k in k_values:
    kmeans = KMeans(featuresCol='features', k=k)
    model = kmeans.fit(train_data)
    predictions = model.transform(test_data)
    evaluator = ClusteringEvaluator(featuresCol='features', predictionCol='prediction')
    silhouette_score = evaluator.evaluate(predictions, {evaluator.metricName: "silhouette"})
    wcss=model.summary.trainingCost
    print(f"running for k={k}")
    print(f"Silhouette score: {silhouette_score} and WCSS is {wcss}")


kmeans = KMeans(featuresCol="features", k=10)
model = kmeans.fit(train_data)
#predictions = model.transform(test_data)
#predictions.show()
model.save("A:/10-beans-model")
mymodel = KMeansModel.load("A:/10-beans-model")
