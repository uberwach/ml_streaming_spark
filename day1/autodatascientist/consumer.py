#!/usr/bin env python
# -*- coding: utf-8 -*-
"""Simple Autodatascientist consumer"""

import os
import json

from kafka import KafkaConsumer
import numpy as np
KAFKA_SERVER = os.environ.get("KAFKA_SERVER", "localhost:9092")


def deserialize(encoded_msg):
    try:
        obj = json.loads(encoded_msg)
    except Exception as e:
        print(repr(e))
    else:
        return obj


consumer = KafkaConsumer(bootstrap_servers=KAFKA_SERVER,
                         client_id="Autodatascientist_consumer",
                         value_deserializer=deserialize,
                         group_id="autodata_consumer")

consumer.subscribe(["data-topic"])


for msg in consumer:
    value = msg.value

    rows = value["rows"]
    score = value["score"]

    n, m = len(rows), len(rows[0]["x"])

    X = np.empty((n, m), dtype=float)
    y = np.empty((n), dtype=int)

    for i in xrange(n):
        row = rows[i]
        X[i, :] = row["x"]
        y[i] = row["label"]

    print("X: %r\ny: %r" % (X, y))
