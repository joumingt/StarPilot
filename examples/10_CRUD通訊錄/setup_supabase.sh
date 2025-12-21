#!/bin/bash
# Supabase 資料表設定腳本

echo "🚀 開始設定 Supabase 資料表..."
echo ""
echo "請遵循以下步驟："
echo "1️⃣  登入 Supabase: https://supabase.com"
echo "2️⃣  進入你的專案 (URL: https://dldbdiqrgqgybswhuabd.supabase.co)"
echo "3️⃣  點擊左邊菜單的『SQL Editor』"
echo "4️⃣  點擊『+ New Query』"
echo "5️⃣  複製下方的 SQL 命令並執行"
echo ""
echo "========== 複製以下 SQL 命令 =========="
echo ""
cat supabase_setup.sql
echo ""
echo "========================================="
echo ""
echo "✅ 執行完成後，再回來運行應用！"
echo ""
echo "接著運行: streamlit run streamlit_app.py"
