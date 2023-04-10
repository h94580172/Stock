import requests
import pandas as pd
from datetime import datetime
from List import holiday_dates, stock_list

class Common:
    def get_workdays(self, days_to_subtract):
        # 定義假日列表
        holidays = pd.to_datetime(holiday_dates)

        # 設定 CustomBusinessDay 的規則，遇到假日就不扣除
        custom_bday = pd.offsets.CustomBusinessDay(holidays=holidays)

        # 獲取今天的日期
        today = datetime.today()

        # 計算最近的工作日
        start_date = pd.Timestamp(today) - custom_bday * days_to_subtract
        last_workday = pd.Timestamp(today) - custom_bday
        workdays = pd.date_range(start=start_date, end=last_workday, freq=custom_bday)

        # 將日期轉換成指定的格式
        workdays_str = [d.strftime('%Y-%m-%d') for d in workdays]
        return workdays_str

    def calculate_value(self, stock_sorted):
        """
        Calculates the value of each stock based on its trading volume and percent change.
        """
        value_list = [1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
        for i in range(len(stock_sorted)):
            if i < 100:
                stock_sorted.loc[stock_sorted.index[i], 'value'] = value_list[i//10] * 0.7
            else:
                stock_sorted.loc[stock_sorted.index[i], 'value'] = -0.1    
        return stock_sorted

class StockBuySellProcessor(Common):
    def __init__(self):
        self.url = "https://api.finmindtrade.com/api/v4/data"
        self.parameter = {
            "dataset": "TaiwanStockInstitutionalInvestorsBuySell",
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRlIjoiMjAyMy0wMy0yOCAyMjo0ODozNyIsInVzZXJfaWQiOiJoOTQ1ODAxNzIiLCJpcCI6IjE4MC4xNzcuMC4yMDEifQ.OEggToxfSdTQAT5Qmve6gR_NfTyH_-L8LssFKTIXO9Q",
        }

    def get_buy_sell_data(self, date):
        self.parameter["start_date"] = date
        resp = requests.get(self.url, params=self.parameter)
        data = resp.json()
        data = pd.DataFrame(data["data"])

        # select data for Investment_Trust and Foreign_Investor only
        data = data.loc[data['name'].isin(['Investment_Trust', 'Foreign_Investor'])]

        # select columns you need
        data = data[['date', 'stock_id', 'buy', 'name', 'sell']]

        # group data by date and stock_id, and sum the buy and sell columns
        data = data.groupby(['date', 'stock_id']).agg({'buy': 'sum', 'sell': 'sum'}).reset_index()

        # add value column
        data['value'] = data['buy'] - data['sell']

        return data

    def process_buy_sell_data(self):
        workdays_str = self.get_workdays(2)
        with pd.ExcelWriter('stock_data2.xlsx') as writer:
            for date in workdays_str:
                # get stock data
                stock = self.get_buy_sell_data(date)
                # select data for stock list
                stock = stock[stock['stock_id'].isin(stock_list)]
                # add value column
                stock['value'] = stock['buy'] - stock['sell']
                # sort by trading money
                stock_sorted = stock.sort_values(by=['value'], ascending=False)
                stock_sorted = self.calculate_value(stock_sorted)

                sheet_name = f"{date}"
                stock_sorted.to_excel(writer, sheet_name=sheet_name, index=False)


if __name__ == '__main__':
    processor = StockBuySellProcessor()
    processor.process_buy_sell_data()

