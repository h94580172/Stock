import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time
import random
import os
import datetime

def check_file_exist(file_path: str) -> bool:
    return os.path.exists(file_path)

def get_user_agent() -> str:
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"
    ]
    return random.choice(user_agent_list)

def get_proxy() -> dict:
    user_proxy_list = [
        '204.2.218.145:80',
        '103.121.149.66:8080',
        '144.202.100.17:80',
        '86.110.212.151:3128',
        '152.67.10.190:8080',
        '8.219.176.202:80',
        '170.39.193.234:80',
        '139.178.66.232:8080',
        '125.17.80.229:80',
        '107.152.42.99:80',
        '181.78.82.131:80',
        '203.104.31.155:80',
        '117.54.161.36:8080',
        '115.135.60.22:8080',
        '136.0.95.99:80',
        '200.8.57.8:8080'
    ]
    user_proxy = random.choice(user_proxy_list)
    return {
        "http" : user_proxy
    }

def get_html(url: str, headers: dict, proxies: dict) -> str:
    with requests.Session() as session:
        res = session.get(url, headers=headers, proxies=proxies, timeout=10)
        res.encoding = 'UTF-8'
        return res.text

def get_soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, 'lxml')

def update_excel(url: str, column_name: str, value: float, sleep_time: int = 5) -> None:
    if url is None:
        return
    
    if not check_file_exist('stock_list.xlsx'):
        print('Excel 檔案不存在')
        return
    
    df = pd.read_excel('stock_list.xlsx')
    df['數值'] = df['數值'].fillna(0)

    user_agent = get_user_agent()
    header = {
        "User-Agent": user_agent
    }
    proxy = get_proxy()
    html = get_html(url, header, proxy)
    soup = get_soup(html)

    tables = soup.find_all('table', {'class': 'r10_0_0_10 b1 p4_1'})
    for table in tables:
        rows = table.find_all('a')
        for i, row in enumerate(rows):
            if i % 2 == 0:
                row_href = row.get('href')
                if row_href is not None:
                    stock_number = re.findall('\d+', row_href)[0]
                    df.loc[df['股票代號'] == int(stock_number), column_name] += value

    df.to_excel('stock_list.xlsx', index=False)
    
    # create folder and save excel
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    if not os.path.exists(today):
        os.makedirs(today)
    df.to_excel(f'{today}/stock_list.xlsx', index=False)
    
    time.sleep(random.randint(sleep_time, sleep_time+5))

update_list = [
    ('https://goodinfo.tw/tw2/StockList.asp?MARKET_CAT=%E6%99%BA%E6%85%A7%E9%81%B8%E8%82%A1&INDUSTRY_CAT=%E6%BC%B2%E5%81%9C%E8%82%A1', '數值', 3),
    ('https://goodinfo.tw/tw2/StockList.asp?MARKET_CAT=%E6%99%BA%E6%85%A7%E9%81%B8%E8%82%A1&INDUSTRY_CAT=%E6%BC%B27%25%E8%82%A1', '數值', 2),
    ('https://goodinfo.tw/tw2/StockList.asp?RPT_TIME=&MARKET_CAT=%E6%99%BA%E6%85%A7%E9%81%B8%E8%82%A1&INDUSTRY_CAT=%E9%80%A3%E7%BA%8C%E5%A4%9A%E6%97%A5%E6%BC%B25%25%E4%BB%A5%E4%B8%8A%40%40%E9%80%A3%E7%BA%8C%E5%A4%9A%E6%AC%A1%E6%BC%B25%25%E4%BB%A5%E4%B8%8A%40%40%E9%80%A3%E7%BA%8C%E5%A4%9A%E6%97%A5%E6%BC%B25%25%E4%BB%A5%E4%B8%8A', '數值', 1),
    ('https://goodinfo.tw/tw2/StockList.asp?RPT_TIME=&MARKET_CAT=%E6%99%BA%E6%85%A7%E9%81%B8%E8%82%A1&INDUSTRY_CAT=%E8%82%A1%E5%83%B9%E5%89%B5%E4%B8%89%E5%B9%B4%E9%AB%98%E9%BB%9E%40%40%E8%82%A1%E5%83%B9%E5%89%B5%E5%A4%9A%E6%97%A5%E9%AB%98%E9%BB%9E%40%40%E4%B8%89%E5%B9%B4', '數值', 5),
    ('https://goodinfo.tw/tw2/StockList.asp?MARKET_CAT=%E6%99%BA%E6%85%A7%E9%81%B8%E8%82%A1&INDUSTRY_CAT=%E8%B7%8C%E5%81%9C%E8%82%A1', '數值', -3),
    ('https://goodinfo.tw/tw2/StockList.asp?MARKET_CAT=%E6%99%BA%E6%85%A7%E9%81%B8%E8%82%A1&INDUSTRY_CAT=%E8%B7%8C7%25%E8%82%A1', '數值', -2),
    ('https://goodinfo.tw/tw2/StockList.asp?MARKET_CAT=%E6%99%BA%E6%85%A7%E9%81%B8%E8%82%A1&INDUSTRY_CAT=%E8%B7%8C5%25%E8%82%A1', '數值', -1),
    ('https://goodinfo.tw/tw2/StockList.asp?RPT_TIME=&MARKET_CAT=%E6%99%BA%E6%85%A7%E9%81%B8%E8%82%A1&INDUSTRY_CAT=%E6%8A%95%E4%BF%A1%E9%80%A3%E8%B2%B7+%E2%80%93+%E6%97%A5%40%40%E6%8A%95%E4%BF%A1%E9%80%A3%E7%BA%8C%E8%B2%B7%E8%B6%85%40%40%E6%8A%95%E4%BF%A1%E9%80%A3%E7%BA%8C%E8%B2%B7%E8%B6%85+%E2%80%93+%E6%97%A5', '數值', 1),
    ('https://goodinfo.tw/tw2/StockList.asp?RPT_TIME=&MARKET_CAT=%E6%99%BA%E6%85%A7%E9%81%B8%E8%82%A1&INDUSTRY_CAT=%E5%A4%96%E8%B3%87%E9%80%A3%E8%B2%B7+%E2%80%93+%E6%97%A5%40%40%E5%A4%96%E8%B3%87%E9%80%A3%E7%BA%8C%E8%B2%B7%E8%B6%85%40%40%E5%A4%96%E8%B3%87%E9%80%A3%E7%BA%8C%E8%B2%B7%E8%B6%85+%E2%80%93+%E6%97%A5'
, '數值', 1)
]

for update in update_list:
    update_excel(*update)
