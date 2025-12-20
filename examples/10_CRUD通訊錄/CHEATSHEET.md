# 📇 CRUD 通訊錄快速參考

## 🚀 快速開始（30 秒）

```bash
cd examples/10_CRUD通訊錄

# 方案 1：命令行版本
python contact_manager.py

# 方案 2：Web 版本（需要 Flask）
pip install flask
python app.py
# 瀏覽器開啟: http://localhost:5000
```

---

## 📚 四大 CRUD 操作

### 1️⃣ CREATE（新增）
```python
from contact_manager import ContactManager

manager = ContactManager()
contact = manager.create(
    name="王小明",
    phone="0912-345-678",
    email="xiaoming@example.com",
    company="美好科技",
    category="同事",
    notes="每週三開會"
)
```

### 2️⃣ READ（讀取）
```python
# 查看所有聯絡人
all_contacts = manager.read()

# 查看單筆
contact = manager.read("contact_id")

# 按名稱搜尋
results = manager.read_by_name("王")

# 按分類篩選
results = manager.read_by_category("同事")
```

### 3️⃣ UPDATE（更新）
```python
# 修改資訊
manager.update(
    "contact_id",
    phone="0912-999-999",
    notes="已升職"
)
```

### 4️⃣ DELETE（刪除）
```python
# 刪除聯絡人
manager.delete("contact_id")
```

---

## 🌐 Web 版本路由

| 路由 | 方法 | 功能 |
|------|------|------|
| `/` | GET | 首頁（聯絡人清單） |
| `/create` | GET/POST | 新增聯絡人 |
| `/view/<id>` | GET | 檢視詳細資訊 |
| `/edit/<id>` | GET/POST | 編輯聯絡人 |
| `/delete/<id>` | POST | 刪除聯絡人 |
| `/search` | GET | 搜尋 |
| `/api/contacts` | GET/POST | API（獲取/新增） |
| `/api/contacts/<id>` | GET/PUT/DELETE | API（讀取/更新/刪除） |

---

## 📋 檔案說明

| 檔案 | 說明 |
|------|------|
| `contact_manager.py` | 核心類別 + 命令行介面 |
| `app.py` | Flask Web 應用 |
| `example_usage.py` | CRUD 演示範例 |
| `templates/` | HTML 模版（6 個） |
| `README.md` | 完整文件 |
| `QUICKSTART.md` | 快速開始 |
| `ADVANCED.md` | 資料庫整合教學 |

---

## 🎯 常用命令

```bash
# 執行命令行版本
python contact_manager.py

# 執行 Web 版本
python app.py

# 執行範例
python example_usage.py

# 安裝 Flask
pip install flask

# 安裝所有依賴
pip install -r requirements.txt
```

---

## 💾 資料存儲

**預設位置**：`contacts.json`（同目錄）

**資料格式**：
```json
{
  "id": "a1b2c3d4",
  "name": "王小明",
  "phone": "0912-345-678",
  "email": "xiaoming@example.com",
  "company": "美好科技",
  "category": "同事",
  "notes": "每週三開會",
  "created_at": "2024-12-20T10:30:45.123456",
  "updated_at": "2024-12-20T14:20:30.654321"
}
```

---

## 🔍 搜尋和篩選

```python
# 按名稱搜尋（模糊）
results = manager.read_by_name("王")

# 按分類篩選（精確）
results = manager.read_by_category("同事")

# 組合條件（自訂）
results = [c for c in manager.read() 
           if c['category'] == '同事' and 'wang' in c['name'].lower()]
```

---

## 📊 進階功能

```python
# 統計資訊
stats = manager.get_statistics()
# 輸出: {'total_contacts': 10, 'categories': {'同事': 5, '客戶': 3, ...}}

# 匯出 CSV
manager.export_to_csv("contacts.csv")

# 匯入 CSV
manager.import_from_csv("contacts.csv")
```

---

## 🎨 Web 介面特色

- 📱 響應式設計（手機/電腦友善）
- 🎯 直觀的使用者介面
- 🎨 美觀的卡片式佈局
- 🏷️ 彩色分類徽章
- 🔍 即時搜尋
- ⚡ 快速操作按鈕

---

## ⚠️ 注意事項

| 項目 | 說明 |
|------|------|
| 電話重複 | ❌ 不允許 |
| 刪除復原 | ❌ 無法復原 |
| 多人同時使用 | ❌ JSON 版本不支持 |
| 資料備份 | ✅ 複製 contacts.json |

---

## 🚀 升級方案

### SQLite（推薦）
```bash
pip install flask-sqlalchemy
python app_sqlite.py
```

### PostgreSQL (Supabase)
```bash
# 詳見 ADVANCED.md
```

---

## 📞 快速幫助

**Q: 找不到 contacts.json？**
A: 執行一次應用後會自動建立

**Q: 如何修改電話號碼？**
A: 點擊「✏️ 編輯」進行修改

**Q: 可以匯入大量聯絡人嗎？**
A: 是，使用 `manager.import_from_csv()` 或命令行選項 9

**Q: 支持哪些分類？**
A: 同事、客戶、家人、朋友（可自訂新增）

---

## 🎓 學習資源

1. [README.md](README.md) - 完整說明
2. [QUICKSTART.md](QUICKSTART.md) - 詳細教學
3. [ADVANCED.md](ADVANCED.md) - 進階主題
4. [example_usage.py](example_usage.py) - 程式碼範例

---

**準備好開始了嗎？** 🚀

執行：`python contact_manager.py`
