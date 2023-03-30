import pandas as pd

# 讀取 Excel 檔案
df = pd.read_excel("112年辦公日曆表.xlsx", sheet_name="sheet1", header=None)

# 篩選出紫色放假日
holiday_dates = []
for i in range(len(df)):
    for j in range(len(df.columns)):
        cell_color = df.iloc[i, j].fill.bgColor.rgb.lower()
        if cell_color == "#FF99FF":
            holiday_dates.append(df.iloc[i, j].date().strftime("%Y-%m-%d"))

print(holiday_dates)
