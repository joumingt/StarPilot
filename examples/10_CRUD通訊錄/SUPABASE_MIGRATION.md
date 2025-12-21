# 🚀 Supabase 版本遷移指南

已將通訊錄應用改為使用 **Supabase 雲端資料庫**，取代本地 JSON 檔案。

## ✅ 已完成的改寫

### 1. **contact_manager.py** - Supabase 版本
- ✅ 使用 `supabase-py` SDK 連接資料庫
- ✅ 所有 CRUD 操作連接到 Supabase
- ✅ 支援 CSV 匯入匯出
- ✅ 完整的錯誤處理

### 2. **streamlit_app.py** - 雲端版本
- ✅ 整合 ContactManager (Supabase)
- ✅ 移除本地 JSON 檔案操作
- ✅ 新增快取機制加速讀取
- ✅ 新增「重新整理」按鈕

### 3. **資料庫設定**
- ✅ `supabase_setup.sql` - 建立 contacts 資料表的 SQL 命令

### 4. **環境變數設定**
- ✅ `.env` - 你的 Supabase 認證資訊
- ✅ `.env.example` - 環境變數範本

## 🔧 快速開始

### 步驟 1: 在 Supabase 建立資料表

1. 登入 [Supabase](https://supabase.com)
2. 進入 **SQL Editor**
3. 複製 [supabase_setup.sql](supabase_setup.sql) 的內容
4. 執行 SQL 命令建立 `contacts` 資料表

### 步驟 2: 驗證環境變數

檢查 `.env` 檔案是否正確設定：
```
SUPABASE_URL=https://dldbdiqrgqgybswhuabd.supabase.co
SUPABASE_KEY=fx7SsONmauV08BHr
```

### 步驟 3: 安裝依賴包

```bash
pip install -r requirements.txt
```

### 步驟 4: 運行 Streamlit 應用

```bash
streamlit run streamlit_app.py
```

## 📦 新增的依賴包

```
supabase>=2.0.0        # Supabase Python SDK
python-dotenv>=1.0.0   # 環境變數管理
streamlit>=1.30.0      # 原有
```

## 🔐 安全性提醒

⚠️ **重要**: 
- `.env` 檔案包含你的 Supabase API Key
- **不要將 `.env` 提交到版本控制**
- 如果要部署到線上，改用環境變數或密鑰管理服務

建議在 `.gitignore` 中新增：
```
.env
.env.local
```

## 📊 主要功能

- ✅ **新增聯絡人** - 雲端保存
- ✅ **查看清單** - 實時同步
- ✅ **編輯聯絡人** - 即時更新
- ✅ **刪除聯絡人** - 永久移除
- ✅ **搜尋功能** - 模糊查詢
- ✅ **統計分析** - 分類統計
- ✅ **CSV 匯入/匯出** - 數據遷移

## 🛠️ 常見問題

### Q: 如何遷移舊的 JSON 資料到 Supabase？

A: 使用 CSV 匯出功能：
1. 使用舊版本 (JSON) 匯出 CSV
2. 在 Supabase 版本中匯入 CSV

### Q: 如何測試連接？

A: 執行以下 Python 代碼：
```python
from contact_manager import ContactManager

try:
    manager = ContactManager()
    contacts = manager.read()
    print(f"✅ 連接成功，共 {len(contacts)} 筆聯絡人")
except Exception as e:
    print(f"❌ 連接失敗: {str(e)}")
```

### Q: 如何備份資料？

A: 在 Streamlit 中使用「匯出 CSV」功能進行備份

## 📝 API 使用範例

```python
from contact_manager import ContactManager

# 初始化
manager = ContactManager()

# 新增
contact = manager.create(
    name="張三",
    phone="0912345678",
    email="zhang@example.com",
    category="同事"
)

# 查看所有
all_contacts = manager.read()

# 查看單筆
one = manager.read(contact['id'])

# 搜尋
results = manager.read_by_name("張")

# 更新
manager.update(contact['id'], phone="0987654321")

# 刪除
manager.delete(contact['id'])

# 統計
stats = manager.get_statistics()
```

## 🎯 下一步

1. ✅ 完成 Supabase 資料表建立
2. ✅ 安裝依賴包
3. ✅ 驗證 `.env` 設定
4. ✅ 測試應用是否正常運作
5. 📦 (選) 遷移舊資料

---

**版本**: Supabase v2.0.0+  
**更新日期**: 2025-12-21
