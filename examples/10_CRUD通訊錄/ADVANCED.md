# 🚀 CRUD 通訊錄 - 進階篇（資料庫整合）

## 📌 進階功能概述

本文件介紹如何將通訊錄系統升級到使用真正的資料庫，支持：

- ✅ 多人同時使用
- ✅ 更強大的搜尋功能
- ✅ 自動備份
- ✅ 更高的安全性
- ✅ 雲端存取

## 🔧 方案選擇

### 方案 1️⃣: SQLite（推薦入門）

**優點**：
- 🟢 無需另外安裝伺服器
- 🟢 檔案型資料庫，易於備份
- 🟢 支持 Python 原生

**安裝**：
```bash
pip install flask flask-sqlalchemy
```

### 方案 2️⃣: PostgreSQL（推薦專業開發）

**優點**：
- 🟢 功能強大，適合大型應用
- 🟢 支持多人並行存取
- 🟢 提供 Supabase 免費雲端方案

**安裝**：
```bash
pip install flask flask-sqlalchemy psycopg2-binary
```

### 方案 3️⃣: MongoDB（推薦彈性資料結構）

**優點**：
- 🟢 無綱要設計，靈活度高
- 🟢 易於擴展新欄位

**安裝**：
```bash
pip install flask pymongo
```

---

## 💾 使用 SQLite 實現 CRUD

### 第 1 步：安裝 Flask-SQLAlchemy

```bash
pip install flask-sqlalchemy
```

### 第 2 步：建立模型（model）

建立新檔案 `models.py`：

```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Contact(db.Model):
    """聯絡人模型"""
    __tablename__ = 'contacts'
    
    # 欄位定義
    id = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100))
    company = db.Column(db.String(100))
    category = db.Column(db.String(50))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """轉換為字典"""
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'company': self.company,
            'category': self.category,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
```

### 第 3 步：修改 Flask 應用（使用 SQLite）

建立新檔案 `app_sqlite.py`：

