from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'global_weather',
    bootstrap_servers='localhost:9093',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='weather-consumer-group-2'
)

print("Starting to consume messages from Kafka...")
for message in consumer:
    print(f"Received message: {message.value}")
