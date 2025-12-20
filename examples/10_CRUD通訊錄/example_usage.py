"""
CRUD 通訊錄 - 使用範例
演示如何使用 ContactManager 類別進行各種操作
"""

from contact_manager import ContactManager

# 初始化聯絡人管理器
manager = ContactManager("demo_contacts.json")

print("=" * 60)
print("📇 CRUD 通訊錄管理系統 - 使用範例")
print("=" * 60)

# ========== CREATE（新增）==========
print("\n1️⃣  CREATE - 新增聯絡人\n")

# 新增第一個聯絡人
contact1 = manager.create(
    name="王小明",
    phone="0912-345-678",
    email="xiaoming.wang@example.com",
    company="美好科技",
    category="同事",
    notes="每週三開會"
)
print(f"✅ 新增成功：{contact1['name']} (ID: {contact1['id']})")

# 新增第二個聯絡人
contact2 = manager.create(
    name="李美華",
    phone="0923-456-789",
    email="meihua.li@example.com",
    company="創新工坊",
    category="客戶",
    notes="大客戶優先處理"
)
print(f"✅ 新增成功：{contact2['name']} (ID: {contact2['id']})")

# 新增第三個聯絡人
contact3 = manager.create(
    name="張大偉",
    phone="0934-567-890",
    email="dawei.zhang@example.com",
    company="美好科技",
    category="同事",
    notes="同部門"
)
print(f"✅ 新增成功：{contact3['name']} (ID: {contact3['id']})")

# ========== READ（讀取）==========
print("\n" + "=" * 60)
print("2️⃣  READ - 查看聯絡人\n")

# 讀取所有聯絡人
all_contacts = manager.read()
print(f"📋 所有聯絡人（共 {len(all_contacts)} 人）：\n")
for i, c in enumerate(all_contacts, 1):
    print(f"{i}. {c['name']} | {c['phone']} | {c['company']} | {c['category']}")

# 讀取特定聯絡人
print(f"\n查看詳細資訊 (ID: {contact1['id']})：")
contact_detail = manager.read(contact1['id'])
print(f"  姓名：{contact_detail['name']}")
print(f"  電話：{contact_detail['phone']}")
print(f"  信箱：{contact_detail['email']}")
print(f"  公司：{contact_detail['company']}")
print(f"  分類：{contact_detail['category']}")
print(f"  備註：{contact_detail['notes']}")

# 按名稱搜尋
print(f"\n搜尋名稱中含有「王」的聯絡人：")
search_results = manager.read_by_name("王")
for c in search_results:
    print(f"  • {c['name']} - {c['phone']}")

# 按分類篩選
print(f"\n篩選分類為「同事」的聯絡人：")
category_results = manager.read_by_category("同事")
for c in category_results:
    print(f"  • {c['name']} ({c['company']})")

# ========== UPDATE（更新）==========
print("\n" + "=" * 60)
print("3️⃣  UPDATE - 修改聯絡人\n")

# 修改聯絡人資訊
updated = manager.update(
    contact1['id'],
    phone="0912-999-999",
    notes="已升職為主任"
)
print(f"✅ 成功更新 {updated['name']} 的資訊")
print(f"  新電話：{updated['phone']}")
print(f"  新備註：{updated['notes']}")

# ========== DELETE（刪除）==========
print("\n" + "=" * 60)
print("4️⃣  DELETE - 刪除聯絡人\n")

# 刪除聯絡人
deleted = manager.delete(contact2['id'])
print(f"✅ 已刪除 {deleted['name']} 的聯絡人資訊")

# 驗證刪除
remaining = manager.read()
print(f"📊 現有聯絡人數：{len(remaining)} 人")

# ========== 進階功能 ==========
print("\n" + "=" * 60)
print("5️⃣  進階功能\n")

# 統計資訊
stats = manager.get_statistics()
print("📊 統計資訊：")
print(f"  總聯絡人數：{stats['total_contacts']}")
print(f"  分類統計：")
for cat, count in stats['categories'].items():
    print(f"    • {cat}：{count} 人")

# 匯出 CSV
print(f"\n💾 匯出聯絡人到 CSV...")
try:
    result = manager.export_to_csv("demo_contacts_export.csv")
    print(f"✅ {result}")
except Exception as e:
    print(f"⚠️  {e}")

# ========== 總結 ==========
print("\n" + "=" * 60)
print("📚 教學總結\n")
print("""
✅ CREATE (新增)  - 新增一位聯絡人
✅ READ (讀取)    - 查看所有聯絡人或搜尋
✅ UPDATE (更新)  - 修改現有聯絡人資訊
✅ DELETE (刪除)  - 刪除一位聯絡人

💡 延伸功能：
   • 按名稱搜尋
   • 按分類篩選
   • 統計分析
   • CSV 匯出匯入
""")
print("=" * 60)
print("\n🎉 範例執行完成！")
print("\n💻 要開始使用，執行以下命令：")
print("   python contact_manager.py")
