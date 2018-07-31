#!/usr/bin env python
# -*- coding: utf-8 -*-

import json
import logging
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType
import pyspark.sql.functions as F

def decode(payload):
    try:
        decoded_msg = json.loads(payload.decode("utf-8"))
    except Exception as e:
        logging.warn("Error while decoding: %r", e)
    else:
        # change next line to work with struct type to return decoded_msg
        return decoded_msg["msg"]

# Instead of getting only the string "msg" you can read in both entries as two columsn
# {"msg": "Hello World", "time": 123452345}
# from pyspark.sql.types import StructType, StructField, IntegerType
# struct_type = StructType([StructField("msg", StringType()), StructField("time", IntegerType())])
# Or: StructType.add("msg", StringType()).add("time", LongType())
# and change decode function to return decoded_msg instead of decoded_msg["msg"]
decode_udf = F.udf(decode, StringType())


def normalize(string):
    return string.lower()

normalize_udf = F.udf(normalize, StringType())


if __name__ == "__main__":
    spark = SparkSession.builder.appName("Test Stream").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    ds = (spark.readStream
            .format("kafka")
            .option("kafka.bootstrap.servers", "localhost:9092")  # can add more to this list, seperate with ','
            .option("subscribe", "test")
            .load())

    decoded_ds = ds.select(decode_udf(F.col("value")).alias("content"))
    words = decoded_ds.withColumn("word", F.explode(F.split(F.col("content"), " ")))
    normalized_words = words.select(normalize_udf(F.col("word")).alias("word"))
    word_counts = normalized_words.groupBy("word").count()

    query = (word_counts.writeStream
             .outputMode("update")
             .format("console")
             .start())

    # to start stream
    query.awaitTermination()
