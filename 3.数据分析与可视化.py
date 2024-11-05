import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 加载清理后的数据集
cleaned_file_path = 'data/Cleaned_GlobalWeatherRepository.csv'
data = pd.read_csv(cleaned_file_path)

# 2. 生成全球最热和最冷的5个地点
hottest_locations = data.nlargest(5, 'temperature_celsius')[['location_name', 'temperature_celsius']]
coldest_locations = data.nsmallest(5, 'temperature_celsius')[['location_name', 'temperature_celsius']]

print("全球最热的5个地点：")
print(hottest_locations)
print("\n全球最冷的5个地点：")
print(coldest_locations)

# 3. 按地区计算平均温度、湿度和降水量
# 这里假设有一个列 'region' 用于存储地区信息，您可以根据实际情况修改
if 'region' in data.columns:
    region_summary = data.groupby('region').agg({
        'temperature_celsius': ['mean', 'max', 'min'],
        'humidity': ['mean', 'max', 'min'],
        'precip_mm': ['mean', 'max', 'min']
    }).reset_index()
    print("\n按地区计算的摘要：")
    print(region_summary)

# 4. 绘制可视化图
# 设置可视化风格
sns.set(style='whitegrid')

# 绘制温度的直方图
plt.figure(figsize=(10, 5))
sns.histplot(data['temperature_celsius'], bins=30, kde=True)
plt.title('温度分布直方图')
plt.xlabel('温度 (°C)')
plt.ylabel('频数')
plt.show()

# 绘制特定地区随时间变化的降水量（假设有 'last_updated' 列，您可以根据实际情况修改）
data['last_updated'] = pd.to_datetime(data['last_updated'])
data['year'] = data['last_updated'].dt.year

# 假设有一个列 'specific_region' 代表特定地区
if 'specific_region' in data.columns:
    regional_precipitation = data.groupby(['year', 'specific_region'])['precip_mm'].sum().reset_index()

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=regional_precipitation, x='year', y='precip_mm', hue='specific_region', marker='o')
    plt.title('特定地区随时间变化的降水量')
    plt.xlabel('年份')
    plt.ylabel('降水量 (mm)')
    plt.legend(title='地区')
    plt.show()
