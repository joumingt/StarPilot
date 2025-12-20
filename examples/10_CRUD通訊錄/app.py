"""
CRUD 通訊錄 - Flask Web 應用
提供 Web 介面的聯絡人管理系統
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import json
import os
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

DB_FILE = 'contacts.json'


def load_contacts():
    """載入聯絡人資料"""
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []


def save_contacts(contacts):
    """保存聯絡人資料"""
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(contacts, f, ensure_ascii=False, indent=2)


def generate_id():
    """生成唯一 ID"""
    return str(uuid.uuid4())[:8]


@app.route('/')
def index():
    """首頁 - 顯示聯絡人清單"""
    contacts = load_contacts()

    # 取得分類篩選
    category = request.args.get('category')
    if category:
        contacts = [c for c in contacts if c.get('category') == category]

    # 統計分類
    all_contacts = load_contacts()
    categories = {}
    for c in all_contacts:
        cat = c.get('category', '未分類')
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
            contacts = load_contacts()

            # 驗證必填欄位
            name = request.form.get('name', '').strip()
            phone = request.form.get('phone', '').strip()

            if not name or not phone:
                flash('❌ 名稱和電話號碼為必填項目', 'error')
                return redirect(url_for('create'))

            # 檢查電話號碼是否重複
            if any(c['phone'] == phone for c in contacts):
                flash(f'❌ 電話號碼 {phone} 已存在', 'error')
                return redirect(url_for('create'))

            # 新增聯絡人
            contact = {
                'id': generate_id(),
                'name': name,
                'phone': phone,
                'email': request.form.get('email', '').strip(),
                'company': request.form.get('company', '').strip(),
                'category': request.form.get('category', '').strip(),
                'notes': request.form.get('notes', '').strip(),
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }

            contacts.append(contact)
            save_contacts(contacts)

            flash(f'✅ 成功新增 {name} 的聯絡人！', 'success')
            return redirect(url_for('index'))

        except Exception as e:
            flash(f'❌ 錯誤: {str(e)}', 'error')
            return redirect(url_for('create'))

    return render_template('create.html')


@app.route('/view/<contact_id>')
def view(contact_id):
    """檢視聯絡人詳細資訊"""
    contacts = load_contacts()
    contact = next((c for c in contacts if c['id'] == contact_id), None)

    if not contact:
        flash('❌ 找不到該聯絡人', 'error')
        return redirect(url_for('index'))

    return render_template('view.html', contact=contact)


@app.route('/edit/<contact_id>', methods=['GET', 'POST'])
def edit(contact_id):
    """編輯聯絡人"""
    contacts = load_contacts()
    contact = next((c for c in contacts if c['id'] == contact_id), None)

    if not contact:
        flash('❌ 找不到該聯絡人', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        try:
            # 更新欄位
            contact['name'] = request.form.get('name', contact['name']).strip()
            contact['phone'] = request.form.get(
                'phone', contact['phone']).strip()
            contact['email'] = request.form.get('email', '').strip()
            contact['company'] = request.form.get('company', '').strip()
            contact['category'] = request.form.get('category', '').strip()
            contact['notes'] = request.form.get('notes', '').strip()
            contact['updated_at'] = datetime.now().isoformat()

            save_contacts(contacts)
            flash(f'✅ 成功更新 {contact["name"]} 的資訊！', 'success')
            return redirect(url_for('view', contact_id=contact_id))

        except Exception as e:
            flash(f'❌ 錯誤: {str(e)}', 'error')
            return redirect(url_for('edit', contact_id=contact_id))

    return render_template('edit.html', contact=contact)


@app.route('/delete/<contact_id>', methods=['POST'])
def delete(contact_id):
    """刪除聯絡人"""
    try:
        contacts = load_contacts()
        contact = next((c for c in contacts if c['id'] == contact_id), None)

        if not contact:
            flash('❌ 找不到該聯絡人', 'error')
        else:
            contacts = [c for c in contacts if c['id'] != contact_id]
            save_contacts(contacts)
            flash(f'✅ 已刪除 {contact["name"]} 的聯絡人資訊', 'success')

    except Exception as e:
        flash(f'❌ 錯誤: {str(e)}', 'error')

    return redirect(url_for('index'))


@app.route('/search')
def search():
    """搜尋聯絡人"""
    query = request.args.get('q', '').strip()
    contacts = load_contacts()

    if query:
        contacts = [c for c in contacts if query.lower() in c['name'].lower() or
                    query in c['phone']]

    return render_template('search.html', contacts=contacts, query=query)


@app.route('/api/contacts', methods=['GET'])
def api_get_contacts():
    """API: 取得所有聯絡人"""
    contacts = load_contacts()
    category = request.args.get('category')
    if category:
        contacts = [c for c in contacts if c.get('category') == category]
    return jsonify(contacts)


@app.route('/api/contacts/<contact_id>', methods=['GET'])
def api_get_contact(contact_id):
    """API: 取得單筆聯絡人"""
    contacts = load_contacts()
    contact = next((c for c in contacts if c['id'] == contact_id), None)
    if not contact:
        return jsonify({'error': '找不到聯絡人'}), 404
    return jsonify(contact)


@app.route('/api/contacts', methods=['POST'])
def api_create_contact():
    """API: 新增聯絡人"""
    try:
        data = request.get_json()
        contacts = load_contacts()

        # 驗證
        if not data.get('name') or not data.get('phone'):
            return jsonify({'error': '名稱和電話為必填'}), 400

        if any(c['phone'] == data['phone'] for c in contacts):
            return jsonify({'error': '電話號碼已存在'}), 400

        # 新增
        contact = {
            'id': generate_id(),
            'name': data.get('name', ''),
            'phone': data.get('phone', ''),
            'email': data.get('email', ''),
            'company': data.get('company', ''),
            'category': data.get('category', ''),
            'notes': data.get('notes', ''),
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }

        contacts.append(contact)
        save_contacts(contacts)

        return jsonify(contact), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/contacts/<contact_id>', methods=['PUT'])
def api_update_contact(contact_id):
    """API: 更新聯絡人"""
    try:
        data = request.get_json()
        contacts = load_contacts()

        contact = next((c for c in contacts if c['id'] == contact_id), None)
        if not contact:
            return jsonify({'error': '找不到聯絡人'}), 404

        # 更新欄位
        for key in ['name', 'phone', 'email', 'company', 'category', 'notes']:
            if key in data:
                contact[key] = data[key]

        contact['updated_at'] = datetime.now().isoformat()
        save_contacts(contacts)

        return jsonify(contact)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/contacts/<contact_id>', methods=['DELETE'])
def api_delete_contact(contact_id):
    """API: 刪除聯絡人"""
    try:
        contacts = load_contacts()
        contact = next((c for c in contacts if c['id'] == contact_id), None)

        if not contact:
            return jsonify({'error': '找不到聯絡人'}), 404

        contacts = [c for c in contacts if c['id'] != contact_id]
        save_contacts(contacts)

        return jsonify({'message': '成功刪除'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
