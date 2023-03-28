import requests
from bs4 import BeautifulSoup
import random
import logging

class Login:
    
    def __init__(self):
        self.user_agent_list = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"
        ]
        self.user_proxy_list = [
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
        
    def get_user_agent(self) -> str:
        user_agent = random.choice(self.user_agent_list)
        return {
            "User-Agent": user_agent
        }

    def get_proxy(self) -> dict:
        user_proxy = random.choice(self.user_proxy_list)
        return {
            "http" : user_proxy
        }

    def get_html(self, url: str, header: dict, proxy: dict) -> str:
        try:
            with requests.Session() as session:
                res = session.get(url, headers=header, proxies=proxy, timeout=30)
                res.encoding = 'UTF-8'
                return res.text
        except requests.exceptions.RequestException as e:
            logging.error(f"Error occurred while getting html: {e}")
            return None

    def get_soup(self, html: str) -> BeautifulSoup:
        return BeautifulSoup(html, 'lxml')

url = 'https://www.google.com'
header = Login().get_user_agent()
proxy = Login().get_proxy()
html = Login().get_html(url, header, proxy)
soup = Login().get_soup(html)

logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
