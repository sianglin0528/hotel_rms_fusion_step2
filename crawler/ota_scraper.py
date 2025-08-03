#模擬抓取自家 OTA 資料：
import pandas as pd
from datetime import datetime

def fetch_ota_data():
    """模擬 OTA 自家房價資料"""
    today = datetime.today().strftime("%Y-%m-%d")
    data = [
        {"date": today, "room_type": "Standard", "price": 120, "available_rooms": 5},
        {"date": today, "room_type": "Deluxe", "price": 180, "available_rooms": 3},
        {"date": today, "room_type": "Suite", "price": 300, "available_rooms": 1},
    ]
    df = pd.DataFrame(data)
    df.to_csv("data/ota_data.csv", mode='a', index=False, header=False)
    return df

if __name__ == "__main__":
    print(fetch_ota_data())
