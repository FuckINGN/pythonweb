from kafka import KafkaConsumer
import pandas as pd
import json
import time

# 初始化 Kafka 消费者
try:
    consumer = KafkaConsumer(
        'global_weather',
        bootstrap_servers='localhost:9093',
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='weather-consumer-group'
    )
    print("Kafka consumer initialized successfully.")
except Exception as e:
    print(f"Error initializing Kafka consumer: {e}")
    exit(1)

# 记录接收到的数据
weather_data = []

# 开始消费数据
print("Starting to consume data from Kafka...")
start_time = time.time()
while time.time() - start_time < 60:  # 运行60秒
    for message in consumer:
        weather_data.append(message.value)
        print(f'Received: {message.value}')
        if time.time() - start_time >= 60:
            break

consumer.close()

# 将数据保存到 CSV 文件
df = pd.DataFrame(weather_data)
df.to_csv('weather_updates.csv', index=False)
print("Data saved to 'weather_updates.csv'.")

# 显示数据摘要
print("\nSummary of received data:")
print(df.describe())
