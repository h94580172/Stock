import pandas as pd
from Stock_data import Common
import datetime
import os

class StockValues:
    def __init__(self, file_path):
        self.file_path = file_path
        self.common = Common()
        self.workdays = self.common.get_workdays(20)
        self.stock_data = {}
        self.stock_temp_data = pd.DataFrame()
        self.df = pd.DataFrame()

    def read_excel_file(self, column_name):
        excel_file = pd.ExcelFile(self.file_path)
        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            for stock_id in df['stock_id'].unique():
                if stock_id not in self.stock_data:
                    self.stock_data[stock_id] = {}
                self.stock_data[stock_id][sheet_name] = df[df['stock_id']==stock_id][column_name].sum()

    def convert_to_dataframe(self):
        self.stock_temp_data = pd.DataFrame(self.stock_data)
        self.stock_temp_data.index = self.workdays
        self.df = self.stock_temp_data.T
        self.df.columns = pd.to_datetime(self.df.columns).strftime('%Y-%m-%d')
        self.df.index.name = 'stock_id'

    def calculate_moving_averages(self):
        self.df['5sma'] = self.df.rolling(window=5, axis=1).mean().iloc[:, -1]
        self.df['10sma'] = self.df.rolling(window=10, axis=1).mean().iloc[:, -2]
        self.df['20sma'] = self.df.rolling(window=20, axis=1).mean().iloc[:, -3]

    def calculate_values(self):
        self.df['value'] = 0
        last_workday = self.workdays[-1]
        self.df.loc[self.df[last_workday] >= self.df['5sma'], 'value'] += 0.05
        self.df.loc[self.df[last_workday] < self.df['5sma'], 'value'] -= 0.05
        self.df.loc[self.df[last_workday] >= self.df['10sma'], 'value'] += 0.15
        self.df.loc[self.df[last_workday] < self.df['10sma'], 'value'] -= 0.15
        self.df.loc[self.df[last_workday] >= self.df['20sma'], 'value'] += 0.25
        self.df.loc[self.df[last_workday] < self.df['20sma'], 'value'] -= 0.25

    def calculate_stock_sma(self):
        self.read_excel_file('close')
        self.convert_to_dataframe()
        self.calculate_moving_averages()
        self.calculate_values()
        return self.df

    def calculate_stock_values(self):
        self.read_excel_file('value')
        stock_temp_data = pd.DataFrame(self.stock_data)
        stock_temp_data.index = self.workdays
        stock_temp_data = stock_temp_data.T
        stock_temp_data['value'] = stock_temp_data.sum(axis=1)
        stock_temp_data.insert(0, 'stock_id', stock_temp_data.index)
        stock_temp_data.to_excel('stock_value.xlsx', index=False)

def main():
    stock_sma = StockValues('stock_data.xlsx')
    stock_sma.calculate_stock_sma().to_excel('stock_sma.xlsx', index=True)
    stock_values = StockValues('stock_merged_data.xlsx')
    stock_values.calculate_stock_values()

    if not os.path.exists('StockFile'):
        os.makedirs('StockFile')

    df1 = pd.read_excel('stock_sma.xlsx')
    df2 = pd.read_excel('stock_value.xlsx')
    merged_df = pd.merge(df1, df2, on='stock_id', how='outer')
    merged_df['value'] = merged_df['value_x'].fillna(0) + merged_df['value_y'].fillna(0)
    result_df = merged_df[['stock_id', 'value']]
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    result_df.to_excel(f'StockFile/{today}_StockValue.xlsx', sheet_name=today, index=False)

main()
