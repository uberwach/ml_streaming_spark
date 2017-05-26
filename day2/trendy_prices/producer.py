#!/usr/bin env python
# -*- coding: utf-8 -*-
"""Trendy producer"""

import json
from time import sleep
from time import time

import numpy as np
from scipy import rand
from kafka import KafkaProducer

TIME_BATCHES = 5  # Time in seconds to send a batch
N_BATCH_SIZE = 10  # number of data points per batch
N_FEATURES = 5  # number of features
CHANGE_PER_SECOND = 0.01
LABEL_KNOWN = 0.5  # Probability that the label is known
TIME_STARTED = int(time() * 1000)
WEIGHTS = np.random.random(N_FEATURES) - 0.5


def serialize(msg):
    try:
        encoded_msg = json.dumps(msg)
    except Exception as e:
        print(repr(e))
    else:
        return encoded_msg

producer = KafkaProducer(bootstrap_servers="localhost:9092",
                         value_serializer=serialize)


def current_weight():
    return (((time()*1000 - TIME_STARTED) / 1000.0) + 1) * WEIGHTS * CHANGE_PER_SECOND


def generate_label(x, with_noise):
    w = current_weight()

    if with_noise:
        # FIXME: should be selected from normal distribution centered at 0 and variance of 1
        eps = rand(0, 1)
        return np.dot(w, x) + eps
    else:
        return np.dot(w, x)

if __name__ == "__main__":

    j = 1
    while True:
        X = np.random.random((N_BATCH_SIZE, N_FEATURES))
        rows = []

        for i, row in enumerate(X):
            known = True if np.random.random() >= LABEL_KNOWN else False

            data_point = {
                'x': row.tolist(),
                'label': str(generate_label(row, not known)),
                'known': known
            }

            rows.append(data_point)

        msg = {
            "rows": rows,
        }
        print("Batch %d, send with weight %r" % (j, current_weight()))
        j += 1

        producer.send("trendy-topic", msg)
        sleep(TIME_BATCHES)
