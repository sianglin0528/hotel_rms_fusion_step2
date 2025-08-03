import pandas as pd
import sqlite3

def run_etl(csv_path='data/hotel_data.csv', db_path='database/hotel_data.db'):
    df = pd.read_csv(csv_path, parse_dates=['date'])
    conn = sqlite3.connect(db_path)
    df.to_sql('hotel_data', conn, if_exists='replace', index=False)
    conn.close()
    print('ETL completed!')

if __name__ == "__main__":
    run_etl()
