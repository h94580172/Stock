import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import random
import time

# 讀取Excel檔案
df = pd.read_excel('stock_list.xlsx')

df['數值'] = 0

# 定義要爬取的網址(漲停股)
url = 'https://goodinfo.tw/tw2/StockList.asp?MARKET_CAT=%E6%99%BA%E6%85%A7%E9%81%B8%E8%82%A1&INDUSTRY_CAT=%E6%BC%B2%E5%81%9C%E8%82%A1'

# 隨機選擇一個 User-Agent
user_agent_list = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"
]
user_agent = random.choice(user_agent_list)

# 設置標頭
header = {
    "User-Agent": user_agent
}

# 向網站發送請求
res = requests.get(url, headers = header)
res.encoding = 'UTF-8'

# 解析 HTML 原始碼
soup = BeautifulSoup(res.text, 'html.parser')

tables = soup.find_all('table', {'class': 'r10_0_0_10 b1 p4_1'})
for table in tables:
    rows = table.find_all('a')
    for i, row in enumerate(rows):
        if i % 2 == 0:
            row_title = row.get('title')
            if row_title is not None:
                stock_number = re.findall('\d+', row_title)[0]
                # 對每一筆資料進行判斷
                df.loc[df['股票代號'] == int(stock_number), '數值'] += 5

# 將修改後的資料寫回Excel檔案
df.to_excel('stock_list.xlsx', index=False)
