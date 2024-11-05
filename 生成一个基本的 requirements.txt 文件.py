import os
import re
import pkg_resources


def get_imports_from_file(file_path):
    """从一个 Python 文件中提取出导入的库名"""
    imports = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.readlines()

        # 提取 import 语句
        for line in content:
            line = line.strip()
            # 匹配标准的 import 语句（包括 from ... import ...）
            if re.match(r'^\s*(import|from)\s+(\S+)', line):
                match = re.match(r'^\s*(import|from)\s+(\S+)', line)
                module_name = match.group(2).split('.')[0]  # 只取模块的顶层部分
                imports.add(module_name)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return imports


def generate_requirements(directory):
    """扫描指定目录，生成 requirements.txt 文件"""
    all_imports = set()

    # 遍历目录中的所有 Python 文件
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                imports = get_imports_from_file(file_path)
                all_imports.update(imports)

    # 使用 pkg_resources 来检查模块是否存在于 PyPI
    required_modules = []
    for module in all_imports:
        try:
            dist = pkg_resources.get_distribution(module)
            required_modules.append(f"{module}=={dist.version}")
        except pkg_resources.DistributionNotFound:
            required_modules.append(module)  # 如果找不到版本信息，只添加模块名

    # 写入 requirements.txt 文件
    requirements_file = os.path.join(directory, 'requirements.txt')
    with open(requirements_file, 'w', encoding='utf-8') as f:
        for module in sorted(required_modules):
            f.write(module + '\n')

    print(f"requirements.txt has been generated at {requirements_file}")


if __name__ == "__main__":
    directory = r"E:\code and money\11.4 flaskweb"  # 替换为你的目标路径
    generate_requirements(directory)
