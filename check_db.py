import sqlite3
import pandas as pd

# 連線到你的 SQLite DB
conn = sqlite3.connect('database/hotel_data.db')

# 讀取最新 10 筆資料
query = "SELECT * FROM hotel_data ORDER BY date DESC LIMIT 10"
df = pd.read_sql(query, conn)

print("資料筆數：", len(df))
print(df)

conn.close()
