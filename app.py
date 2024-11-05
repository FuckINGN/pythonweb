from flask import Flask, jsonify, request
from kafka import KafkaConsumer
import pandas as pd
import json

app = Flask(__name__)

# 加载清洁的全球天气数据
cleaned_data = pd.read_csv('data/Cleaned_GlobalWeatherRepository.csv')  # 请将路径替换为你的数据集路径

# 路由 1: 获取清洁的天气数据
@app.route('/api/weather_data', methods=['GET'])
def get_weather_data():
    # 获取请求参数
    country = request.args.get('country')
    location_name = request.args.get('location_name')
    filtered_data = cleaned_data

    # 根据请求过滤数据
    if country:
        filtered_data = filtered_data[filtered_data['country'] == country]
    if location_name:
        filtered_data = filtered_data[filtered_data['location_name'] == location_name]

    return jsonify(filtered_data.to_dict(orient='records'))

# 路由 2: 获取实时天气更新
@app.route('/api/live_weather', methods=['GET'])
def get_live_weather():
    consumer = KafkaConsumer(
        'global_weather',
        bootstrap_servers='localhost:9093',
        auto_offset_reset='latest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    updates = []
    for message in consumer:
        updates.append(message.value)
        if len(updates) >= 10:  # 获取最新的10条更新
            break

    consumer.close()
    return jsonify(updates)

if __name__ == '__main__':
    app.run(debug=True)
