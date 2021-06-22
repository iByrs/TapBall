from __future__ import print_function
from pyspark import SparkContext
from pyspark.sql import dataframe
from pyspark.sql.session import SparkSession
import pyspark.sql.functions as f
from pyspark.conf import SparkConf
from pyspark import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.sql.functions import from_json
from pyspark.streaming import StreamingContext
import pyspark.sql.types as tp
from pyspark.ml.feature import VectorAssembler
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame
from pyspark.ml.regression import DecisionTreeRegressionModel
from elasticsearch import Elasticsearch
from pyspark.ml.functions import vector_to_array
import os
import sys
import time



sc = SparkContext(appName="TapBall")
spark = SparkSession(sc)
sc.setLogLevel("WARN")
cong = SparkConf(loadDefaults=False)
# ES PARAMETERS
es_host = "10.0.100.30"
es_index = "tapball"
es_document = "_doc"
# KAFKA PARAMETERS
kafka_server = "kafkaServer:9092"
kafka_topic = "tapball"
# DECISION TREE
tree = DecisionTreeRegressionModel.load("/Trees/Regressor/TreeRegressorLESS")


#STRUCT OF KAFKA DATA
kafka_msg = tp.StructType([
    tp.StructField(name= '@version', dataType= tp.StringType(),  nullable= True),
    tp.StructField(name= '@timestamp', dataType= tp.StringType(),  nullable= True),
    tp.StructField(name= 'path',       dataType= tp.StringType(),  nullable= True),
    tp.StructField(name= 'message',       dataType= tp.StringType(),  nullable= True),
    tp.StructField(name= 'host',       dataType= tp.StringType(),  nullable= True),
])


def connectionToES():
    connected = False
    while not connected:
        try:
            es = Elasticsearch(hosts=es_host)
            print("Elasticsearch connection successful: host created.")
            connected = True
        except ConnectionError:
            print("Elasticsearch not available yet, trying again in 2s...")
            time.sleep(2)
    # API call
    conn = False
    while not conn:
        try:
            response = es.indices.create(index=es_index, ignore=400)
            print("Elasticsearch connection successful: index created.")
            conn = True
        except:
            print("Elasticsearch not available yet, trying again in 2s...")
            time.sleep(2)
    
    if 'acknowledged' in response:
        if response['acknowledged'] == True:
            print ("INDEX MAPPING SUCCESS FOR INDEX:", response['index'])



def getKafkaMessage(kafka_msg: DataFrame):
    if not kafka_msg.rdd.isEmpty():
        df2 = kafka_msg.withColumn('Features', f.split('data.message', ',')) \
                .withColumn('Team', f.col('Features').getItem(0)) \
                .withColumn('Shots_goal', f.col('Features').getItem(1).cast('integer'))\
                .withColumn('Shots_off', f.col('Features').getItem(2).cast('integer'))  \
                .withColumn('Total', f.col('Features').getItem(3).cast('integer'))  \
                .withColumn('Fouls', f.col('Features').getItem(4).cast('integer'))   \
                .withColumn('Corners', f.col('Features').getItem(5).cast('integer'))   \
                .withColumn('Ball_possession', f.col('Features').getItem(6).cast('integer'))   \
                .withColumn('Yellow', f.col('Features').getItem(7).cast('integer'))   \
                .withColumn('Red', f.col('Features').getItem(8).cast('integer'))   \
                .withColumn('Total_passes', f.col('Features').getItem(9).cast('integer'))   \
                .withColumn('Accurate', f.col('Features').getItem(10).cast('integer'))  \
                .withColumn('Passes%', f.col('Features').getItem(11).cast('integer'))
        # SPLIT AND THEN SELECT
        df = df2.select("Team","Shots_goal", "Shots_off", "Total","Fouls","Corners","Ball_possession","Yellow","Red","Total_Passes","Accurate","Passes%")
        return df

def vectorAssemblerOnDF(kafka_df: DataFrame):
    if not kafka_df.rdd.isEmpty():
        # ALL TOGETHER IN A SINGLER ARRAY
        vector_assembler = VectorAssembler(inputCols=["Shots_goal", "Shots_off", "Total","Fouls","Corners" \
            ,"Ball_possession","Yellow","Red","Total_Passes","Accurate","Passes%"] \
            ,outputCol="features")
        df_pred = vector_assembler.transform(kafka_df) \
                .drop("Shots_goal", "Shots_off", "Total","Fouls","Corners","Ball_possession","Yellow","Red","Total_Passes","Accurate","Passes%")
        return df_pred

def prediction(df: DataFrame):
    if not df.rdd.isEmpty():
        df_pred = tree.transform(df) 
        return df_pred

def DFintoArrray(df: DataFrame):
    if not df.rdd.isEmpty():
        # TRANSFORM INTO AN ARRAY
        df = df.withColumn('array', vector_to_array('features'))
        df = df.withColumn('Shots_goal', f.col('array').getItem(0)) \
                    .withColumn('Shots_off',f.col('array').getItem(1)) \
                    .withColumn('Total',f.col('array').getItem(2)) \
                    .withColumn('Fouls',f.col('array').getItem(3)) \
                    .withColumn('Corners',f.col('array').getItem(4)) \
                    .withColumn('Ball_possession',f.col('array').getItem(5)) \
                    .withColumn('Yellow',f.col('array').getItem(6)) \
                    .withColumn('Red',f.col('array').getItem(7)) \
                    .withColumn('Total_passes',f.col('array').getItem(8)) \
                    .withColumn('Accurate',f.col('array').getItem(9)) \
                    .withColumn('Passes%',f.col('array').getItem(10))
        df = df.drop('features','array')
    return df

def sendToElasticSearch(dfES: DataFrame):
    if not dfES.rdd.isEmpty():
        dfES.write \
                .format("org.elasticsearch.spark.sql") \
                .mode('append') \
                .option("es.mapping.id","Team") \
                .option("es.nodes", es_host).save(es_index)
        print("DF SENT TO ELASTICSEARCH!")
        dfES.show()

def work(kafka_msg: DataFrame, kafka_id: int):
    if not kafka_msg.rdd.isEmpty():
        df1 = getKafkaMessage(kafka_msg)
        df2 = vectorAssemblerOnDF(df1)
        df3 = prediction(df2)
        df4 = DFintoArrray(df3)
        sendToElasticSearch(df4)

def main():
    df = spark.readStream.format("kafka") \
        .option("kafka.bootstrap.servers", kafka_server) \
        .option("subscribe", kafka_topic) \
        .load()

    df.selectExpr("CAST(value AS STRING)") \
        .select(from_json("value", kafka_msg).alias("data")) \
        .writeStream \
        .foreachBatch(work) \
        .start() \
        .awaitTermination()

""" if __name__ == '__main__':
    main() """

main()
