import pandas as pd
from Data import workdays_str

# 讀取 Excel 檔案
excel_file = pd.ExcelFile('stock_data.xlsx')

# 計算每個 stock_id 在不同日期的 close 價格加總
stock_data = {}
for sheet_name in excel_file.sheet_names:
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    for stock_id in df['stock_id'].unique():
        if stock_id not in stock_data:
            stock_data[stock_id] = {}
        stock_data[stock_id][sheet_name] = df[df['stock_id']==stock_id]['close'].sum()

# 將 stock_data 轉換成 DataFrame 格式
stock_temp_data = pd.DataFrame(stock_data)

# 設定 DataFrame 的 index 為 workdays_str
stock_temp_data.index = workdays_str

# 將 DataFrame 轉置，並新增 SUM 行
stock_temp_data = stock_temp_data.T
stock_temp_data['SUM'] = stock_temp_data.sum(axis=1) #修正此處

# # 新增一列，名稱為 'SUM'，數值為每一列的加總
# stock_temp_data.loc['SUM'] = stock_temp_data.sum()

# 將 DataFrame 輸出成 Excel 檔案
stock_temp_data.to_excel('stock_temp.xlsx')
