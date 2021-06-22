from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.session import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.feature import StringIndexer
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml.regression import DecisionTreeRegressionModel, DecisionTreeRegressor
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.mllib.util import MLUtils

# instantiate spark environment
sc = SparkContext("local[*]", "Decision Tree Classifier")
spark = SparkSession(sc)
sc.setLogLevel('WARN')

# load the dataset
FULL = spark.read.csv("/Dataset/Dataset_FULL.csv", inferSchema=True) \
    .toDF("Team","Shots_goal", "Shots_off", "Total","Fouls","Corners","Ball_possesion","Yellow","Red","Total_Passes","Accurate","Passes%", "Result")
MINUS = spark.read.csv("/Dataset/Dataset_MINUS.csv", inferSchema=True) \
    .toDF("Team","Shots_goal", "Shots_off", "Total","Fouls","Corners","Ball_possesion","Yellow","Red","Total_Passes","Accurate","Passes%", "Result")

# Transformer — create a new “features” column that store all data features as an array
vector_assembler = VectorAssembler(inputCols=["Shots_goal", "Shots_off", "Total","Fouls","Corners","Ball_possesion","Yellow","Red","Total_Passes","Accurate","Passes%"],outputCol="features")

dfFULL = vector_assembler.transform(FULL) \
    .drop("Shots_goal", "Shots_off", "Total","Fouls","Corners","Ball_possesion","Yellow","Red","Total_Passes","Accurate","Passes%")
dfMINUS = vector_assembler.transform(MINUS) \
    .drop("Shots_goal", "Shots_off", "Total","Fouls","Corners","Ball_possesion","Yellow","Red","Total_Passes","Accurate","Passes%")

# train our model using training data
TreeClassRegressorFULL = DecisionTreeRegressor(labelCol="Result", featuresCol="features")
TreeClassRegressorMINUS = DecisionTreeRegressor(labelCol="Result", featuresCol="features")
TreeClassClassificationFULL = DecisionTreeClassifier(labelCol="Result", featuresCol="features")
TreeClassClassificationMINUS = DecisionTreeClassifier(labelCol="Result", featuresCol="features")

modelRegressorFull = TreeClassRegressorFULL.fit(dfFULL)
modelRegressorMINUS = TreeClassRegressorMINUS.fit(dfMINUS)
modelClassifierFull = TreeClassClassificationFULL.fit(dfFULL)
modelClassifierMINUS = TreeClassClassificationMINUS.fit(dfMINUS)


modelRegressorFull.save("/Trees/Regressor/TreeRegressorFULL")
modelRegressorMINUS.save("/Trees/Regressor/TreeRegressorMINUS")
modelClassifierFull.save("/Trees/Classifier/TreeClassifierFULL")
modelClassifierMINUS.save("/Trees/Classifier/TreeClassifierMINUS")
#predictions = modelR.transform(df_p)

#predictions.select("Team","features","prediction").show()
#sameModel = DecisionTreeModel.load(sc, "target/tmp/myDecisionTreeRegressionModel")
# test our model and make predictions using testing data
#predictions = model.transform(testing)
#predictions.select("prediction", "ResultIndex").show(20)

# Indici di valutazione del nostro algoritmo
""" evaluator = MulticlassClassificationEvaluator(labelCol="ResultIndex", predictionCol="prediction",metricName="accuracy")
accuracy = evaluator.evaluate(predictions)
print("Test Error = %g " % (1.0 - accuracy))
print("Accuracy = %g " % accuracy) """

