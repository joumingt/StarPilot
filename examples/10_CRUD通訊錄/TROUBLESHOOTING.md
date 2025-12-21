# 故障排除指南

## 🔧 解決 502 錯誤

### 步驟 1: 清理環境
```bash
# 停止所有 Streamlit 進程
pkill -f streamlit

# 等待 2 秒
sleep 2
```

### 步驟 2: 清除快取
1. 關閉所有瀏覽器的 Streamlit 頁面
2. 按 Ctrl+Shift+Delete 清除瀏覽器快取
3. 或使用無痕模式開啟

### 步驟 3: 啟動測試版
```bash
cd /workspaces/StarPilot/examples/10_CRUD通訊錄
streamlit run test_app.py --server.port=8502
```

打開瀏覽器訪問: http://localhost:8502

### 步驟 4: 如果測試版正常，啟動正式版
```bash
streamlit run streamlit_app.py --server.port=8501
```

打開瀏覽器訪問: http://localhost:8501

### 步驟 5: 如果還有問題
```bash
# 檢查端口是否被佔用
lsof -i :8501
lsof -i :8502

# 如果有進程佔用，kill 它
kill -9 <PID>

# 重新啟動
streamlit run streamlit_app.py --server.port=8503
```

## ✅ 應用功能驗證

所有後端功能都已測試通過：
- ✅ 新增聯絡人
- ✅ 編輯聯絡人  
- ✅ 刪除聯絡人
- ✅ 搜尋功能
- ✅ 統計圖表

502 錯誤通常是：
1. 瀏覽器快取問題
2. 端口衝突
3. Streamlit health check 失敗

建議先用測試版驗證基本功能，再使用正式版。
