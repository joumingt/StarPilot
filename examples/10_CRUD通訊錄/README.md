# 📇 CRUD 通訊錄完整解決方案

## 📋 專案概況

這是一個完整的聯絡人管理系統，實現了所有 CRUD 操作（新增、查看、修改、刪除），提供了兩個版本：

### 版本對比

| 功能 | 命令行版 | Web 版 |
|------|---------|-------|
| 新增聯絡人 | ✅ | ✅ |
| 查看清單 | ✅ | ✅ |
| 修改資訊 | ✅ | ✅ |
| 刪除聯絡人 | ✅ | ✅ |
| 搜尋功能 | ✅ | ✅ |
| 分類篩選 | ✅ | ✅ |
| 統計資訊 | ✅ | ✅ |
| 匯出 CSV | ✅ | ⭕ |
| 匯入 CSV | ✅ | ⭕ |
| 視覺化介面 | ❌ | ✅ |
| REST API | ❌ | ✅ |

## 🗂️ 檔案結構

```
10_CRUD通訊錄/
├── contact_manager.py        # 命令行版本（CLI）
├── app.py                    # Flask Web 應用（JSON 版）
├── models.py                 # 資料庫模型（SQLAlchemy）
├── app_sqlite.py             # Flask 應用（SQLite 資料庫）
├── app_supabase.py           # Flask 應用（雲端 PostgreSQL）
│
├── templates/                # HTML 模版
│   ├── base.html            # 基礎模版
│   ├── index.html           # 首頁（聯絡人清單）
│   ├── create.html          # 新增聯絡人
│   ├── view.html            # 檢視詳細資訊
│   ├── edit.html            # 編輯聯絡人
│   └── search.html          # 搜尋結果
│
├── 測試資料/
│   ├── sample_contacts.csv
│   ├── sample_contacts.json
│   └── README.md
│
├── contacts.json             # 預設資料庫（JSON 格式）
├── contacts.db              # SQLite 資料庫檔案
│
├── QUICKSTART.md            # 快速開始指南
├── ADVANCED.md              # 進階教學（資料庫整合）
├── README.md                # 本檔案
└── requirements.txt         # Python 依賴
```

## 🚀 快速開始

### 安裝步驟

```bash
# 進入專案目錄
cd examples/10_CRUD通訊錄

# 安裝依賴
pip install flask          # Web 版本需要
pip install flask-sqlalchemy  # 資料庫版本需要
```

### 執行應用

**方式 1：命令行版本（推薦初學者）**
```bash
python contact_manager.py
```

**方式 2：Web 版本（推薦實際使用）**
```bash
python app.py
# 然後在瀏覽器開啟 http://localhost:5000
```

**方式 3：使用 SQLite 資料庫**
```bash
python app_sqlite.py
```

## 📚 核心功能說明

### 1️⃣ CREATE（新增）

**功能**：新增一位新的聯絡人

**必填欄位**：
- 名稱
- 電話號碼

**選填欄位**：
- 信箱
- 公司名稱
- 分類（同事/客戶/家人/朋友）
- 備註

**驗證規則**：
- 電話號碼不能重複
- 名稱不能為空

**範例**：
```
姓名：王小明
電話：0912-345-678
信箱：xiaoming@example.com
公司：美好科技
分類：同事
備註：每週三開會
```

### 2️⃣ READ（讀取）

**功能**：查看聯絡人資訊

**查詢方式**：
- 查看所有聯絡人清單
- 按 ID 查看單筆詳細資訊
- 按名稱搜尋
- 按分類篩選

**顯示內容**：
- 聯絡人基本資訊
- 新增時間
- 最後修改時間

### 3️⃣ UPDATE（更新）

**功能**：修改現有聯絡人資訊

**可修改欄位**：
- 名稱、電話、信箱、公司、分類、備註

**不可修改**：
- ID（唯一識別碼）
- 建立時間

**自動更新**：
- 最後修改時間（會自動更新）

### 4️⃣ DELETE（刪除）

**功能**：刪除聯絡人資訊

