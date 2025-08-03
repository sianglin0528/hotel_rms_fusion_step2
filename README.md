# 🏨 Hotel RMS Fusion - Step 2

AI 驅動的飯店營運決策系統，結合 **入住率預測、銷售量預測、RAG 問答、競品價格爬蟲**，  
幫助飯店經理快速做出數據驅動決策。

---

## 📸 系統截圖

| 預測入住率 & 銷售量 | AI 問答模組 | 競品價格表 |
|--------------------|------------|------------|
| ![occupancy](docs/demo1.png) | ![rag](docs/demo2.png) | ![crawler](docs/demo3.png) |

---

## 🚀 功能特色

- **入住率 & 銷售量預測**
  - 使用 Prophet、XGBoost、RandomForest
  - 自動生成未來 N 天的房間銷售預測
- **AI 決策助理**
  - 串接 OpenAI API + LangChain
  - 可針對資料庫進行 RAG 問答
- **自動 ETL 與資料庫更新**
  - 每日自動抓取最新訂單資料
  - 存入 SQLite / PostgreSQL
- **競品爬蟲 & 視覺化**
  - 抓取 OTA 平台競品價格
  - 自動生成競品價格趨勢表
- **可雲端部署**
  - Streamlit Cloud / Docker / AWS 一鍵上線

---

## 🏗 系統架構

```mermaid
graph TD

A[ETL Pipeline] -->|每日更新| B[(SQLite / PostgreSQL)]
B --> C[ML Model - XGBoost & RF]
C --> D[入住率 & 銷售量預測圖]
B --> E[RAG 問答模組]
E --> F[AI 決策助理 (OpenAI API)]
G[競品爬蟲 Crawler] --> B
F --> H[Streamlit Web UI]
D --> H
H --> I[管理者決策]
```

---

## 📂 專案結構

```
HOTEL_RMS_FUSION_STEP2/
│
├── app.py                # Streamlit 主程式
├── etl_pipeline.py       # ETL 更新資料
├── crawler_pipeline.py   # 競品價格爬蟲
├── ml_model.py           # ML 模型訓練與預測
├── utils/                # 工具函數、RAG 模組
├── database/             # SQLite / PostgreSQL DB
├── data/                 # 原始與處理後資料
├── requirements.txt      # 套件需求
├── .env                  # OpenAI Key & DB 設定
└── README.md             # 專案說明
```

---

## ⚡ 快速開始

1️⃣ 安裝環境
```bash
git clone https://github.com/sianglin0528/hotel_rms_fusion_step2.git
cd hotel_rms_fusion_step2
pip install -r requirements.txt
```

2️⃣ 設定環境變數 `.env`
```
OPENAI_API_KEY=your_key
DATABASE_URL=sqlite:///database/hotel_data.db
```

3️⃣ 本地啟動
```bash
streamlit run app.py
```

4️⃣ 自動推送至 GitHub
```bash
sh git_push.sh
```

---

## 📊 模型說明

- **Prophet** → 基本入住率趨勢預測
- **XGBoost / RandomForest** → 多特徵銷售量預測
- **RAG 問答** → 根據內部資料庫回答問題
- **競品爬蟲** → 抓取 OTA 競品價格，輔助定價策略

---

## 🔮 未來優化方向

- 加入 **模型準確率視覺化** (MAE / RMSE)
- 增加 **自動調價建議** 模組
- 部署至 **AWS Lambda + CI/CD 自動化流程**
