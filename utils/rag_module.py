# utils/rag_module.py
import os
import re
import datetime
import pandas as pd
import sqlite3
# utils/rag_module.py
import os
import re
import datetime
import pandas as pd
import sqlite3

# utils/rag_module.py
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.core.llms import ChatMessage
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
from llama_index.embeddings.openai import OpenAIEmbedding

# 指定 OpenAI embedding 模型
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")




# 初始化 LLM
llm = OpenAI(model="gpt-4o-mini", temperature=0)


# --- 新增 generate_rag_answer ---
DB_PATH = "database/hotel_data.db"
FUTURE_PRED_PATH = "models/future_prediction.csv"

def rag_answer(question: str, data_path: str = "./data") -> str:
    """
    使用 LlamaIndex 做簡單 RAG 問答
    """
    # 讀取資料夾內文件
    documents = SimpleDirectoryReader(data_path).load_data()
    
    # 解析成節點
    parser = SimpleNodeParser()
    nodes = parser.get_nodes_from_documents(documents)
    
    # 建立索引
    index = VectorStoreIndex(nodes)
    
    # 建立查詢引擎
    query_engine = index.as_query_engine(llm=llm)
    
    # 回答問題
    response = query_engine.query(question)
    
    return str(response)



def build_rag_index(data_dir="data/rag_docs"):
    documents = load_documents(data_dir)
    if not documents:
        print("⚠️ 沒有文件可供建立索引，返回空索引")
        return None
    return VectorStoreIndex.from_documents(documents)



def generate_rag_answer(user_question: str, context: dict = None):
    """
    進階版：結合 SQLite + CSV 預測資料
    如果問日期 → 回傳當日歷史/預測
    如果問趨勢 → 回傳簡單摘要
    """
    user_question = user_question.strip()

    # --- 嘗試解析日期 ---
    target_date = None
    for fmt in ["%Y/%m/%d", "%Y-%m-%d", "%Y.%m.%d"]:
        try:
            date_strs = re.findall(r"(\d{4}[/-]\d{1,2}[/-]\d{1,2})", user_question)
            if date_strs:
                target_date = datetime.datetime.strptime(date_strs[0], fmt).date()
                break
        except:
            pass

    # --- 載入資料庫 ---
    try:
        conn = sqlite3.connect(DB_PATH)
        df_hist = pd.read_sql_query("SELECT * FROM hotel_data", conn)
        conn.close()
    except Exception as e:
        df_hist = pd.DataFrame()

    try:
        df_future = pd.read_csv(FUTURE_PRED_PATH)
    except:
        df_future = pd.DataFrame()

    # --- 針對日期問題 ---
    if target_date:
        hist_match = df_hist[df_hist['date'] == str(target_date)]
        future_match = df_future[df_future['date'] == str(target_date)]

        answer = ""
        if not hist_match.empty:
            occ = hist_match['occupancy_rate'].iloc[0]
            price = hist_match['avg_price'].iloc[0]
            answer += f"{target_date} 的歷史資料：入住率 {occ:.1f}%，平均房價 {price:.0f} 元。"
        if not future_match.empty:
            pred_occ = future_match['predicted_occupancy_rate'].iloc[0]
            pred_room = future_match['predicted_room_sold'].iloc[0]
            answer += f" 預測：入住率 {pred_occ:.1f}%，預計售出 {pred_room:.0f} 間房。"

        return answer or f"找不到 {target_date} 的相關資料。"

    # --- 趨勢問題 ---
    if "趨勢" in user_question or "未來" in user_question:
        if df_future.empty:
            return "目前沒有未來預測資料。"

        avg_occ = df_future['predicted_occupancy_rate'].mean()
        max_occ_date = df_future.loc[df_future['predicted_occupancy_rate'].idxmax(), 'date']
        max_occ = df_future['predicted_occupancy_rate'].max()

        return f"未來平均入住率約 {avg_occ:.1f}%，最高入住率出現在 {max_occ_date}，約 {max_occ:.1f}%。"

    # --- 回到原本 RAG 做補充 ---
    rag_reply = rag_answer(user_question)
    return f"AI 模型回覆：{rag_reply}"
