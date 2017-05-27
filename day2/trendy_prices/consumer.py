#!/usr/bin env python
# -*- coding: utf-8 -*-
import json
import logging

from pyspark.streaming.kafka import KafkaUtils
from pyspark import SparkContext
from pyspark.streaming import StreamingContext

from pyspark.mllib.linalg import Vectors
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.regression import StreamingLinearRegressionWithSGD

import numpy as np

NUM_FEATURES = 5

logger = logging.getLogger('pyspark')
logger.handlers = []


def extract_data_rows_from_json(data):
    # data is a (key, value) tuple, and because we have no key, the first entry is None.
    msg = json.loads(data[1].decode("utf-8"))
    rows = msg.get("rows", [])
    return rows


def transform_training_row_into_lp(row):
    features = Vectors.dense(row["x"])
    label = row["label"]
    return LabeledPoint(label, features)


def transform_test_row(row):
    return Vectors.dense(row["x"])




if __name__ == "__main__":
    # Create a local StreamingContext with two working thread
    # and batch interval of 1 second
    sc = SparkContext("local[2]", "Streaming Linear Regression")
    # 2nd argument is batch duration
    ssc = StreamingContext(sc, 5)

    directKafkaStream = KafkaUtils.createDirectStream(ssc,
                                                      ["trendy-topic"],
                                                      {"metadata.broker.list": "localhost:9092"})


    model = StreamingLinearRegressionWithSGD()
    model.setInitialWeights(np.random.rand(NUM_FEATURES))

    numStream = directKafkaStream.flatMap(extract_data_rows_from_json)

    trainingStream = numStream.filter(lambda row: row["known"]).map(transform_training_row_into_lp)
    testStream = numStream.filter(lambda row: not row["known"]).map(transform_test_row)

    model.trainOn(trainingStream)
    predictionStream = model.predictOn(testStream)
    # predictionStream.pprint()

    def printResults(rdd):
        predictions = rdd.collect()
        print("Predictions: %r" % predictions)
        print("Weights %r" % model._model.weights)

    predictionStream.foreachRDD(printResults)
    ssc.start()
    ssc.awaitTermination()