**注意事項**：
- ⚠️ 刪除後無法復原
- 需要確認刪除才能執行

---

## 🎨 Web 介面功能

### 首頁（聯絡人清單）
- 📊 統計卡片（總數、各分類統計）
- 🔍 搜尋欄位
- 📋 聯絡人卡片列表
- 快速動作（查看、編輯、刪除）

### 新增頁面
- 表單驗證
- 可視化欄位
- 分類選擇器

### 詳細頁面
- 完整聯絡人資訊
- 快速撥號連結
- 快速寄信連結
- 編輯和刪除按鈕

### 編輯頁面
- 預填原始資訊
- 分部欄位修改
- 更新時間自動更新

### 搜尋頁面
- 模糊搜尋
- 結果計數
- 快速操作

---

## 💾 資料儲存方案

### JSON 版本（預設）

**優點**：
- 簡單易懂
- 無需安裝資料庫
- 檔案易於備份

**缺點**：
- 不支持並行讀寫
- 搜尋效率低

**檔案位置**：`contacts.json`

**資料結構**：
```json
[
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
]
```

### SQLite 版本（推薦升級）

**優點**：
- 功能強大
- 搜尋高效
- 支持複雜查詢

**缺點**：
- 仍不支持多人並行寫入

**檔案位置**：`contacts.db`

### Supabase 版本（推薦雲端）

**優點**：
- ☁️ 雲端存儲
- 👥 支持多人協作
- 🔐 自動備份
- 🌐 隨時隨地存取

**使用方式**：詳見 [ADVANCED.md](ADVANCED.md)

---

## 🔍 搜尋和篩選

### 搜尋功能
- 按名稱模糊搜尋
- 按電話號碼搜尋
- 即時搜尋結果

**範例**：
```
搜尋「王」可找到：王小明、王美玲...
搜尋「0912」可找到所有該電話開頭的聯絡人
```

### 篩選功能
- 按分類篩選（同事/客戶/家人/朋友）
- 篩選後顯示統計資訊
- 一鍵清除篩選

---

## 📊 統計和分析

### 顯示的統計資訊

**首頁統計卡片**：
- 總聯絡人數
- 各分類的人數
- 視覺化展示

**API 端點**：
- `GET /api/statistics` - 取得統計資訊

---

## 🌐 REST API 參考

### 端點列表

| 方法 | 端點 | 說明 |
|------|------|------|
| GET | `/api/contacts` | 獲取所有聯絡人 |
| POST | `/api/contacts` | 新增聯絡人 |
| GET | `/api/contacts/<id>` | 獲取單筆聯絡人 |
| PUT | `/api/contacts/<id>` | 更新聯絡人 |
| DELETE | `/api/contacts/<id>` | 刪除聯絡人 |

### 使用範例

**新增聯絡人**：
```bash
curl -X POST http://localhost:5000/api/contacts \
  -H "Content-Type: application/json" \
  -d '{
    "name": "李美華",
    "phone": "0923-456-789",
    "email": "meih@example.com",
    "company": "創新工坊",
    "category": "客戶",
    "notes": "大客戶優先"
  }'
```

**查詢所有聯絡人**：
```bash
curl http://localhost:5000/api/contacts
```

**查詢特定聯絡人**：
```bash
curl http://localhost:5000/api/contacts/a1b2c3d4
```

**更新聯絡人**：
```bash
curl -X PUT http://localhost:5000/api/contacts/a1b2c3d4 \
  -H "Content-Type: application/json" \
  -d '{"company": "新公司名稱"}'
```

**刪除聯絡人**：
```bash
curl -X DELETE http://localhost:5000/api/contacts/a1b2c3d4
```

---

## 🛠️ 自訂和擴展

### 新增自訂欄位

**步驟 1**：修改模型
```python
# 在 models.py 或 contact_manager.py 中新增欄位
phone = db.Column(db.String(20))
birthday = db.Column(db.Date)  # 新增生日欄位
address = db.Column(db.String(255))  # 新增地址欄位
```

