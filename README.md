# 🏨 Hotel RMS Fusion Step 2
**飯店營運決策 AI 助理 | Hotel Revenue Management AI Assistant**

---

## 📖 專案簡介
這是一個 **智慧飯店營運決策系統**，整合以下功能：

- 📈 **入住率與銷售量預測**（Prophet + XGBoost + RandomForest）  
- 🗄 **ETL 與資料庫管理**（每日自動更新資料）  
- 🤖 **AI 問答助手（RAG）**，可讀取內部資料庫回答營運問題  
- 🕵️‍♂️ **競品價格爬蟲**，提供動態定價策略  
- ☁️ **雲端部署**（Streamlit Cloud / Docker-ready）  

**使用場景：**  
- 飯店經理想知道未來 7 天的入住率與銷售量  
- 想快速獲得營運建議（例如「今天入住率低怎麼辦？」）  
- 想根據競品動態調整價格策略  

---

## 🛠 技術架構

```
Hotel RMS Fusion Step 2
├── app.py                 # 主入口，Streamlit Dashboard
├── etl_pipeline.py        # 每日資料更新 (ETL)
├── ml_model.py            # 機器學習模型訓練 & 預測
├── rag_module.py          # RAG 問答模組 (LangChain + LlamaIndex)
├── crawler_pipeline.py    # 競品價格爬蟲
├── database/
│   └── hotel_data.db      # SQLite 資料庫
├── models/                # 儲存訓練好的模型
├── utils/                 # 工具函式
└── requirements.txt       # 套件依賴
```

**主要技術棧：**  
- **Python**：Pandas、scikit-learn、XGBoost、Prophet  
- **AI 問答**：LangChain + LlamaIndex + OpenAI API  
- **資料庫**：SQLite（可擴展 PostgreSQL）  
- **爬蟲**：BeautifulSoup / Playwright  
- **雲端**：Streamlit Cloud，支援 Docker  

---

## 🚀 功能展示

1️⃣ **入住率 & 銷售量預測**  
2️⃣ **AI 問答助手（RAG）**  
3️⃣ **競品動態價格分析**  

---

## ⚡ 快速啟動

```bash
# 1️⃣ 下載專案
git clone https://github.com/yourname/hotel_rms_fusion_step2.git
cd hotel_rms_fusion_step2

# 2️⃣ 安裝套件
pip install -r requirements.txt

# 3️⃣ 啟動 Streamlit
streamlit run app.py
```

> 預設使用 **SQLite**，可自行修改為 **PostgreSQL**。  
> 若需啟用 **RAG 問答功能**，請在 `.env` 中設定 `OPENAI_API_KEY`。  

---

## 📌 專案進度

| 階段 | 狀態 |
|------|------|
| Step 0：原始專案             | ✅ 完成 |
| Step 1：ETL + SQL 資料庫     | ✅ 完成 |
| Step 2：加入機器學習模型     | ✅ 完成 |
| Step 3：RAG 問答模組         | ✅ 完成 |
| Step 4：競品爬蟲 & 視覺化    | ✅ 完成 |
| Step 5：雲端部署             | ✅ 完成 |

---

## 📬 聯絡方式

- **作者**：香琳  
- **Email**：your_email@example.com  
- **LinkedIn / GitHub**：your_profile_link  
