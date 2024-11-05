import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 加载清理后的数据集
cleaned_file_path = 'data/Cleaned_GlobalWeatherRepository.csv'
data = pd.read_csv(cleaned_file_path)

# 打印列名以确认
print("数据集的列名：")
print(data.columns)

# 2. 生成全球最热和最冷的地点
hottest_locations = data.nlargest(5, 'temperature_celsius')[['location_name', 'temperature_celsius']]
coldest_locations = data.nsmallest(5, 'temperature_celsius')[['location_name', 'temperature_celsius']]

print("\n全球最热的5个地点：")
print(hottest_locations)
print("\n全球最冷的5个地点：")
print(coldest_locations)

# 3. 按地区计算统计数据
if 'country' in data.columns:  # 用国家列进行分组
    region_summary = data.groupby('country').agg({
        'temperature_celsius': ['mean', 'max', 'min'],
        'humidity': ['mean', 'max', 'min'],
        'precip_mm': ['mean', 'max', 'min']
    }).reset_index()
    print("\n按国家计算的摘要：")
    print(region_summary)

# 4. 数据可视化
data['last_updated'] = pd.to_datetime(data['last_updated'])
data['year'] = data['last_updated'].dt.year

# 设置字体以避免中文字符警告
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # 更改为支持中文的字体

# 可视化 1：温度的直方图
plt.figure(figsize=(10, 5))
sns.histplot(data['temperature_celsius'], bins=30, kde=True, color='blue')
plt.title('温度分布直方图')
plt.xlabel('温度 (°C)')
plt.ylabel('频数')
plt.axvline(data['temperature_celsius'].mean(), color='red', linestyle='--', label='平均温度')
plt.legend()
plt.show()

# 可视化 2：特定地区随时间变化的降水量
specific_region = 'Kuwait City'  # 使用真实的地区名称替换
region_data = data[data['location_name'] == specific_region]

if not region_data.empty:
    regional_precipitation = region_data.groupby('year')['precip_mm'].sum().reset_index()

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=regional_precipitation, x='year', y='precip_mm', marker='o', color='green')
    plt.title(f'{specific_region}地区随时间变化的降水量')
    plt.xlabel('年份')
    plt.ylabel('降水量 (mm)')
    plt.xticks(region_data['year'].unique())  # 显示所有年份
    plt.show()
else:
    print(f"指定地区 {specific_region} 的数据不可用")
