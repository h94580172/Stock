import requests
import pandas as pd
from datetime import datetime
from List import holiday_dates, stock_list

class StockDataProcessor:
    def __init__(self):
        self.holidays = pd.to_datetime(holiday_dates)
        self.custom_bday = pd.offsets.CustomBusinessDay(holidays=self.holidays)
        self.today = datetime.today()
        self.url = "https://api.finmindtrade.com/api/v4/data"
        self.parameter = {
            "dataset": "TaiwanStockPriceAdj",
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRlIjoiMjAyMy0wMy0yOCAyMjo0ODozNyIsInVzZXJfaWQiOiJoOTQ1ODAxNzIiLCJpcCI6IjE4MC4xNzcuMC4yMDEifQ.OEggToxfSdTQAT5Qmve6gR_NfTyH_-L8LssFKTIXO9Q",
        }
        self.value_list = [1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]

    def get_workdays(self, days_to_subtract):
        """
        Returns a list of workdays by subtracting the given number of days from today's date and excluding holidays.
        """
        start_date = pd.Timestamp(self.today) - self.custom_bday * days_to_subtract
        last_workday = pd.Timestamp(self.today) - self.custom_bday
        workdays = pd.date_range(start=start_date, end=last_workday, freq=self.custom_bday)

        # Convert dates to the specified format
        workdays_str = [d.strftime('%Y-%m-%d') for d in workdays]
        return workdays_str

    def get_stock_data(self, date):
        """
        Returns stock data for the given date from the FinMind API.
        """
        self.parameter["start_date"] = date
        resp = requests.get(self.url, params=self.parameter)
        data = resp.json()
        data = pd.DataFrame(data["data"])
        return data

    def calculate_value(self, stock_sorted):
        """
        Calculates the value of each stock based on its trading volume and percent change.
        """
        for i in range(len(stock_sorted)):
            if i < 100:
                stock_sorted.loc[stock_sorted.index[i], 'value'] = self.value_list[i//10] * 0.7
            else:
                stock_sorted.loc[stock_sorted.index[i], 'value'] = -0.1    
        return stock_sorted

    def process_stock_data(self):
        """
        Processes stock data for the last 20 workdays and writes it to an Excel file.
        """
        workdays_str = self.get_workdays(20)
        with pd.ExcelWriter('stock_data.xlsx') as writer:
            for date in workdays_str:
                # Get stock data
                stock = self.get_stock_data(date)

                # Select data for stock list
                stock = stock[stock['stock_id'].isin(stock_list)]

                # Calculate percent change
                stock['percent_change'] = round((stock['spread'] / stock['open']) * 100, 2)

                # Convert trading volume and money to thousands
                stock[['Trading_Volume', 'Trading_money']] /= 1000
                stock = stock.rename(columns={'Trading_Volume': 'Trading_Volume(k)', 'Trading_money': 'Trading_money(k)'})

                # Sort by trading money
                stock_sorted = stock.sort_values(by=['Trading_money(k)'], ascending=False)

                # Calculate value
                stock_sorted = self.calculate_value(stock_sorted)
                stock_sorted['value'] = stock_sorted['value'] + stock['percent_change'] / 10

                # Write to Excel
                sheet_name = f"{date}"
                stock_sorted.to_excel(writer, sheet_name=sheet_name, index=False)

if __name__ == '__main__':
    processor = StockDataProcessor()
    processor.process_stock_data()

