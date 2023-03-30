import requests
import pandas as pd
from datetime import datetime, timedelta
from List import holiday_dates

# # 獲取今天的日期
today = datetime.today()
yesterday = today - timedelta(days=1)

# 計算起始日期
start_date = today - timedelta(days=2)

today = today.strftime('%Y-%m-%d')
start_date = start_date.strftime('%Y-%m-%d')

# 定義假日列表
holidays = pd.to_datetime(holiday_dates).tolist()

# 獲取最近30天的工作日
workdays = pd.bdate_range(start=start_date, end=yesterday, freq="C", holidays=holidays)

# 將日期轉換成指定的格式
workdays_str = [d.strftime('%Y-%m-%d') for d in workdays]

print(workdays_str)

def get_stock_data(date):
    url = "https://api.finmindtrade.com/api/v4/data"
    parameter = {
        "dataset": "TaiwanStockPriceAdj",
        "start_date": date,
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRlIjoiMjAyMy0wMy0yOCAyMjo0ODozNyIsInVzZXJfaWQiOiJoOTQ1ODAxNzIiLCJpcCI6IjE4MC4xNzcuMC4yMDEifQ.OEggToxfSdTQAT5Qmve6gR_NfTyH_-L8LssFKTIXO9Q", # 參考登入，獲取金鑰
    }
    resp = requests.get(url, params=parameter)
    data = resp.json()
    data = pd.DataFrame(data["data"])
    return data

from List import stock_list


# # 計算5日移動平均數
# stock['5ma'] = stock.groupby('stock_id')['close'].rolling(window=5).mean().reset_index(drop=True)



if __name__ == '__main__':
    with pd.ExcelWriter('stock_data.xlsx') as writer:
        for date in workdays_str:
            st = get_stock_data(date)
            # 選取股票列表的數據
            stock = st[st['stock_id'].isin(stock_list)]
            
            # 計算漲幅
            stock['percent_change'] = (stock['spread'] / stock['open']) * 100

            # 將漲幅保留兩位小數並四捨五入
            stock['percent_change'] = stock['percent_change'].apply(lambda x: round(x, 2))

            # 將Trading_Volume和Trading_money轉換為千位單位
            stock['Trading_Volume'] = stock['Trading_Volume'] / 1000
            stock['Trading_money'] = stock['Trading_money'] / 1000

            # 在列名中添加備註
            stock = stock.rename(columns={'Trading_Volume': 'Trading_Volume(k)', 'Trading_money': 'Trading_money(k)'})
            
            # 新增一個名為'Value'的欄位
            stock['Value'] = stock['percent_change'] / 10
            
            sheet_name = f"{date}"
            stock.to_excel(writer, sheet_name=sheet_name, index=False)