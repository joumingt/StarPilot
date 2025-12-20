# 📇 CRUD 通訊錄管理系統 - 快速開始

## 🎯 功能概述

這是一個完整的通訊錄管理系統，實現了 CRUD 的四大操作：

- **C (Create)** - ➕ 新增聯絡人
- **R (Read)** - 👁️ 查看聯絡人清單
- **U (Update)** - ✏️ 修改聯絡人資訊
- **D (Delete)** - 🗑️ 刪除聯絡人

## 📦 包含的檔案

```
contact_manager.py      - 命令行版本（CLI）
app.py                  - Flask Web 應用
templates/              - HTML 模版
  ├── base.html        - 基礎模版
  ├── index.html       - 首頁（聯絡人清單）
  ├── create.html      - 新增聯絡人頁面
  ├── view.html        - 聯絡人詳細資訊
  ├── edit.html        - 編輯聯絡人頁面
  └── search.html      - 搜尋結果頁面
```

## 🚀 快速開始

### 方式 1️⃣: 命令行版本（推薦初學者）

```bash
# 進入專案目錄
cd examples/10_CRUD通訊錄

# 執行命令行應用
python contact_manager.py
```

**功能選單**：
```
1️⃣  新增聯絡人 (CREATE)
2️⃣  查看聯絡人 (READ)
3️⃣  修改聯絡人 (UPDATE)
4️⃣  刪除聯絡人 (DELETE)
5️⃣  按名稱搜尋
6️⃣  按分類篩選
7️⃣  查看統計
8️⃣  匯出為 CSV
9️⃣  匯入 CSV
0️⃣  結束
```

### 方式 2️⃣: Web 應用（功能更豐富）

#### 安裝依賴

```bash
# 進入專案目錄
cd examples/10_CRUD通訊錄

# 安裝 Flask
pip install flask
```

#### 啟動應用

```bash
# 執行 Flask 應用
python app.py
```

然後在瀏覽器中開啟：`http://localhost:5000`

## 📖 使用教學

### 新增聯絡人 (CREATE)

**命令行版本**：
```
選擇 1️⃣  新增聯絡人 (CREATE)
輸入名稱: 王小明
輸入電話: 0912-345-678
輸入信箱 (選填): xiaoming@example.com
輸入公司 (選填): 美好科技
輸入分類 (同事/客戶/家人/朋友): 同事
輸入備註 (選填): 每週三開會
```

**Web 版本**：
1. 點擊「➕ 新增聯絡人」按鈕
2. 填寫必填欄位（名稱、電話）
3. 選填其他欄位
4. 點擊「✅ 確認新增」

### 查看聯絡人 (READ)

**命令行版本**：
```
選擇 2️⃣  查看聯絡人 (READ)
# 顯示所有聯絡人清單
```

**Web 版本**：
- 首頁自動顯示所有聯絡人
- 點擊「👁️ 查看」查看詳細資訊

### 修改聯絡人 (UPDATE)

**命令行版本**：
```
選擇 3️⃣  修改聯絡人 (UPDATE)
輸入要修改的聯絡人 ID: a1b2c3d4
# 逐一輸入要修改的欄位（留空表示不修改）
```

**Web 版本**：
1. 點擊聯絡人卡片的「✏️ 編輯」按鈕
2. 修改相應欄位
3. 點擊「✅ 確認更新」

### 刪除聯絡人 (DELETE)

**命令行版本**：
```
選擇 4️⃣  刪除聯絡人 (DELETE)
輸入要刪除的聯絡人 ID: a1b2c3d4
# 確認刪除（無法復原！）
```

**Web 版本**：
1. 點擊聯絡人卡片的「🗑️ 刪除」按鈕
2. 確認刪除提示
3. 聯絡人已刪除

## 💾 資料存儲

- **資料格式**：JSON （易於備份和轉換）
- **預設檔案**：`contacts.json`
- **位置**：與 Python 檔案同目錄

