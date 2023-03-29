from FinMind.data import DataLoader

api = DataLoader()
api.login_by_token(api_token='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRlIjoiMjAyMy0wMy0yOCAyMjo0ODozNyIsInVzZXJfaWQiOiJoOTQ1ODAxNzIiLCJpcCI6IjE4MC4xNzcuMC4yMDEifQ.OEggToxfSdTQAT5Qmve6gR_NfTyH_-L8LssFKTIXO9Q')
api.login(user_id='h94580172',password='h94228200')

from datetime import datetime

today = datetime.today().strftime('%Y-%m-%d')

df = api.taiwan_stock_daily(start_date = today)

print(df)