from Stock_Login import df
from Stock_List import stock_list

# 選取股票列表的數據
selected_df = df[df['stock_id'].isin(stock_list)]

# 計算漲幅
selected_df['percent_change'] = (selected_df['spread'] / selected_df['open']) * 100

# 將漲幅保留兩位小數並四捨五入
selected_df['percent_change'] = selected_df['percent_change'].apply(lambda x: round(x, 2))

# 將Trading_Volume和Trading_money轉換為千位單位
selected_df['Trading_Volume'] = selected_df['Trading_Volume'] / 1000
selected_df['Trading_money'] = selected_df['Trading_money'] / 1000

# 在列名中添加備註
selected_df = selected_df.rename(columns={'Trading_Volume': 'Trading_Volume(k)', 'Trading_money': 'Trading_money(k)'})

# 新增一個名為'Value'的欄位
selected_df['Value'] = selected_df['percent_change'] / 10

# 保存結果到Excel
selected_df.to_excel('漲幅統計.xlsx', index=False)
