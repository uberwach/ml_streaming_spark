# hard to find, because the output gives the wrong package:
# https://mvnrepository.com/artifact/org.apache.spark/spark-streaming-kafka-0-8_2.11/2.1.0
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.3.0 hashtag_count.py