### 資料結構

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
  "updated_at": "2024-12-20T10:30:45.123456"
}
```

## 🔍 進階功能

### 搜尋功能

**按名稱搜尋**：
- 輸入聯絡人的部分名稱即可搜尋
- 例：輸入「王」可找到所有姓王的聯絡人

**按分類篩選**：
- 快速篩選同事、客戶、家人或朋友
- 分類統計一目瞭然

### 匯出/匯入 CSV

**匯出**：
```bash
選擇 8️⃣  匯出為 CSV
# 將所有聯絡人匯出到 CSV 檔案
```

**匯入**：
```bash
選擇 9️⃣  匯入 CSV
輸入匯入檔案名稱: sample_contacts.csv
# 批量匯入聯絡人資料
```

## 🧩 程式結構

### ContactManager 類別

```python
# 初始化
manager = ContactManager("contacts.json")

# CRUD 操作
contact = manager.create(name, phone, email, company, category, notes)
contacts = manager.read()  # 獲取所有
contact = manager.read(contact_id)  # 獲取單筆
manager.update(contact_id, name=new_name, phone=new_phone)
manager.delete(contact_id)

# 搜尋功能
results = manager.read_by_name("王")
results = manager.read_by_category("同事")

# 資料分析
stats = manager.get_statistics()

# 檔案操作
manager.export_to_csv("contacts.csv")
manager.import_from_csv("contacts.csv")
```

## 🌐 Web API 端點

### 所有聯絡人
- **GET** `/api/contacts` - 獲取所有聯絡人
- **POST** `/api/contacts` - 新增聯絡人

### 單筆聯絡人
- **GET** `/api/contacts/{id}` - 獲取單筆
- **PUT** `/api/contacts/{id}` - 更新聯絡人
- **DELETE** `/api/contacts/{id}` - 刪除聯絡人

### 使用範例

```bash
# 新增聯絡人
curl -X POST http://localhost:5000/api/contacts \
  -H "Content-Type: application/json" \
  -d '{"name":"李美華","phone":"0923-456-789","email":"meihul@example.com"}'

# 查看所有聯絡人
curl http://localhost:5000/api/contacts

# 查看特定聯絡人
curl http://localhost:5000/api/contacts/a1b2c3d4

# 更新聯絡人
curl -X PUT http://localhost:5000/api/contacts/a1b2c3d4 \
  -H "Content-Type: application/json" \
  -d '{"company":"新公司名稱"}'

# 刪除聯絡人
curl -X DELETE http://localhost:5000/api/contacts/a1b2c3d4
```

## 🎨 自訂功能擴展

### 新增欄位
編輯 `contact_manager.py` 的 `create()` 方法，新增欄位：
```python
contact = {
    # ... 現有欄位
    'birthday': request.form.get('birthday', ''),
    'address': request.form.get('address', '')
}
```

### 自訂分類
在表單中修改分類選項：
```html
<option value="同事">同事</option>
<option value="客戶">客戶</option>
<option value="你的分類">你的分類</option>
```

### 集成資料庫
可以將 JSON 替換為：
- SQLite
- PostgreSQL
- MongoDB
- MySQL

## ⚠️ 常見問題

**Q: 資料會不會遺失？**
A: 不會。資料保存在 `contacts.json` 檔案中，除非手動刪除檔案。

**Q: 可以多人共用嗎？**
A: 目前 JSON 版本不支持多人同時修改。建議升級到資料庫版本（詳見進階教學）。

**Q: 如何備份資料？**
A: 直接複製 `contacts.json` 檔案即可備份。

**Q: 刪除後可以復原嗎？**
A: 目前不支持回收站，建議定期備份 JSON 檔案。

## 📚 延伸學習

### 進階版本
- 🔐 新增使用者認證功能
- 💾 整合雲端資料庫 (Supabase, Firebase)
- 📱 建立行動應用版本
- 🔔 新增提醒功能

### 相關技術
- Flask Web 框架
- JSON 資料格式
- RESTful API 設計
- 前端 HTML/CSS/JavaScript

## 🤝 專案貢獻

歡迎提出建議或改進！

---

**祝你編程愉快！** 🚀