```python
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from models import db, Contact
import uuid
from datetime import datetime

app = Flask(__name__)

# 設定資料庫
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your-secret-key'

db.init_app(app)

# 建立資料庫表格
with app.app_context():
    db.create_all()

def generate_id():
    return str(uuid.uuid4())[:8]

@app.route('/')
def index():
    """首頁 - 顯示聯絡人清單"""
    category = request.args.get('category')
    
    query = Contact.query
    if category:
        query = query.filter_by(category=category)
    
    contacts = query.all()
    
    # 統計分類
    all_contacts = Contact.query.all()
    categories = {}
    for c in all_contacts:
        cat = c.category or '未分類'
        categories[cat] = categories.get(cat, 0) + 1
    
    return render_template('index.html',
                          contacts=contacts,
                          categories=categories,
                          selected_category=category,
                          total_contacts=len(all_contacts))

@app.route('/create', methods=['GET', 'POST'])
def create():
    """新增聯絡人"""
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            phone = request.form.get('phone', '').strip()
            
            if not name or not phone:
                flash('❌ 名稱和電話號碼為必填項目', 'error')
                return redirect(url_for('create'))
            
            # 檢查電話是否重複
            if Contact.query.filter_by(phone=phone).first():
                flash(f'❌ 電話號碼 {phone} 已存在', 'error')
                return redirect(url_for('create'))
            
            # 新增聯絡人
            contact = Contact(
                id=generate_id(),
                name=name,
                phone=phone,
                email=request.form.get('email', '').strip(),
                company=request.form.get('company', '').strip(),
                category=request.form.get('category', '').strip(),
                notes=request.form.get('notes', '').strip()
            )
            
            db.session.add(contact)
            db.session.commit()
            
            flash(f'✅ 成功新增 {name} 的聯絡人！', 'success')
            return redirect(url_for('index'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'❌ 錯誤: {str(e)}', 'error')
            return redirect(url_for('create'))
    
    return render_template('create.html')

@app.route('/view/<contact_id>')
def view(contact_id):
    """檢視聯絡人"""
    contact = Contact.query.get(contact_id)
    
    if not contact:
        flash('❌ 找不到該聯絡人', 'error')
        return redirect(url_for('index'))
    
    return render_template('view.html', contact=contact)

@app.route('/edit/<contact_id>', methods=['GET', 'POST'])
def edit(contact_id):
    """編輯聯絡人"""
    contact = Contact.query.get(contact_id)
    
    if not contact:
        flash('❌ 找不到該聯絡人', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        try:
            contact.name = request.form.get('name', contact.name).strip()
            contact.phone = request.form.get('phone', contact.phone).strip()
            contact.email = request.form.get('email', '').strip()
            contact.company = request.form.get('company', '').strip()
            contact.category = request.form.get('category', '').strip()
            contact.notes = request.form.get('notes', '').strip()
            
            db.session.commit()
            flash(f'✅ 成功更新 {contact.name} 的資訊！', 'success')
            return redirect(url_for('view', contact_id=contact_id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'❌ 錯誤: {str(e)}', 'error')
            return redirect(url_for('edit', contact_id=contact_id))
    
    return render_template('edit.html', contact=contact)

@app.route('/delete/<contact_id>', methods=['POST'])
def delete(contact_id):
    """刪除聯絡人"""
    try:
        contact = Contact.query.get(contact_id)
        
        if not contact:
            flash('❌ 找不到該聯絡人', 'error')
        else:
            name = contact.name
            db.session.delete(contact)
            db.session.commit()
            flash(f'✅ 已刪除 {name} 的聯絡人資訊', 'success')
    
    except Exception as e:
        db.session.rollback()
        flash(f'❌ 錯誤: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/search')
def search():
    """搜尋聯絡人"""
    query = request.args.get('q', '').strip()
    contacts = []
    
    if query:
        contacts = Contact.query.filter(
            (Contact.name.ilike(f'%{query}%')) |
            (Contact.phone.like(f'%{query}%'))
        ).all()
    
    return render_template('search.html', contacts=contacts, query=query)

# API 端點
@app.route('/api/contacts', methods=['GET'])
def api_get_contacts():
    """API: 取得所有聯絡人"""
    category = request.args.get('category')
    
    query = Contact.query
    if category:
        query = query.filter_by(category=category)
    
    contacts = query.all()
    return jsonify([c.to_dict() for c in contacts])

@app.route('/api/contacts/<contact_id>', methods=['GET'])
def api_get_contact(contact_id):
    """API: 取得單筆聯絡人"""
    contact = Contact.query.get(contact_id)
    if not contact:
        return jsonify({'error': '找不到聯絡人'}), 404
    return jsonify(contact.to_dict())

@app.route('/api/contacts', methods=['POST'])
def api_create_contact():
    """API: 新增聯絡人"""
    try:
        data = request.get_json()
        
        if not data.get('name') or not data.get('phone'):
            return jsonify({'error': '名稱和電話為必填'}), 400
        
        if Contact.query.filter_by(phone=data['phone']).first():
            return jsonify({'error': '電話號碼已存在'}), 400
        
        contact = Contact(
            id=generate_id(),
            name=data['name'],
            phone=data['phone'],
            email=data.get('email', ''),
            company=data.get('company', ''),
            category=data.get('category', ''),
            notes=data.get('notes', '')
        )
        
        db.session.add(contact)
        db.session.commit()
        
        return jsonify(contact.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/contacts/<contact_id>', methods=['PUT'])
def api_update_contact(contact_id):
    """API: 更新聯絡人"""
    try:
        data = request.get_json()
        contact = Contact.query.get(contact_id)
        
        if not contact:
            return jsonify({'error': '找不到聯絡人'}), 404
        
        for key in ['name', 'phone', 'email', 'company', 'category', 'notes']:
            if key in data:
                setattr(contact, key, data[key])
        
        db.session.commit()
        return jsonify(contact.to_dict())
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/contacts/<contact_id>', methods=['DELETE'])
def api_delete_contact(contact_id):
    """API: 刪除聯絡人"""
    try:
        contact = Contact.query.get(contact_id)
        
        if not contact:
            return jsonify({'error': '找不到聯絡人'}), 404
        
        db.session.delete(contact)
        db.session.commit()
        
        return jsonify({'message': '成功刪除'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### 第 4 步：啟動應用

```bash
python app_sqlite.py
```

然後在瀏覽器開啟 `http://localhost:5000`

---

## ☁️ 整合 Supabase（雲端 PostgreSQL）

### 優勢
- 🌐 資料在雲端，隨時隨地存取
- 📱 支持多人同時使用
- 🔐 自動備份和安全認證
- ✅ 完全免費

### 第 1 步：註冊 Supabase

