import streamlit as st
import pandas as pd
import joblib
import sqlite3
from datetime import timedelta
from utils.decision_engine import generate_ai_suggestion
from utils.rag_module import generate_rag_answer
from crawler_pipeline import fetch_competitors_data

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 當前檔案所在資料夾
input_dir = os.path.join(os.path.dirname(__file__), "data", "rag_docs") # 指向 data/rag_docs

files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
if len(files) == 0:
    raise ValueError(f"No files found in {input_dir}. Found dirs: {os.listdir(os.path.join(BASE_DIR, '..', 'data'))}")


st.set_page_config(page_title="🏨 飯店營運決策 AI 助理", layout="wide")
st.title("🏨 飯店營運決策 AI 助理")
st.caption("CSV 上傳 → ETL → RF + XGB 多模型預測 → AI 問答")

DB_PATH = 'database/hotel_data.db'

# ================= 上傳飯店資料 =================
uploaded_file = st.file_uploader("📂 上傳飯店營運資料 [CSV]", type="csv")
if uploaded_file:
    df_upload = pd.read_csv(uploaded_file, parse_dates=['date'])
    conn = sqlite3.connect(DB_PATH)
    df_upload.to_sql('hotel_data', conn, if_exists='replace', index=False)
    conn.close()
    st.success("✅ 資料已更新到資料庫！")

# ================= 讀取資料 =================
conn = sqlite3.connect(DB_PATH)
df = pd.read_sql('SELECT * FROM hotel_data', conn, parse_dates=['date'])
conn.close()

if df.empty:
    st.warning("⚠️ 資料庫是空的，請先上傳 CSV 或執行 ETL。")
    st.stop()

st.subheader("📊 最近 10 筆資料")
st.dataframe(df.tail(10))

# ================= 多模型預測 (RF + XGB) =================
st.subheader("🤖 多模型預測 (RF + XGB)")

rf_occ = joblib.load('models/occupancy_rate_rf.pkl')
xgb_occ = joblib.load('models/occupancy_rate_xgb.pkl')

last_date = df['date'].max()
future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=7)

future_df = pd.DataFrame({'date': future_dates})
future_df['weekday'] = future_df['date'].dt.weekday
future_df['month'] = future_df['date'].dt.month

# 預測入住率
future_df['rf_pred'] = rf_occ.predict(future_df[['weekday','month']])
future_df['xgb_pred'] = xgb_occ.predict(future_df[['weekday','month']])
future_df['pred_occupancy_rate'] = future_df[['rf_pred','xgb_pred']].mean(axis=1)

st.line_chart(future_df.set_index('date')['pred_occupancy_rate'] / 100)

avg_rate = future_df['pred_occupancy_rate'].mean()
st.markdown(f"🤖 模型建議：📊 平均預測入住率 **{avg_rate:.2f}%**")



st.dataframe(future_df)

# ========================AI 決策建議 (RAG)========================
st.subheader("💡 AI 決策建議")
st.caption("請輸入問題（例：今天入住率很低怎麼辦？）")

user_question = st.text_input("問題：")
if user_question:
    # 將預測結果當作 context 傳給 RAG
    context = {
        "latest_data": df.tail(3).to_dict(orient="records"),
        "future_prediction": future_df.to_dict(orient="records")
    }
    rag_answer = generate_rag_answer(user_question, context)
    st.write(f"🤖 AI 回覆：{rag_answer}")




st.subheader("🏨 競品即時價格")
comp_df = fetch_competitors_data()
st.dataframe(comp_df)

# 簡單策略建議
avg_price = comp_df.groupby("hotel_name")["price"].mean().reset_index()
avg_price.columns = ["hotel_name", "avg_price"]

st.subheader("💡 簡單價格策略建議")
for _, row in avg_price.iterrows():
    if row["avg_price"] > 3500:
        st.write(f"{row['hotel_name']} 平均價格 {row['avg_price']} 元，可考慮降價促銷")
    else:
        st.write(f"{row['hotel_name']} 平均價格 {row['avg_price']} 元，可維持或小幅調漲")