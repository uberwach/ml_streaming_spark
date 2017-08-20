#!/usr/bin env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
from time import time
import logging
import json

from kafka import KafkaConsumer

logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO)


def get_time_ms():
    return int(time() * 1000.0)


def deserialize(msg):
    try:
        decoded_msg = json.loads(msg.decode("utf-8"))
    except Exception as e:
        logging.warn("Error while decoding: %r", e)
    else:
        return decoded_msg

if __name__ == "__main__":
    KAFKA_SERVER = os.environ.get("KAFKA_SERVER", "localhost:9092")
    CONSUME_TOPICS = os.environ.get("CONSUME_TOPICS", "test-topic").split(",")

    consumer = KafkaConsumer(bootstrap_servers="localhost:9092",
                             client_id="Simple Consumer",
                             group_id="Simple",  # consumer group
                             value_deserializer=deserialize,
                             auto_offset_reset='earliest')

    consumer.subscribe(CONSUME_TOPICS)

    for msg in consumer:
        print(msg.value)
