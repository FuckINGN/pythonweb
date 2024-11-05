import pandas as pd

# 定义数据文件路径
data_file_path = 'data/Cleaned_GlobalWeatherRepository.csv'  # 请确保路径正确

# 加载数据集
try:
    data = pd.read_csv(data_file_path)
    print("数据加载成功。\n")
except FileNotFoundError:
    print(f"错误：未找到文件 {data_file_path}")
    exit(1)
except Exception as e:
    print(f"加载数据时出错: {e}")
    exit(1)

# 打印列名
print("数据列名:")
print(data.columns.tolist())

# 打印数据结构
print("\n数据结构概览:")
print(data.info())

# 打印前几行数据
print("\n数据预览:")
print(data.head())
