#!/bin/bash
# 自動 Git 推送腳本

# 1️⃣ 顯示當前分支與狀態
echo "=== 當前 Git 狀態 ==="
git status

# 2️⃣ 加入所有變更
git add .
echo "✅ 已加入所有檔案"

# 3️⃣ 自動生成 commit 訊息（含日期時間）
commit_msg="Auto commit on $(date '+%Y-%m-%d %H:%M:%S')"
git commit -m "$commit_msg"
echo "✅ 已提交 commit: $commit_msg"

# 4️⃣ 推送到 main 分支
git push origin main
echo "🚀 推送完成！"
