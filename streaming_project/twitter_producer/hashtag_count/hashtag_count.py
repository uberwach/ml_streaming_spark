#!/usr/bin env python
# -*- coding: utf-8 -*-

import json
import logging
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, StructType, StructField
import pyspark.sql.functions as F

logger = logging.getLogger('pyspark')
logger.handlers = []


def decode(payload):
    try:
        decoded_msg = json.loads(payload.decode("utf-8"))
    except Exception as e:
        logging.warn("Error while decoding: %r", e)
    else:
        return decoded_msg

# can also be replaced by MapType or StructType.
# StructType.add("msg", StringType()).add("time", LongType())

msg_struct = StructType([StructField("msg", StringType(), True),
                         StructField("user", StringType(), True)])

decode_udf = F.udf(decode, msg_struct)

def normalize(string):
    return filter(lambda ch: ch.isalpha(), string.lower())

normalize_udf = F.udf(normalize, StringType())


if __name__ == "__main__":
    spark = SparkSession.builder.appName("Hashtag Stream").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    ds = (spark.readStream
            .format("kafka")
            .option("kafka.bootstrap.servers", "localhost:9092")  # can add more to this list, seperate with ','
            .option("subscribe", "tweets")
            .load())

    decoded_ds = ds.select(decode_udf(F.col("value")).alias("content"))
    words = decoded_ds.withColumn("word", F.explode(F.split(F.col("content.msg"), " "))).alias("word")
    words.printSchema()
    hashtags = words.filter((words["word"] != "") & (F.substring(words["word"], 0, 1) == '#'))
    hashtags.printSchema()
    hashtag_counts = hashtags.groupBy("word").count()

    query = (hashtag_counts.writeStream
             .outputMode("complete")
             .format("console")
             .start())

    # to start stream
    query.awaitTermination()
