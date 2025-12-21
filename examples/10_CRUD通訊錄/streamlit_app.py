"""
CRUD 通訊錄 - Streamlit 簡化版 (Supabase 版本)
"""

import streamlit as st
from contact_manager import ContactManager
from datetime import datetime
import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

st.set_page_config(page_title="📇 通訊錄", layout="wide")

st.title("📇 CRUD 通訊錄管理系統")
st.write("簡單易用的聯絡人管理應用 (Supabase 雲端版)")

# ========== 初始化 ==========


@st.cache_resource
def init_manager():
    return ContactManager()


try:
    manager = init_manager()
except ValueError as e:
    st.error(f"❌ 初始化失敗: {str(e)}")
    st.info("請設定 .env 檔案中的 SUPABASE_URL 和 SUPABASE_KEY")
    st.stop()

# ========== 統計資訊 ==========


@st.cache_data(ttl=10)
def get_stats():
    try:
        contacts = manager.read()
        total = len(contacts)
        categories = {}
        for c in contacts:
            cat = c.get('category', '未分類')
            categories[cat] = categories.get(cat, 0) + 1
        return total, categories
    except:
        return 0, {}


total, categories = get_stats()
col1, col2, col3, col4 = st.columns(4)

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

    try:
        contacts = manager.read()

        if contacts:
            for contact in contacts:
                with st.container(border=True):
                    col1, col2, col3, col4 = st.columns([2, 2, 1, 0.8])
                    with col1:
                        st.write(f"**{contact['name']}** | {contact['phone']}")
                        st.caption(
                            f"{contact['company']} · {contact['category']}")
                    with col2:
                        st.write(f"📧 {contact['email']}")
                        st.caption(
                            f"備註: {contact['notes'][:30] if contact.get('notes') else 'N/A'}")
                    with col3:
                        st.caption(f"ID: {contact['id'][:8]}")
                    with col4:
                        if st.button("✏️", key=f"edit_{contact['id']}", help="編輯"):
                            st.session_state.selected_contact_id = contact['id']
                            st.rerun()
                        if st.button("🗑️", key=f"delete_{contact['id']}", help="刪除"):
                            try:
                                manager.delete(contact['id'])
                                st.success(f"✅ 已刪除 {contact['name']}！")
                                st.cache_data.clear()
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ 刪除失敗: {str(e)}")
        else:
            st.warning("📭 沒有聯絡人，請先新增！")
    except Exception as e:
        st.error(f"❌ 讀取聯絡人失敗: {str(e)}")

# ========== 編輯區域 (在側邊欄彈出) ==========
if 'selected_contact_id' in st.session_state and st.session_state.selected_contact_id:
    try:
        contact = manager.read(st.session_state.selected_contact_id)

        if contact:
            with st.sidebar:
                st.divider()
                st.subheader(f"✏️ 編輯聯絡人")
                st.caption(f"名稱: {contact['name']}")

                with st.form("edit_form", clear_on_submit=False):
                    new_name = st.text_input("👤 名稱", value=contact['name'])
                    new_phone = st.text_input("📱 電話", value=contact['phone'])
                    new_email = st.text_input(
                        "📧 信箱", value=contact.get('email', ''))
                    new_company = st.text_input(
                        "🏢 公司", value=contact.get('company', ''))
                    new_category = st.selectbox("🏷️ 分類", ["同事", "客戶", "家人", "朋友"],
                                                index=["同事", "客戶", "家人", "朋友"].index(contact.get('category', '同事')))
                    new_notes = st.text_area(
                        "📝 備註", value=contact.get('notes', ''))

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.form_submit_button("✅ 更新", use_container_width=True):
                            if not new_name or not new_phone:
                                st.error("❌ 名稱和電話為必填")
                            else:
                                try:
                                    manager.update(
                                        st.session_state.selected_contact_id,
                                        name=new_name,
                                        phone=new_phone,
                                        email=new_email,
                                        company=new_company,
                                        category=new_category,
                                        notes=new_notes
                                    )
                                    st.session_state.selected_contact_id = None
                                    st.cache_data.clear()
                                    st.success(f"✅ 已更新 {new_name}！")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"❌ 更新失敗: {str(e)}")

                    with col2:
                        if st.button("❌ 取消", use_container_width=True, key="cancel_edit"):
                            st.session_state.selected_contact_id = None
                            st.rerun()
    except Exception as e:
        st.error(f"❌ 載入聯絡人失敗: {str(e)}")

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
            else:
                try:
                    manager.create(name, phone, email,
                                   company, category, notes)
                    st.cache_data.clear()
                    st.success(f"✅ 新增 {name} 成功！")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ 新增失敗: {str(e)}")

# ========== Tab 3: 搜尋 ==========
with tab3:
    st.subheader("🔍 搜尋聯絡人")

    search = st.text_input("輸入名稱或電話")

    if search:
        try:
            results = manager.read_by_name(search)

            if results:
                st.info(f"🔍 找到 {len(results)} 筆")
                for contact in results:
                    with st.container(border=True):
                        col1, col2 = st.columns([4, 0.8])
                        with col1:
                            st.write(
                                f"**{contact['name']}** | {contact['phone']}")
                            st.caption(
                                f"{contact['company']} · {contact['category']}")
                        with col2:
                            if st.button("✏️", key=f"search_edit_{contact['id']}", help="編輯"):
                                st.session_state.selected_contact_id = contact['id']
                                st.rerun()
            else:
                st.warning("❌ 找不到")
        except Exception as e:
            st.error(f"❌ 搜尋失敗: {str(e)}")

# ========== Tab 4: 統計 ==========
with tab4:
    st.subheader("📊 統計分析")

    try:
        contacts = manager.read()

        if contacts:
            col1, col2 = st.columns(2)

            with col1:
                st.write("**按分類統計**")
                cat_data = {}
                for c in contacts:
                    cat = c.get('category', '未分類')
                    cat_data[cat] = cat_data.get(cat, 0) + 1
                st.bar_chart(cat_data)

            with col2:
                st.write("**基本統計**")
                st.write(f"- 總人數: {len(contacts)}")
                st.write(
                    f"- 有信箱: {len([c for c in contacts if c.get('email')])}")
                st.write(
                    f"- 有公司: {len([c for c in contacts if c.get('company')])}")
        else:
            st.warning("📭 沒有資料")
    except Exception as e:
        st.error(f"❌ 統計失敗: {str(e)}")

# ========== 側邊欄 ==========
st.sidebar.divider()
st.sidebar.subheader("💾 資料管理")

if st.sidebar.button("🗑️ 刪除所有 (需確認)", use_container_width=True):
    try:
        count = manager.delete_all()
        st.cache_data.clear()
        st.sidebar.success(f"✅ 已清空 {count} 筆聯絡人")
        st.rerun()
    except Exception as e:
        st.sidebar.error(f"❌ 清空失敗: {str(e)}")

st.sidebar.divider()

if st.sidebar.button("🔄 重新整理", use_container_width=True):
    st.cache_data.clear()
    st.rerun()

st.sidebar.divider()
try:
    contact_count = len(manager.read())
    st.sidebar.info(f"📊 共 {contact_count} 位聯絡人")
    st.sidebar.info("☁️ 存儲於 Supabase 雲端")
except:
    st.sidebar.warning("⚠️ 無法連接到 Supabase")
