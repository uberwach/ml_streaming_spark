# Streaming ML on Apache Spark

This repository covers the streaming analytics and machine learning in the [DSR](https://www.datascienceretreat.com) batch. DSR is a three month bootcamp that quickly trains experienced(!) professionals into freshly minted Data Scientists.

Over two days the topics covered are Apache Spark - in particular the *Spark Streaming* part and Apache Kafka.

As streaming use-cases are particularly involved in terms of architectures the slide presentation covers additional material on Big Data architectures.

Last, but not least, we discuss on how to do Machine Learning in the module.
## Changelog

```
Batch 11

- switched to Spark 2.2, finally structured streaming API is stable!
```

## Setup

The setup is particularly involved. The reason is that using the command line, Docker, and Apache Spark are seperate modules in DSR. Depending on the batch, they are sometimes not given, or in another form. We go through all.
### Terminal

We work with the command line. This is *de-facto* standard for Data Scientists. On MacOS you should install iTerm2, Linux has a standard installation, and Windows... You may want to google for `zsh`, the Z-shell.

### Anaconda 

Anaconda distribution installed, preferably with Python 3.5. If you have the Python 2 based distribution installed, you can create an environment as follows:

```
conda create -n YOUR_ENV_NAME python=3.5
source activate YOUR_ENV_NAME
```

Now you can try `pip freeze` to see that only a minimal set of packages is installed. As long as the environment is 

### PySpark 

Download `spark-2.2.0-bin-hadoop2.7.tgz` from the [Apache Spark homepage](https://spark.apache.org)

```
tar -xzf ~/Downloads/spark-2.2.0-bin-hadoop2.7.tgz
mv spark-2.2.0-bin-hadoop2.7 $HOME/spark
```

In order to run the Spark tools from the CLI, Spark must be added to the `$PATH`. Additionally, to `import pyspark` special Python libraries should be added to the `$PYTHONPATH`, so that everything works fine. Note that we run python programs directly, rather than going for Jupyter notebooks. Thus, possible settings from old modules must be removed.

My configuration looks as follow (in file `.bashrc` in the HOME folder)

```
export SPARK_HOME=$HOME/spark
export PATH="$PATH:$SPARK_HOME/bin" # adds spark-submit, spark-shell etc. to PATH

export PYTHONPATH=$SPARK_HOME/python:$PYTHONPATH
export PYTHONPATH=$SPARK_HOME/python/lib/py4j-0.10.4-src.zip:$PYTHONPATH

export PYSPARK_DRIVER_PYTHON=$(which python)
export PYSPARK_DRIVER_OPTS= # unsets if you have it set to notebook
export PYSPARK_PYTHON=$(which ipython)
```

### Kafka

Kafka is a distributed and fault-tolerant message queue. Kafka depends on Zookeeper for keeping its state. To keep things simple, we run a docker container with _both_ Kafka and Zookeeper. In practice, this is never done, as both services have different requirements. 

#### Manual Installation
It is wise, however, to install (get [this](https://www.apache.org/dyn/closer.cgi?path=/kafka/0.10.2.1/kafka_2.12-0.10.2.1.tgz)) Kafka separately as this provides the CLI tools.

Decompress the archive via `tar -xzf kafka_2.12-0.10.2.1.tgz` and set `KAFKA_HOME` to the target path. I extracted it to `~/Downloads/kafka_2.12-0.10.2.1` and write

```
export KAFKA_HOME="~/Downloads/kafka_2.12-0.10.2.1"
cd $KAFKA_HOME
```

#### Docker container
We use the docker container image `spotify/kafka`, use `docker pull spotify/kafka` once. Then to start a container,

```
docker run -p 2181:2181 -p 9092:9092 --env ADVERTISED_HOST=localhost --env ADVERTISED_PORT=9092 spotify/kafka
```

#### Manual commands
_Starting Zookeeper_

```
bash bin/zookeeper-server-start.sh config/zookeeper.properties
```

_Starting Kafka Broker_

```
bash bin/kafka-server-start.sh config/server.properties
```
_Console Consumer_

Useful to test a topic's contents.
```
kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --from-beginning or --offset <offset> \
  --topic test
```

_Producing messages in terminal_

_note that the test topics gets created automatically_
```
bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test
```

_Topics_
```
kafka-topics.sh \
  --zookeeper localhost:2181 \
  --create --topic test-topic \
  --partitions 2 \
  --replication-factor 1
  
kafka-topics.sh --zookeeper localhost:2181 --describe

kafka-topics.sh --zookeeper localhost:2181 --delete --topic test-topic
```

_Consumer Groups_
```
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list
```

_Cleaning up_

Stop the Kafka brokers, then Zookeeper. Under /tmp you can delete the kafka-logs and zookeeper, e.g.

```
rm -rf /tmp/zookeeper /tmp/kafka-logs
```
 
## Day 1
 
#### Overview
 
```
 └── day1 
    ├── autodatascientist
    │   ├── consumer.py
    │   ├── exercise.txt
    │   ├── producer.py
    │   └── requirements.txt
    ├── simple_consumer
    │   ├── Dockerfile
    │   ├── requirements.txt
    │   ├── run.sh
    │   └── simple_consumer.py
    ├── simple_producer
    │   ├── Dockerfile
    │   ├── requirements.txt
    │   ├── run.sh
    │   └── simple_producer.py
    └── simple_sparkstream
        ├── requirements.txt
        ├── run.sh
        └── simple_sparkstream.py
```
_simple\_consumer_: A simple Kafka consumer in Python, also as a microservice.

_simple\_producer_: A simple Kafka producer in Python, also as a microservice.

_simple\_sparkstream_: A minimal example to show-case how to use the traditional `DStream` API of Spark streaming.

_autodatascientist_: Additional "game" to show-case how to send matrix data over Kafka and process it.
