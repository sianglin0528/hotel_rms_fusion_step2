import pandas as pd
import re
from utils.rag_module import rag_answer

# -------------------------------
# 1️⃣ 簡單 NLP 問題分類
# -------------------------------
def classify_question(question: str) -> str:
    """
    簡單 NLP 問題分類：
    - 人手 / 班表
    - 價格 / 銷售
    - 入住 / 空房 / 佔用
    - 其他
    """
    q = question.lower()
    if re.search(r"人手|員工|排班", q):
        return 'staff'
    elif re.search(r"價格|房價|銷售", q):
        return 'pricing'
    elif re.search(r"入住|空房|佔用", q):
        return 'occupancy'
    else:
        return 'general'

# -------------------------------
# 2️⃣ 主函式：產生 AI 決策建議
# -------------------------------
def generate_ai_suggestion(user_question: str, future_df: pd.DataFrame) -> str:
    """
    根據未來 7 天預測入住率產生 AI 建議
    - 回傳：建議文字
    """
    # 計算平均 & 最近一天入住率
    avg_pred = future_df['pred_occupancy_rate'].mean()     # 已是 0~100
    latest_pred = future_df['pred_occupancy_rate'].iloc[0] # 已是 0~100

    # 問題分類
    q_type = classify_question(user_question)

    # 針對入住率/價格/銷售問題 → 回傳決策建議
    if q_type in ['occupancy', 'pricing']:
        if latest_pred < 50:
            suggestion = f"未來入住率偏低 ({latest_pred:.0f}%)，建議降價促銷或推出早鳥方案。"
        elif latest_pred < 80:
            suggestion = f"未來入住率中等 ({latest_pred:.0f}%)，建議維持價格並適度推廣。"
        else:
            suggestion = f"未來入住率偏高 ({latest_pred:.0f}%)，可適度加價並限制取消策略。"

        ai_answer = (
            f"📊 平均預測入住率 {avg_pred:.0f}%\n"
            f"💡 決策建議：{suggestion}"
        )
        return ai_answer

    # 其他問題 → 走 RAG
    return f"🤖 RAG 回答：{rag_answer(user_question)}"

# -------------------------------
# 3️⃣ 每日建議函式 (可用於表格顯示)
# -------------------------------
def daily_suggestion(x: float) -> str:
    """依每日預測入住率給建議"""
    if x < 50:
        return "低需求：降價促銷"
    elif x < 80:
        return "中需求：維持價格"
    else:
        return "高需求：加價或限取消"


    future_df['建議'] = future_df['pred_occupancy_rate'].apply(daily_suggestion)

    return ai_answer, future_df
