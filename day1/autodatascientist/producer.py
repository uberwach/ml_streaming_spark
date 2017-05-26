#!/usr/bin env python
# -*- coding: utf-8 -*-
"""Simple Autodatascientist producer"""

import json
from time import sleep

from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression

from kafka import KafkaProducer


def serialize(msg):
    try:
        encoded_msg = json.dumps(msg)
    except Exception as e:
        print(repr(e))
    else:
        return encoded_msg

producer = KafkaProducer(bootstrap_servers="localhost:9092",
                         value_serializer=serialize)



"""
My strategy is the following:

In an infinite loop I generate a classification data set and fit a logistic regression on it.
The training accuracy is kept as a 'score'.

The data X, y is written in a row format. The resulting x vector is send as a list.
"""
while True:
    # Generate small data set to easily debug
    X, y = make_classification(n_samples=10, n_features=5, flip_y=0.1)

    lr = LogisticRegression()
    lr.fit(X, y)
    score = lr.score(X, y)

    rows = []

    for i, row in enumerate(X):
        data_point = {
            'x': row.tolist(),
            'label': int(y[i])
        }

        rows.append(data_point)

    msg = {
        "rows": rows,
        "score": score
    }

    producer.send("data-topic", msg)
    sleep(30)
