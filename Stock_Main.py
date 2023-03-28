from FinMind.data import DataLoader
from stock_list import stock_list

api = DataLoader()
api.login_by_token(api_token='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRlIjoiMjAyMy0wMy0yOCAyMjo0ODozNyIsInVzZXJfaWQiOiJoOTQ1ODAxNzIiLCJpcCI6IjE4MC4xNzcuMC4yMDEifQ.OEggToxfSdTQAT5Qmve6gR_NfTyH_-L8LssFKTIXO9Q')
api.login(user_id='h94580172',password='h94228200')

# 讀取數據
df = api.taiwan_stock_daily(start_date='2023-03-28')

# 選取指定日期和股票列表的數據
selected_df = df[(df['date'] == '2023-03-28') & (df['stock_id'].isin(stock_list))]

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
