from FinMind.data import DataLoader
import datetime

api = DataLoader()
api.login_by_token(api_token='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRlIjoiMjAyMy0wMy0yOCAyMjo0ODozNyIsInVzZXJfaWQiOiJoOTQ1ODAxNzIiLCJpcCI6IjE4MC4xNzcuMC4yMDEifQ.OEggToxfSdTQAT5Qmve6gR_NfTyH_-L8LssFKTIXO9Q')
api.login(user_id='h94580172',password='h94228200')


today = datetime.date.today()
# 讀取數據
df = api.taiwan_stock_daily(start_date=today)