"""
CRUD 通訊錄 - Streamlit 簡化版
"""

import streamlit as st
import json
import os
from datetime import datetime
import uuid

st.set_page_config(page_title="📇 通訊錄", layout="wide")

st.title("📇 CRUD 通訊錄管理系統")
st.write("簡單易用的聯絡人管理應用")

# ========== 資料庫操作 ==========
DB_FILE = "contacts.json"


def load_contacts():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []


def save_contacts(contacts):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(contacts, f, ensure_ascii=False, indent=2)


def generate_id():
    return str(uuid.uuid4())[:8]


# ========== Session State ==========
if 'contacts' not in st.session_state:
    st.session_state.contacts = load_contacts()
if 'selected_contact_id' not in st.session_state:
    st.session_state.selected_contact_id = None

# ========== 統計資訊 ==========
col1, col2, col3, col4 = st.columns(4)
total = len(st.session_state.contacts)
categories = {}
for c in st.session_state.contacts:
    cat = c.get('category', '未分類')
    categories[cat] = categories.get(cat, 0) + 1

with col1:
    st.metric("📊 總數", total)
with col2:
    st.metric("👥 同事", categories.get('同事', 0))
with col3:
    st.metric("🤝 客戶", categories.get('客戶', 0))
with col4:
    st.metric("👨‍👩‍👧 家人", categories.get('家人', 0))

st.divider()

# ========== 標籤 ==========
tab1, tab2, tab3, tab4 = st.tabs(
    ["📋 清單", "➕ 新增", "🔍 搜尋", "📊 統計"])

# ========== Tab 1: 清單 ==========
with tab1:
    st.subheader("📋 聯絡人清單")

    if st.session_state.contacts:
        for contact in st.session_state.contacts:
            with st.container(border=True):
                col1, col2, col3, col4 = st.columns([2, 2, 1, 0.8])
                with col1:
                    st.write(f"**{contact['name']}** | {contact['phone']}")
                    st.caption(f"{contact['company']} · {contact['category']}")
                with col2:
                    st.write(f"📧 {contact['email']}")
                    st.caption(f"備註: {contact['notes'][:30]}")
                with col3:
                    st.caption(f"ID: {contact['id']}")
                with col4:
                    if st.button("✏️", key=f"edit_{contact['id']}", help="編輯"):
                        st.session_state.selected_contact_id = contact['id']
                    if st.button("🗑️", key=f"delete_{contact['id']}", help="刪除"):
                        st.session_state.contacts = [
                            c for c in st.session_state.contacts if c['id'] != contact['id']]
                        save_contacts(st.session_state.contacts)
                        st.success(f"✅ 已刪除 {contact['name']}！")
                        st.rerun()
    else:
        st.warning("📭 沒有聯絡人，請先新增！")

# ========== 編輯區域 (如果選中聯絡人) ==========
if st.session_state.selected_contact_id:
    contact = next(
        (c for c in st.session_state.contacts if c['id'] == st.session_state.selected_contact_id), None)
    if contact:
        st.divider()
        st.subheader(f"✏️ 編輯 - {contact['name']}")

        col_dummy, col_cancel = st.columns([4, 1])
        with col_cancel:
            if st.button("❌ 取消", use_container_width=True, key="cancel_edit"):
                st.session_state.selected_contact_id = None
                st.rerun()

        with st.form("edit_form"):
            new_name = st.text_input("👤 名稱", value=contact['name'])
            new_phone = st.text_input("📱 電話", value=contact['phone'])
            new_email = st.text_input("📧 信箱", value=contact['email'])
            new_company = st.text_input("🏢 公司", value=contact['company'])
            new_category = st.selectbox("🏷️ 分類", ["同事", "客戶", "家人", "朋友"],
                                        index=["同事", "客戶", "家人", "朋友"].index(contact['category']))
            new_notes = st.text_area("📝 備註", value=contact['notes'])

            if st.form_submit_button("✅ 更新", use_container_width=True):
                if not new_name or not new_phone:
                    st.error("❌ 名稱和電話為必填")
                elif new_phone != contact['phone'] and any(c['phone'] == new_phone for c in st.session_state.contacts if c['id'] != contact['id']):
                    st.error(f"❌ 電話 {new_phone} 已被使用")
                else:
                    contact['name'] = new_name
                    contact['phone'] = new_phone
                    contact['email'] = new_email
                    contact['company'] = new_company
                    contact['category'] = new_category
                    contact['notes'] = new_notes
                    contact['updated_at'] = datetime.now().isoformat()
                    save_contacts(st.session_state.contacts)
                    st.session_state.selected_contact_id = None
                    st.success(f"✅ 已更新 {new_name}！")
                    st.rerun()

