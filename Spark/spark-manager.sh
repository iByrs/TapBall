#!/bin/bash
[[ -z "${SPARK_ACTION}" ]] && { echo "SPARK_ACTION required"; exit 1; }

# ACTIONS start-zk, start-kafka, create-topic, 

echo "Running action ${SPARK_ACTION}"
case ${SPARK_ACTION} in
"spark-submit-python")
 echo "Running package:${SPARK_PACK} and file: ${SPARK_FILE}" 
 ./bin/spark-submit --packages ${SPARK_PACK},${SPARK_ES} /code/${SPARK_FILE}
;;

esac
#         args: 
#            - kafka_structuredstream.py
#            - org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1