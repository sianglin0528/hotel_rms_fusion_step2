import pandas as pd

def load_and_process_data(csv_path):
    df = pd.read_csv(csv_path, parse_dates=['date'])
    df['weekday'] = df['date'].dt.weekday
    df['month'] = df['date'].dt.month
    return df
