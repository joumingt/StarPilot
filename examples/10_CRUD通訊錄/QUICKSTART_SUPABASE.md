# 🚀 快速開始 - Supabase 通訊錄

## 📋 設定步驟 (只需做一次)

### 步驟 1️⃣: 在 Supabase 建立資料表

1. 登入 [Supabase](https://supabase.com)
2. 進入你的專案：https://dldbdiqrgqgybswhuabd.supabase.co
3. 點擊左邊菜單的 **SQL Editor**
4. 點擊 **+ New Query**
5. 複製 [supabase_setup.sql](supabase_setup.sql) 的全部內容
6. 貼上到查詢編輯器
7. 點擊 **Run** (或按 Ctrl+Enter) 執行

✅ 看到綠色勾號表示成功！

### 步驟 2️⃣: 安裝依賴套件

```bash
cd /workspaces/StarPilot/examples/10_CRUD通訊錄
pip install -r requirements.txt
```

### 步驟 3️⃣: 驗證環境變數

檢查 `.env` 檔案確認已設定正確：

```
SUPABASE_URL=https://dldbdiqrgqgybswhuabd.supabase.co
SUPABASE_KEY=sb_publishable_lK4MYxtEBZ_BRxiJz0qRWg_e6bJ4ffY
```

## ▶️ 運行應用

### 方式 1: 使用 Streamlit (推薦)

```bash
streamlit run streamlit_app.py
```

然後在瀏覽器打開：http://localhost:8501

### 方式 2: 使用命令行

```bash
python3 contact_manager.py
```

## ✨ 功能清單

- ✅ **新增聯絡人** - 名稱、電話、信箱、公司、分類、備註
- ✅ **查看清單** - 所有聯絡人列表
- ✅ **編輯聯絡人** - 更新任何欄位
- ✅ **刪除聯絡人** - 單筆或全部刪除
- ✅ **搜尋功能** - 按名稱模糊查詢
- ✅ **分類篩選** - 按分類顯示
- ✅ **統計分析** - 分類統計圖表
- ✅ **CSV 匯入/匯出** - 數據備份和遷移

## 🧪 測試連接

```bash
python3 << 'EOF'
from contact_manager import ContactManager

try:
    manager = ContactManager()
    contacts = manager.read()
    print(f"✅ 連接成功！共 {len(contacts)} 筆聯絡人")
except Exception as e:
    print(f"❌ 連接失敗: {str(e)}")
EOF
```

## 📚 API 使用範例

```python
from contact_manager import ContactManager

# 初始化
manager = ContactManager()

# 新增聯絡人
contact = manager.create(
    name="張三",
    phone="0912345678",
    email="zhang@example.com",
    company="ABC公司",
    category="同事",
    notes="部門經理"
)
print(f"新增成功，ID: {contact['id']}")

# 查看所有聯絡人
all_contacts = manager.read()
print(f"共 {len(all_contacts)} 位聯絡人")

# 查看單筆
one = manager.read(contact['id'])
print(f"名稱: {one['name']}, 電話: {one['phone']}")

# 按名稱搜尋
results = manager.read_by_name("張")
print(f"找到 {len(results)} 筆符合的聯絡人")

# 按分類篩選
colleagues = manager.read_by_category("同事")
print(f"同事共 {len(colleagues)} 人")

# 更新聯絡人
updated = manager.update(contact['id'], 
    phone="0987654321",
    category="客戶"
)
print(f"更新成功: {updated['name']}")

# 刪除聯絡人
deleted = manager.delete(contact['id'])
print(f"已刪除: {deleted['name']}")

# 取得統計資訊
stats = manager.get_statistics()
print(f"總人數: {stats['total_contacts']}")
print(f"分類統計: {stats['categories']}")

# CSV 匯出
manager.export_to_csv("backup.csv")
print("已匯出到 backup.csv")

# CSV 匯入
count = manager.import_from_csv("backup.csv")
print(f"已匯入 {count} 筆聯絡人")
```

## 🔐 安全提醒

⚠️ **重要**：
- `.env` 檔案包含 API Key，**不要提交到 Git**
- 如果洩露了 Key，立即到 Supabase 儀表板重新生成
- 部署到線上時改用環境變數或密鑰管理服務

## ❓ 常見問題

### Q: 執行 SQL 時出現錯誤？
A: 確認是在正確的 Supabase 專案，並且使用 SQL Editor（不是 Migration Editor）

### Q: 連接失敗顯示 "Could not find the table"？
A: 表示還沒建立資料表，請回到步驟 1 執行 SQL

### Q: 如何清除所有資料？
A: 在 Supabase 的 SQL Editor 執行：`DELETE FROM contacts;`

### Q: 如何備份資料？
A: 使用「匯出 CSV」功能備份，放在安全的地方

### Q: 可以多裝置使用嗎？
A: 可以！Supabase 雲端資料庫支援多裝置實時同步

---

**準備好了嗎？先執行 Supabase SQL，然後 `streamlit run streamlit_app.py` 吧！** 🎉
