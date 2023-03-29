import requests
import json
url = "https://api.finmindtrade.com/api/v4/login"
payload = {
    "user_id": 'h94580172',
    "password": 'h94228200',
}

try:
    # 發送請求並讀取數據
    response = requests.get(url)
    data = json.loads(response.text)
except json.decoder.JSONDecodeError as e:
    print("JSONDecodeError: ", e)
    print("Response content: ", response.content)
