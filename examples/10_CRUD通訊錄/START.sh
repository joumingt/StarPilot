#!/bin/bash

# 📇 CRUD 通訊錄快速啟動腳本

echo "╔════════════════════════════════════════════════════════╗"
echo "║      📇 CRUD 通訊錄管理系統 - 快速啟動                ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# 進入專案目錄
cd "$(dirname "$0")"

echo "📂 專案位置："
pwd
echo ""

echo "選擇運行方式："
echo ""
echo "1️⃣  命令行版本（推薦初學者）"
echo "   python contact_manager.py"
echo ""
echo "2️⃣  Web 版本（推薦實際使用）"
echo "   pip install flask"
echo "   python app.py"
echo "   然後在瀏覽器開啟 http://localhost:5000"
echo ""
echo "3️⃣  使用範例（查看 CRUD 演示）"
echo "   python example_usage.py"
echo ""
echo "4️⃣  閱讀文件"
echo "   📖 README.md - 完整文件"
echo "   🚀 QUICKSTART.md - 快速開始"
echo "   🔧 ADVANCED.md - 進階教學"
echo ""
echo "按 Ctrl+C 可返回終端機"
echo ""
echo "════════════════════════════════════════════════════════"
