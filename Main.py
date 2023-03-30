import pandas as pd
from List import stock_list

# 读取 Excel 文件
df = pd.read_excel('stock_data.xlsx', sheet_name=None, index_col=0)

# 创建一个新 DataFrame，存储每个股票的 close 平均值
ma_df = pd.DataFrame(columns=['stock_id', 'close_mean'])

# 遍历每个股票
for stock_id in stock_list:
    # 过滤出该股票的数据
    stock_data = pd.DataFrame()
    for sheet_name in df.keys():
        if stock_id == df[sheet_name]['stock_id'].iloc[0]:
            stock_data = pd.concat([stock_data, df[sheet_name]])
            print(stock_data)
    if stock_data.empty:
        continue
    # 计算该股票的 close 平均值
    close_mean = stock_data['close'].mean()
    # 将结果添加到新 DataFrame
    ma_df = ma_df.append({'stock_id': stock_id, 'close_mean': close_mean}, ignore_index=True)

# 打印结果
print(ma_df)
