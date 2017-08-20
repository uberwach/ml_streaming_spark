#!/usr/bin env python
# -*- coding: utf-8 -*-

from pyspark.streaming.kafka import KafkaUtils
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from operator import add

import json

if __name__ == "__main__":
    # Create a local StreamingContext with two working thread
    # and batch interval of 1 second
    sc = SparkContext("local[1]", "Word Count")
    # 2nd argument is batch duration
    ssc = StreamingContext(sc, 10)

    directKafkaStream = KafkaUtils.createDirectStream(ssc,
                                                      ["test-topic"],
                                                      {"metadata.broker.list": "localhost:9092"})

    numStream = (directKafkaStream.map(lambda tup: json.loads(tup[1]).get("msg", ""))
                 .map(lambda msg: len(msg.split(" ")))
                 .reduce(add)
    )

    numStream.pprint()
    # print("Number of messages arrived: %s" % num_packets)
    ssc.start()
    ssc.awaitTermination()
