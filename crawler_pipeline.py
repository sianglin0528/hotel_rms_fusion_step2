import pandas as pd

def fetch_competitors_data(file_path="data/competitors.csv"):
    # 讀取 CSV，嘗試自動解碼，避免亂碼
    try:
        df = pd.read_csv(file_path, encoding='utf-8-sig')
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='latin1')

    # 如果沒有標題，則自動補齊欄位名
    if 'date' not in df.columns:
        df = pd.read_csv(file_path, header=None)
        col_count = df.shape[1]
        default_cols = ['hotel_name', 'date', 'price', 'room_type']
        df.columns = default_cols[:col_count]

    # 清理欄位名稱
    df.columns = [c.strip().lower() for c in df.columns]

    # -------------------------------
    # 日期清理處理
    # -------------------------------
    if 'date' in df.columns:
        # 先轉成字串並清理空白
        df['date'] = df['date'].astype(str).str.strip()

        # 嘗試用常見格式解析
        for fmt in ['%Y-%m-%d', '%Y/%m/%d', '%d-%m-%Y', '%d/%m/%Y']:
            tmp = pd.to_datetime(df['date'], format=fmt, errors='coerce')
            if tmp.notna().sum() > 0:
                df['date'] = tmp
                break

        # 如果都不匹配，最後用 pandas 自動解析
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # 移除日期無效的列
    df = df.dropna(subset=['date'])

    # 顯示前幾筆 debug
    print("✅ Cleaned competitors data:")
    print(df.head())

    return df

