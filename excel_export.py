# excel_export.py

import pandas as pd

def export_excel(data, filename="process_card.xlsx"):
    """
    将数据导出为 Excel 工艺卡
    """
    # 这里先打印一下，模拟导出过程
    print(f"正在生成 Excel 文件: {filename} ...")
    
    # 模拟数据
    df = pd.DataFrame(data)
    
    # 模拟保存（实际项目中会用到 df.to_excel()）
    print("Excel 文件生成成功 (Mock)")
    
    return filename