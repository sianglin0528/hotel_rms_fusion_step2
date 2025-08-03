import pandas as pd
import sqlite3
import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import os

DB_PATH = 'database/hotel_data.db'

# 建立 models 資料夾（若不存在）
os.makedirs('models', exist_ok=True)

def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql('SELECT * FROM hotel_data', conn, parse_dates=['date'])
    conn.close()

    # 增加 weekday & month
    if 'weekday' not in df.columns:
        df['weekday'] = df['date'].dt.weekday
    if 'month' not in df.columns:
        df['month'] = df['date'].dt.month

    return df

def train_models():
    df = load_data()
    features = ['weekday', 'month']
    X = df[features]

    metrics_log = []  # 儲存模型評估結果

    for target in ['occupancy_rate', 'room_sold']:
        y = df[target]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Random Forest
        rf = RandomForestRegressor(n_estimators=100, random_state=42)
        rf.fit(X_train, y_train)
        rf_pred = rf.predict(X_test)
        joblib.dump(rf, f'models/{target}_rf.pkl')

        rf_mae = mean_absolute_error(y_test, rf_pred)
        rf_rmse = np.sqrt(mean_squared_error(y_test, rf_pred))

        # XGBoost
        xgb = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
        xgb.fit(X_train, y_train)
        xgb_pred = xgb.predict(X_test)
        joblib.dump(xgb, f'models/{target}_xgb.pkl')

        xgb_mae = mean_absolute_error(y_test, xgb_pred)
        xgb_rmse = np.sqrt(mean_squared_error(y_test, xgb_pred))

        # 儲存評估結果
        metrics_log.append({
            'target': target,
            'RF_MAE': rf_mae, 'RF_RMSE': rf_rmse,
            'XGB_MAE': xgb_mae, 'XGB_RMSE': xgb_rmse
        })

        print(f"✅ {target} 模型完成")
        print(f"   RF -> MAE: {rf_mae:.2f}, RMSE: {rf_rmse:.2f}")
        print(f"   XGB -> MAE: {xgb_mae:.2f}, RMSE: {xgb_rmse:.2f}")
        print("-"*50)

    # 儲存評估到 CSV
    metrics_df = pd.DataFrame(metrics_log)
    metrics_df.to_csv('models/model_metrics.csv', index=False)
    print("📄 模型評估結果已存到 models/model_metrics.csv")

def predict_future(days=7):
    """使用 XGBoost 模型預測未來入住率 & 銷售量"""
    df = load_data()
    last_date = df['date'].max()

    future_dates = pd.date_range(last_date + pd.Timedelta(days=1), periods=days)
    future_df = pd.DataFrame({
        'date': future_dates,
        'weekday': future_dates.weekday,
        'month': future_dates.month
    })

    # 預測 occupancy_rate 和 room_sold
    for target in ['occupancy_rate', 'room_sold']:
        model = joblib.load(f'models/{target}_xgb.pkl')
        X_future = future_df[['weekday', 'month']]
        future_df[f'pred_{target}'] = model.predict(X_future)

    # 輸出結果
    future_df.to_csv('models/future_prediction.csv', index=False)
    print("📄 未來預測結果已存到 models/future_prediction.csv")
    print(future_df[['date', 'pred_occupancy_rate', 'pred_room_sold']])

if __name__ == "__main__":
    train_models()
    predict_future(days=7)


