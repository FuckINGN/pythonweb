from kafka import KafkaProducer
import pandas as pd
import json
import time
import random

# 连接到 Kafka
try:
    producer = KafkaProducer(
        bootstrap_servers='localhost:9093',  # 确保端口正确
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    print("Producer connected successfully to Kafka.")
except Exception as e:
    print(f"Error connecting to Kafka: {e}")
    exit(1)

# 加载数据集
data_file_path = 'data/Cleaned_GlobalWeatherRepository.csv'  # 请更改为你的数据集路径
try:
    data = pd.read_csv(data_file_path)
    print("Data loaded successfully.")
except Exception as e:
    print(f"Error loading data file: {e}")
    exit(1)

# 将数据集转换为字典列表
locations = data.to_dict(orient='records')

# 发送天气更新
for i in range(60):  # 运行60秒，每秒发送一个更新
    location = random.choice(locations)  # 随机选择一个位置
    weather_update = {
        'location_name': location['location_name'],
        'temperature_celsius': location['temperature_celsius'] + random.uniform(-1, 1),  # 模拟温度变化
        'humidity': location['humidity'] + random.uniform(-5, 5),  # 模拟湿度变化
        'precip_mm': max(0, location['precip_mm'] + random.uniform(-1, 1))  # 模拟降水变化
    }
    try:
        producer.send('global_weather', value=weather_update)
        print(f"Sent: {weather_update}")
    except Exception as e:
        print(f"Failed to send message: {e}")
    time.sleep(1)  # 每秒发送一个更新

producer.close()
print("Producer closed.")
