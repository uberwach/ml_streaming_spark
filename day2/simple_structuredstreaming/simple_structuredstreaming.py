#!/usr/bin env python
# -*- coding: utf-8 -*-

from pyspark.sql import SparkSession
from pyspark.sql.types import StringType
import pyspark.sql.functions as F
import json
import logging

def decode(payload):
    try:
        decoded_msg = json.loads(payload.decode("utf-8"))
    except Exception as e:
        logging.warn("Error while decoding: %r", e)
    else:
        return decoded_msg["msg"]

# can also be replaced by MapType or StructType.
decode_udf = F.udf(decode, StringType())

if __name__ == "__main__":
    spark = SparkSession.builder.appName("Test Stream").getOrCreate()

    ds = (spark.readStream
            .format("kafka")
            .option("kafka.bootstrap.servers", "localhost:9092")  # can add more to this list, seperate with ','
            .option("subscribe", "test")
            .load())

    decoded_ds = ds.select(decode_udf(F.col("value")).alias("content"))
    words = decoded_ds.withColumn("word", F.explode(F.split(F.col("content"), " ")))
    word_counts = words.groupBy("word").count()

    query = (word_counts.writeStream 
             .outputMode("complete")
             .format("console")
             .start())

    # to start stream
    query.awaitTermination()
