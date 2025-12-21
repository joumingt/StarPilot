"""
簡化測試版 - 驗證基本功能
"""
import streamlit as st
from contact_manager import ContactManager

st.set_page_config(page_title="測試", layout="wide")

st.title("🧪 測試頁面")

try:
    manager = ContactManager()
    st.success("✅ 資料庫連接成功")

    contacts = manager.read()
    st.info(f"📊 目前共有 {len(contacts)} 筆聯絡人")

    if st.button("測試新增"):
        try:
            result = manager.create(
                name="測試",
                phone=f"09{int(st.session_state.get('counter', 0)) % 100000000:08d}",
                email="test@test.com",
                company="Test",
                category="同事",
                notes="測試"
            )
            st.session_state.counter = st.session_state.get('counter', 0) + 1
            st.success(f"✅ 新增成功: {result['name']}")
        except Exception as e:
            st.error(f"❌ {e}")

    if st.button("顯示前 5 筆"):
        for i, c in enumerate(contacts[:5], 1):
            st.write(f"{i}. {c['name']} - {c['phone']}")

except Exception as e:
    st.error(f"❌ 錯誤: {e}")
    import traceback
    st.code(traceback.format_exc())