1. 前往 [supabase.com](https://supabase.com)
2. 使用 GitHub 帳號登入
3. 建立新專案
4. 記錄 `Project URL` 和 `API Key`

### 第 2 步：建立資料表

在 Supabase SQL 編輯器中執行：

```sql
CREATE TABLE contacts (
  id VARCHAR(8) PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  phone VARCHAR(20) UNIQUE NOT NULL,
  email VARCHAR(100),
  company VARCHAR(100),
  category VARCHAR(50),
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_name ON contacts(name);
CREATE INDEX idx_phone ON contacts(phone);
CREATE INDEX idx_category ON contacts(category);
```

### 第 3 步：修改連接字符串

在 `app_sqlite.py` 中修改資料庫 URI：

```python
# 改為 Supabase PostgreSQL
SUPABASE_URL = "postgresql://user:password@db.supabase.co:5432/postgres"
app.config['SQLALCHEMY_DATABASE_URI'] = SUPABASE_URL
```

---

## 🎓 進階 SQL 查詢

### 按分類統計

```python
from sqlalchemy import func

@app.route('/api/statistics')
def statistics():
    """取得統計資訊"""
    stats = db.session.query(
        Contact.category,
        func.count(Contact.id).label('count')
    ).group_by(Contact.category).all()
    
    return jsonify([{
        'category': s[0] or '未分類',
        'count': s[1]
    } for s in stats])
```

### 模糊搜尋

```python
# 搜尋名稱或電話包含關鍵字的聯絡人
results = Contact.query.filter(
    (Contact.name.ilike(f'%{keyword}%')) |
    (Contact.phone.contains(keyword))
).all()
```

### 排序和分頁

```python
# 按建立時間排序，每頁 10 筆
page = request.args.get('page', 1, type=int)
pagination = Contact.query.order_by(
    Contact.created_at.desc()
).paginate(page=page, per_page=10)

contacts = pagination.items
total_pages = pagination.pages
```

---

## 🔒 安全最佳實踐

### 1. 輸入驗證

```python
from wtforms import StringField, validators
from wtforms.validators import Length, Email, Regexp

class ContactForm(FlaskForm):
    name = StringField('Name', [
        validators.Length(min=1, max=100)
    ])
    phone = StringField('Phone', [
        validators.Regexp(r'^\d{10,}$', message='請輸入有效電話')
    ])
    email = StringField('Email', [
        validators.Email(message='請輸入有效信箱')
    ])
```

### 2. SQL 注入防護

```python
# ❌ 不要這樣做（容易被注入）
query = f"SELECT * FROM contacts WHERE name = '{name}'"

# ✅ 用 ORM 自動防護
contacts = Contact.query.filter_by(name=name).all()
```

### 3. API 認證（進階）

```python
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    # 驗證邏輯
    return username == "admin" and password == "secret"

@app.route('/api/contacts', methods=['POST'])
@auth.login_required
def api_create_contact():
    # 只有認證的使用者才能新增
    pass
```

---

## 📊 資料匯入匯出

### 從 CSV 匯入

```python
import csv

@app.route('/import', methods=['POST'])
def import_csv():
    file = request.files['file']
    if file:
        stream = (line.decode('utf-8') for line in file.stream)
        reader = csv.DictReader(stream)
        
        for row in reader:
            contact = Contact(
                id=generate_id(),
                name=row['name'],
                phone=row['phone'],
                email=row.get('email', ''),
                company=row.get('company', ''),
                category=row.get('category', ''),
                notes=row.get('notes', '')
            )
            db.session.add(contact)
        
        db.session.commit()
        flash(f'✅ 成功匯入 {len(list(reader))} 筆聯絡人')
    
    return redirect(url_for('index'))
```

### 匯出為 CSV

```python
from flask import send_file
from io import StringIO

@app.route('/export/csv')
def export_csv():
    contacts = Contact.query.all()
    
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=[
        'id', 'name', 'phone', 'email', 'company', 'category', 'notes'
    ])
    writer.writeheader()
    
    for c in contacts:
        writer.writerow(c.to_dict())
    
    output.seek(0)
    return send_file(
        StringIO(output.getvalue()),
        mimetype='text/csv',
        as_attachment=True,
        download_name='contacts.csv'
    )
```

---

## ✅ 效能最佳化

### 1. 資料庫索引

```python
# 在經常被搜尋的欄位上建立索引
__table_args__ = (
    Index('idx_name', 'name'),
    Index('idx_phone', 'phone'),
    Index('idx_category', 'category'),
)
```

### 2. 查詢優化

```python
# ❌ N+1 查詢問題
for contact in contacts:
    print(contact.category)  # 每次都查詢資料庫

# ✅ 使用 eager loading
from sqlalchemy.orm import joinedload
contacts = Contact.query.joinedload(Contact.category).all()
```

### 3. 快取結果

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/statistics')
@cache.cached(timeout=300)  # 快取 5 分鐘
def statistics():
    # 計算統計資訊
    pass
```

---

## 🚀 部署到雲端

### 部署到 Heroku

1. 安裝 Heroku CLI
2. 建立 `Procfile`：
   ```
   web: gunicorn app:app
   ```
3. 建立 `requirements.txt`：
   ```bash
   pip freeze > requirements.txt
   ```
4. 部署：
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   ```

### 部署到 Render（推薦）

1. 連接 GitHub 倉庫
2. 建立新 Web Service
3. 設定環境變數
4. 自動部署

---

## 📚 進階資源

- [Flask 官方文件](https://flask.palletsprojects.com/)
- [SQLAlchemy 教學](https://docs.sqlalchemy.org/)
- [Supabase 文件](https://supabase.com/docs)
- [RESTful API 設計最佳實踐](https://restfulapi.net/)

---

**準備好升級你的通訊錄系統了嗎？** 🚀