**步驟 2**：更新表單
```html
<!-- 在 create.html 和 edit.html 中新增欄位 -->
<div class="form-group">
  <label for="birthday">生日</label>
  <input type="date" id="birthday" name="birthday">
</div>
```

**步驟 3**：更新 API
```python
# 在 create() 和 update() 函數中處理新欄位
birthday = request.form.get('birthday')
```

### 新增分類

編輯 HTML 表單中的分類選項：
```html
<select id="category" name="category">
  <option value="">-- 選擇分類 --</option>
  <option value="同事">同事</option>
  <option value="客戶">客戶</option>
  <option value="家人">家人</option>
  <option value="朋友">朋友</option>
  <option value="供應商">供應商</option>  <!-- 新增 -->
  <option value="競爭對手">競爭對手</option>  <!-- 新增 -->
</select>
```

### 修改視覺樣式

編輯 `templates/base.html` 中的 CSS 樣式：
```css
:root {
  --primary: #007bff;        /* 主色調 */
  --success: #28a745;        /* 成功色 */
  --danger: #dc3545;         /* 危險色 */
}
```

---

## ⚠️ 常見問題 (FAQ)

### Q1: 資料存在哪裡？
**A**: 預設儲存在 `contacts.json` 檔案中，與 Python 檔案同一目錄。

### Q2: 可以多人同時使用嗎？
**A**: JSON 版本不支持，建議升級到 SQLite 或 Supabase。

### Q3: 刪除的資料可以復原嗎？
**A**: 不可以。請定期備份 `contacts.json` 檔案。

### Q4: 如何備份資料？
**A**: 直接複製 `contacts.json` 或 `contacts.db` 檔案即可。

### Q5: 可以在手機上使用嗎？
**A**: Web 版本支持所有設備（響應式設計），Supabase 版本可隨時隨地存取。

### Q6: 如何修改資料庫位置？
**A**: 在 `app.py` 或 `contact_manager.py` 中修改 `DB_FILE` 變數。

### Q7: 如何隱藏某些欄位？
**A**: 在 HTML 模版中使用 `{% if %}` 條件語句隱藏。

### Q8: 可以新增權限管理嗎？
**A**: 可以，詳見 [ADVANCED.md](ADVANCED.md) 的安全章節。

---

## 📖 學習路線

### 初級（推薦開始）
1. 執行命令行版本 `contact_manager.py`
2. 理解 CRUD 的四個操作
3. 查看 JSON 資料格式

### 中級（Web 開發）
1. 執行 Web 版本 `app.py`
2. 學習 Flask 框架基礎
3. 理解 HTML 表單和路由

### 進階（資料庫）
1. 升級到 SQLite 版本 `app_sqlite.py`
2. 學習 SQL 和 SQLAlchemy ORM
3. 理解資料庫設計和優化

### 專業級（雲端部署）
1. 整合 Supabase PostgreSQL
2. 實現多人協作
3. 部署到雲端平台

---

## 🤝 專案結構和設計模式

### 使用的設計模式
- **MVC 模式**：Model（資料）、View（介面）、Controller（邏輯）
- **REST API**：符合 RESTful 設計原則
- **ORM**：使用 SQLAlchemy 簡化資料庫操作

### 代碼組織
```
app/
├── 模型層 (models.py)     - 資料定義
├── 視圖層 (templates/)    - HTML 頁面
└── 邏輯層 (app.py)        - 業務邏輯和路由
```

---

## 🚀 下一步

1. **測試現有版本** - 執行 `contact_manager.py` 或 `app.py`
2. **自訂欄位** - 新增符合你的需求的欄位
3. **升級資料庫** - 從 JSON 升級到 SQLite 或 Supabase
4. **部署上線** - 將應用部署到 Heroku、Render 等平台
5. **加入更多功能** - 如照片、行事曆提醒等

---

## 📞 支援資源

- [Flask 官方文件](https://flask.palletsprojects.com/)
- [SQLAlchemy 教學](https://docs.sqlalchemy.org/)
- [Supabase 文件](https://supabase.com/docs)
- [Python 官方文件](https://docs.python.org/3/)

---

**祝你的通訊錄系統開發順利！** 🎉
