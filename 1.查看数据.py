import pandas as pd

# 定义文件路径
file_path = 'data/GlobalWeatherRepository.csv'

# 读取CSV文件
data = pd.read_csv(file_path)

# 显示数据结构
print("列名：")
print(data.columns.tolist())
print("\n前五行数据：")
print(data.head())
