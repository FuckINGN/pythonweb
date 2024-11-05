import pandas as pd

# 1. 加载数据集
file_path = 'data/GlobalWeatherRepository.csv'
data = pd.read_csv(file_path)

# 2. 清理数据集
# 处理缺失值：这里选择删除缺失值的行，你也可以选择其他方法
data.dropna(inplace=True)

# 将列转换为适当的数据类型
data['temperature_celsius'] = data['temperature_celsius'].astype(float)
data['humidity'] = data['humidity'].astype(float)

# 3. 存储清理后的数据到新的CSV文件
cleaned_file_path = 'data/Cleaned_GlobalWeatherRepository.csv'
data.to_csv(cleaned_file_path, index=False)

# 4. 显示关键统计数据的摘要
summary = {
    '平均温度（Celsius）': data['temperature_celsius'].mean(),
    '最大温度（Celsius）': data['temperature_celsius'].max(),
    '最小温度（Celsius）': data['temperature_celsius'].min(),
    '平均湿度': data['humidity'].mean(),
    '最大湿度': data['humidity'].max(),
    '最小湿度': data['humidity'].min(),
}

# 输出摘要
print("关键统计数据摘要：")
for key, value in summary.items():
    print(f"{key}: {value}")
