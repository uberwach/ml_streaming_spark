#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from time import time
from time import sleep
import json

from kafka import KafkaProducer


def create_message():
    msg = {
        "time": int(time() * 1000.0),
        "msg": "Hello, World!"
    }

    return msg


if __name__ == "__main__":
    # one broker is enough
    KAFKA_SERVER = os.environ.get("KAFKA_SERVER", "localhost:9092")

    producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER,
                             value_serializer=lambda value: json.dumps(value).encode("utf-8"),
                             client_id="Simple Producer")

    while True:
        producer.send("test", create_message())
        sleep(0.5)
