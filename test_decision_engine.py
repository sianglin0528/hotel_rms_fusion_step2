import pandas as pd
from utils.decision_engine import generate_ai_suggestion

# 模擬未來 7 天入住率
future_df = pd.DataFrame({
    'pred_occupancy_rate': [45, 55, 60, 70, 80, 85, 90]
})

# 測試各種問題
print(generate_ai_suggestion("明天入住率很低怎麼辦？", future_df))
print(generate_ai_suggestion("我們人手夠嗎？", future_df))
