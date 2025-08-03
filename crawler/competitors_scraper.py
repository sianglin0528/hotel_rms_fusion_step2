#模擬抓取競品資料（之後可改成 Playwright）：
import pandas as pd
from datetime import datetime
import random

def fetch_competitor_data():
    """模擬競品房價與空房數"""
    today = datetime.today().strftime("%Y-%m-%d")
    competitors = ["Hotel A", "Hotel B", "Hotel C"]
    data = []
    for hotel in competitors:
        price = random.randint(100, 200)
        available_rooms = random.randint(0, 10)
        data.append({
            "date": today,
            "competitor": hotel,
            "price": price,
            "available_rooms": available_rooms
        })
    df = pd.DataFrame(data)
    df.to_csv("data/competitors_data.csv", mode='a', index=False, header=False)
    return df

if __name__ == "__main__":
    print(fetch_competitor_data())
