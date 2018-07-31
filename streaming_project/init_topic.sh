kafka-topics.sh --zookeeper localhost:2181 \
    --create --topic tweets \ 
    --replication-factor 1 \
    --partitions 3 \
    --config cleanup.policy=compact
