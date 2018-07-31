#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import logging
from time import sleep
from kafka import KafkaProducer
from twitter_profile import parse_profile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_list():
    with open("boehmermann_list.txt") as f:
        # remove the @
        account_names = [name[1:].strip() for name in f.readlines()]
        return account_names

    return []


def hash_tweet(tweet):
    return str(hash("%s||%s" % (tweet["user"], tweet["msg"])))


if __name__ == "__main__":
    # one broker is enough
    KAFKA_SERVER = os.environ.get("KAFKA_SERVER", "localhost:9092")

    producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER,
                             key_serializer=str.encode,
                             value_serializer=lambda value: json.dumps(value).encode("utf-8"),
                             client_id="Twitter Profile Reader")

    dissident_list = get_list()

    if dissident_list == []:
        logger.fatal("Dissident list is empty???")
        sys.exit()

    logger.info("%d dissidents" % len(dissident_list))
    while True:

        for profile_name in dissident_list:
            logger.info("Reading '%s'", profile_name)
            tweets = parse_profile(profile_name)
            logger.info("Found %d tweets", len(tweets))

            for tweet in tweets:
                logger.info(tweet)
                producer.send("tweets", key=hash_tweet(tweet), value=tweet)

            sleep(0.5)