# ========== Tab 2: 新增 ==========
with tab2:
    st.subheader("➕ 新增聯絡人")

    with st.form("add_form"):
        name = st.text_input("👤 名稱 *")
        phone = st.text_input("📱 電話 *")
        email = st.text_input("📧 信箱")
        company = st.text_input("🏢 公司")
        category = st.selectbox("🏷️ 分類", ["同事", "客戶", "家人", "朋友"])
        notes = st.text_area("📝 備註")

        if st.form_submit_button("✅ 新增"):
            if not name or not phone:
                st.error("❌ 名稱和電話為必填")
            elif any(c['phone'] == phone for c in st.session_state.contacts):
                st.error(f"❌ 電話 {phone} 已存在")
            else:
                contact = {
                    'id': generate_id(),
                    'name': name,
                    'phone': phone,
                    'email': email,
                    'company': company,
                    'category': category,
                    'notes': notes,
                    'created_at': datetime.now().isoformat(),
                    'updated_at': datetime.now().isoformat()
                }
                st.session_state.contacts.append(contact)
                save_contacts(st.session_state.contacts)
                st.success(f"✅ 新增 {name} 成功！")
                st.balloons()

# ========== Tab 3: 搜尋 ==========
with tab3:
    st.subheader("🔍 搜尋聯絡人")

    search = st.text_input("輸入名稱或電話")

    if search:
        results = [c for c in st.session_state.contacts
                   if search.lower() in c['name'].lower() or search in c['phone']]

        if results:
            st.info(f"🔍 找到 {len(results)} 筆")
            for contact in results:
                with st.container(border=True):
                    col1, col2 = st.columns([4, 0.8])
                    with col1:
                        st.write(f"**{contact['name']}** | {contact['phone']}")
                        st.caption(
                            f"{contact['company']} · {contact['category']}")
                    with col2:
                        if st.button("✏️", key=f"search_edit_{contact['id']}", help="編輯"):
                            st.session_state.selected_contact_id = contact['id']
        else:
            st.warning("❌ 找不到")

# ========== Tab 4: 統計 ==========
with tab4:
    st.subheader("📊 統計分析")

    if st.session_state.contacts:
        col1, col2 = st.columns(2)

        with col1:
            st.write("**按分類統計**")
            cat_data = {}
            for c in st.session_state.contacts:
                cat = c.get('category', '未分類')
                cat_data[cat] = cat_data.get(cat, 0) + 1
            st.bar_chart(cat_data)

        with col2:
            st.write("**基本統計**")
            st.write(f"- 總人數: {len(st.session_state.contacts)}")
            st.write(
                f"- 有信箱: {len([c for c in st.session_state.contacts if c['email']])}")
            st.write(
                f"- 有公司: {len([c for c in st.session_state.contacts if c['company']])}")
    else:
        st.warning("📭 沒有資料")

# ========== 側邊欄 ==========
st.sidebar.divider()
st.sidebar.subheader("💾 資料管理")

if st.sidebar.button("🗑️ 刪除所有 (需確認)", use_container_width=True):
    st.session_state.contacts = []
    save_contacts([])
    st.sidebar.success("✅ 已清空")
    st.rerun()

st.sidebar.divider()
st.sidebar.info(f"📊 共 {len(st.session_state.contacts)} 位聯絡人")
st.sidebar.info("💾 存儲於 contacts.json")
