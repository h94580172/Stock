import requests
import pandas as pd
from datetime import datetime
from List import holiday_dates, stock_list

class Common:
    def get_workdays(self, days_to_subtract):
        """
        Returns a list of workdays that are days_to_subtract days before today.
        Excludes weekends and holidays.
        """
        
        # Define holiday list
        holidays = pd.to_datetime(holiday_dates)

        # Set CustomBusinessDay rule to exclude holidays 
        custom_bday = pd.offsets.CustomBusinessDay(holidays=holidays)

        # Get today's date
        today = datetime.today()
        
        # Calculate the most recent workday
        start_date = (pd.Timestamp(today) + pd.Timedelta(days=1)) - custom_bday * days_to_subtract
        last_workday = pd.Timestamp(today)
        workdays = pd.date_range(start=start_date, end=last_workday, freq=custom_bday)
        
        # Convert dates to the specified format
        workdays_str = [d.strftime('%Y-%m-%d') for d in workdays]
        return workdays_str

    def calculate_value(self, stock_sorted):
        """
        Calculates the value of each stock in stock_sorted based on its ranking.
        """

        value_list = [1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
        for i in range(len(stock_sorted)):
            if i < 100:
                stock_sorted.loc[stock_sorted.index[i], 'value'] = value_list[i//10] * 0.3
            else:
                stock_sorted.loc[stock_sorted.index[i], 'value'] = -0.005    
        return stock_sorted
    
class StockDataProcessor(Common):
    def __init__(self):
        self.url = "https://api.finmindtrade.com/api/v4/data"
        self.parameter = {
            "dataset": "TaiwanStockPriceAdj",
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRlIjoiMjAyMy0wMy0yOCAyMjo0ODozNyIsInVzZXJfaWQiOiJoOTQ1ODAxNzIiLCJpcCI6IjE4MC4xNzcuMC4yMDEifQ.OEggToxfSdTQAT5Qmve6gR_NfTyH_-L8LssFKTIXO9Q",
        }

    def get_stock_data(self, date):
        """
        Returns stock data for the given date from the FinMind API.
        """
        
        self.parameter["start_date"] = date
        resp = requests.get(self.url, params=self.parameter)
        data = resp.json()
        data = pd.DataFrame(data["data"])
        return data

    def process_stock_data(self):
        """
        Processes stock data for the last 20 workdays and writes it to an Excel file.
        """
        
        workdays_str = self.get_workdays(20)
   
        with pd.ExcelWriter('stock_data.xlsx') as writer:
            for date in workdays_str:
                # Get stock data
                stock_data = self.get_stock_data(date)

                # Select data for stock list
                stock = stock_data[stock_data['stock_id'].isin(stock_list)].copy()
                
                # Calculate percent change
                stock['percent_change'] = round((stock['spread'] / stock['open']) * 100, 2)

                # Convert trading volume and money to thousands
                stock[['Trading_Volume', 'Trading_money']] /= 1000
                stock = stock.rename(columns={'Trading_Volume': 'Trading_Volume(k)', 'Trading_money': 'Trading_money(k)'})

                # Sort by trading money
                stock_sorted = stock.sort_values(by=['Trading_money(k)'], ascending=False)

                # Calculate value
                stock_sorted = self.calculate_value(stock_sorted)
                stock_sorted['value'] = stock_sorted['value'] + stock['percent_change'] / 5

                # Write to Excel
                sheet_name = f"{date}"
                stock_sorted.to_excel(writer, sheet_name=sheet_name, index=False)

class StockBuySellProcessor(Common):
    def __init__(self):
        self.url = "https://api.finmindtrade.com/api/v4/data"
        self.parameter = {
            "dataset": "TaiwanStockInstitutionalInvestorsBuySell",
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRlIjoiMjAyMy0wMy0yOCAyMjo0ODozNyIsInVzZXJfaWQiOiJoOTQ1ODAxNzIiLCJpcCI6IjE4MC4xNzcuMC4yMDEifQ.OEggToxfSdTQAT5Qmve6gR_NfTyH_-L8LssFKTIXO9Q",
        }

    def get_stock_buy_sell(self, date):
        """
        Returns institutional investor buy/sell data for the given date from the FinMind API.
        """
        
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

    def process_stock_buy_sell(self):
        workdays_str = self.get_workdays(20)
        with pd.ExcelWriter('stock_buy_sell.xlsx') as writer:
            for date in workdays_str:
                # get stock data
                stock = self.get_stock_buy_sell(date)
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
    stock_data_obj = StockDataProcessor()
    stock_data_obj.process_stock_data()
    stock_buy_sell_obj = StockBuySellProcessor()
    stock_buy_sell_obj.process_stock_buy_sell()
