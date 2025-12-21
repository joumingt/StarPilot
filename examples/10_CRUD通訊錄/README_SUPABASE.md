# 📇 Supabase 版本通訊錄管理系統

**改用雲端 Supabase 資料庫，支援多裝置同步！**

## 🎯 快速開始 (3 步驟)

### 1️⃣ 建立 Supabase 資料表
```bash
bash setup_supabase.sh
```
按照指示在 Supabase SQL Editor 執行 SQL

### 2️⃣ 安裝依賴
```bash
pip install -r requirements.txt
```

### 3️⃣ 運行應用
```bash
streamlit run streamlit_app.py
```

🎉 完成！打開 http://localhost:8501

## ✅ 環境設定狀態

```
✅ Python 3.11.14
✅ .env 檔案已配置
✅ streamlit 1.52.2
✅ supabase 2.27.0
✅ python-dotenv
⏳ Supabase 資料表 (需要手動建立)
```

執行 `python3 healthcheck.py` 檢查完整狀態。

## 📋 檔案說明

| 檔案 | 說明 |
|------|------|
| `contact_manager.py` | 核心業務邏輯 (Supabase 版本) |
| `streamlit_app.py` | Web UI 介面 |
| `supabase_setup.sql` | 資料表建立 SQL 腳本 |
| `.env` | Supabase 認證資訊 |
| `requirements.txt` | Python 依賴套件 |
| `setup_supabase.sh` | 一鍵設定指南 |
| `healthcheck.py` | 環境檢查工具 |
| `QUICKSTART_SUPABASE.md` | 詳細設定步驟 |

## 🚀 功能特性

### 基本 CRUD
- ✅ **Create** - 新增聯絡人
- ✅ **Read** - 查看清單/搜尋
- ✅ **Update** - 編輯聯絡人
- ✅ **Delete** - 刪除聯絡人

### 高級功能
- 📊 統計分析 (分類統計圖表)
- 🔍 模糊搜尋 (按名稱)
- 🏷️ 分類篩選 (同事/客戶/家人/朋友)
- 📤 CSV 匯出備份
- 📥 CSV 匯入還原
- ☁️ 多裝置雲端同步

## 📚 使用指南

### Web 介面 (推薦)
```bash
streamlit run streamlit_app.py
```

開啟瀏覽器，使用直觀的 UI 進行操作。

### 命令行介面
```bash
python3 contact_manager.py
```

### Python 代碼
```python
from contact_manager import ContactManager

manager = ContactManager()

# 新增
manager.create("張三", "0912345678", email="zhang@example.com")

# 查看
contacts = manager.read()

# 搜尋
results = manager.read_by_name("張")

# 更新
manager.update(contact_id, name="李四")

# 刪除
manager.delete(contact_id)
```

詳見 [QUICKSTART_SUPABASE.md](QUICKSTART_SUPABASE.md)

## 🔐 安全性

- ✅ `.env` 已加入 `.gitignore`
- ⚠️ 不要在程式碼中硬編碼 API Key
- ⚠️ 洩露 Key 時立即到 Supabase 儀表板重新生成
- ✅ Supabase 提供免費 SSL 加密傳輸

## 📡 Supabase 認證信息

```
URL: https://dldbdiqrgqgybswhuabd.supabase.co
Key: sb_publishable_lK4MYxtEBZ_BRxiJz0qRWg_e6bJ4ffY
```

(已保存在 `.env` 檔案中)

## 🆚 vs 舊版本 (JSON 本地存儲)

| 特性 | 舊版本 | 新版本 |
|------|--------|--------|
| 存儲方式 | 本地 JSON 檔案 | Supabase 雲端 |
| 多裝置同步 | ❌ 不支援 | ✅ 實時同步 |
| 資料備份 | 手動複製檔案 | 自動備份 |
| 可擴展性 | 有限 | 無限 |
| 部署難度 | 簡單 | 簡單 (已配置) |
| 費用 | 免費 | 免費額度充足 |

## ⚡ 常見操作

### 刪除所有資料
在 Streamlit UI 的「資料管理」區塊點擊「刪除所有」，或在 SQL 中執行：
```sql
DELETE FROM contacts;
```

### 重置資料表
```sql
DROP TABLE IF EXISTS contacts;
-- 然後重新執行 supabase_setup.sql
```

### 備份資料
```bash
# 在 Streamlit UI 中點擊「匯出 CSV」
# 或通過 Python 代碼
manager.export_to_csv("backup.csv")
```

### 還原資料
```bash
# 在 Streamlit UI 中上傳 CSV
# 或通過 Python 代碼
count = manager.import_from_csv("backup.csv")
print(f"還原 {count} 筆資料")
```

## 🐛 故障排除

### 問題：連接失敗
```
❌ Could not find the table 'public.contacts'
```
**解決**：執行 `bash setup_supabase.sh` 建立資料表

### 問題：API Key 無效
```
❌ 401 Unauthorized
```
**解決**：檢查 `.env` 中的 SUPABASE_KEY 是否正確

### 問題：無法讀取環境變數
```
❌ 請設定 SUPABASE_URL 和 SUPABASE_KEY
```
**解決**：確認 `.env` 存在且格式正確

### 更多幫助
- 📖 詳見 [QUICKSTART_SUPABASE.md](QUICKSTART_SUPABASE.md)
- 🔍 運行 `python3 healthcheck.py` 檢查環境

## 📊 統計資訊

**當前資料庫狀態：** 未建立  
**建議行動：** 執行 `bash setup_supabase.sh`

---

**技術棧**: Python + Streamlit + Supabase + PostgreSQL  
**維護者**: StarPilot  
**更新日期**: 2025-12-21
