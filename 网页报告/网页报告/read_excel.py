import pandas as pd

# 读取Excel文件
xlsx_file = "/workspace/user_input_files/竞品财务数据库_标准模板 (1).xlsx"

xl = pd.ExcelFile(xlsx_file)
print("Sheet names:", xl.sheet_names)
print()

# 读取每个sheet的结构
for sheet in xl.sheet_names:
    print(f"=== Sheet: {sheet} ===")
    df = pd.read_excel(xlsx_file, sheet_name=sheet, header=None)
    print(f"Shape: {df.shape}")
    print(df.head(20).to_string())
    print("\n" + "="*80 + "\n")