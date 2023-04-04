import requests
import pandas as pd
from datetime import datetime
from List import holiday_dates, stock_list

# 定義假日列表
holidays = pd.to_datetime(holiday_dates)

# 設定 CustomBusinessDay 的規則，遇到假日就不扣除
custom_bday = pd.offsets.CustomBusinessDay(holidays=holidays)

# 獲取今天的日期
today = datetime.today()

# 設定要扣除的天數
days_to_subtract = 10

# 計算最近的工作日
start_date = pd.Timestamp(today) - custom_bday * days_to_subtract
last_workday = pd.Timestamp(today) - custom_bday
workdays = pd.date_range(start=start_date, end=last_workday, freq=custom_bday)

# 將日期轉換成指定的格式
workdays_str = [d.strftime('%Y-%m-%d') for d in workdays]

print(workdays_str)

def get_stock_data(date):
    url = "https://api.finmindtrade.com/api/v4/data"
    parameter = {
        "dataset": "TaiwanStockPriceAdj",
        "start_date": date,
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRlIjoiMjAyMy0wMy0yOCAyMjo0ODozNyIsInVzZXJfaWQiOiJoOTQ1ODAxNzIiLCJpcCI6IjE4MC4xNzcuMC4yMDEifQ.OEggToxfSdTQAT5Qmve6gR_NfTyH_-L8LssFKTIXO9Q",
    }
    resp = requests.get(url, params=parameter)
    data = resp.json()
    data = pd.DataFrame(data["data"])
    return data

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