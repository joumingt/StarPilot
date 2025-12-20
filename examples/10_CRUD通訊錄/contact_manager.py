"""
CRUD 通訊錄管理系統
功能：新增、查看、修改、刪除聯絡人
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class ContactManager:
    """通訊錄管理系統主類"""

    def __init__(self, db_file: str = "contacts.json"):
        """
        初始化通訊錄管理系統

        Args:
            db_file: 資料庫檔案路徑
        """
        self.db_file = db_file
        self.contacts = self._load_contacts()

    def _load_contacts(self) -> List[Dict]:
        """載入聯絡人清單"""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def _save_contacts(self) -> None:
        """保存聯絡人清單"""
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(self.contacts, f, ensure_ascii=False, indent=2)

    def create(self, name: str, phone: str, email: str = "",
               company: str = "", category: str = "", notes: str = "") -> Dict:
        """
        新增聯絡人 (CREATE)

        Args:
            name: 聯絡人名稱（必填）
            phone: 電話號碼（必填）
            email: 電子郵件
            company: 公司名稱
            category: 分類（同事/客戶/家人/朋友）
            notes: 備註

        Returns:
            新增的聯絡人資料
        """
        if not name or not phone:
            raise ValueError("名稱和電話號碼為必填項目")

        # 檢查電話號碼是否已存在
        if any(c['phone'] == phone for c in self.contacts):
            raise ValueError(f"電話號碼 {phone} 已存在")

        contact = {
            'id': self._generate_id(),
            'name': name,
            'phone': phone,
            'email': email,
            'company': company,
            'category': category,
            'notes': notes,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }

        self.contacts.append(contact)
        self._save_contacts()
        return contact

    def read(self, contact_id: Optional[str] = None) -> List[Dict] | Dict:
        """
        查看聯絡人 (READ)

        Args:
            contact_id: 聯絡人 ID（不指定則返回所有聯絡人）

        Returns:
            聯絡人資料或聯絡人清單
        """
        if contact_id:
            for contact in self.contacts:
                if contact['id'] == contact_id:
                    return contact
            raise ValueError(f"找不到 ID 為 {contact_id} 的聯絡人")
        return self.contacts

    def read_by_name(self, name: str) -> List[Dict]:
        """按名稱查詢聯絡人"""
        return [c for c in self.contacts if name in c['name']]

    def read_by_category(self, category: str) -> List[Dict]:
        """按分類查詢聯絡人"""
        return [c for c in self.contacts if c.get('category') == category]

    def update(self, contact_id: str, **kwargs) -> Dict:
        """
        更新聯絡人 (UPDATE)

        Args:
            contact_id: 聯絡人 ID
            **kwargs: 要更新的欄位（name, phone, email, company, category, notes）

        Returns:
            更新後的聯絡人資料
        """
        for contact in self.contacts:
            if contact['id'] == contact_id:
                # 不允許更新 ID 和建立時間
                allowed_fields = {'name', 'phone', 'email',
                                  'company', 'category', 'notes'}
                for key, value in kwargs.items():
                    if key in allowed_fields:
                        contact[key] = value

                contact['updated_at'] = datetime.now().isoformat()
                self._save_contacts()
                return contact

        raise ValueError(f"找不到 ID 為 {contact_id} 的聯絡人")

    def delete(self, contact_id: str) -> Dict:
        """
        刪除聯絡人 (DELETE)

        Args:
            contact_id: 聯絡人 ID

        Returns:
            被刪除的聯絡人資料
        """
        for i, contact in enumerate(self.contacts):
            if contact['id'] == contact_id:
                deleted = self.contacts.pop(i)
                self._save_contacts()
                return deleted

        raise ValueError(f"找不到 ID 為 {contact_id} 的聯絡人")

    def _generate_id(self) -> str:
        """生成唯一的 ID"""
        import uuid
        return str(uuid.uuid4())[:8]

    def export_to_csv(self, filename: str = "contacts_export.csv") -> str:
        """匯出聯絡人為 CSV 檔案"""
        import csv

        if not self.contacts:
            raise ValueError("沒有聯絡人可以匯出")

        fields = ['id', 'name', 'phone', 'email',
                  'company', 'category', 'notes']

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for contact in self.contacts:
                writer.writerow({field: contact.get(field, '')
                                for field in fields})

        return f"已匯出至 {filename}"

    def import_from_csv(self, filename: str) -> int:
        """從 CSV 檔案匯入聯絡人"""
        import csv

        imported_count = 0
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    self.create(
                        name=row['name'],
                        phone=row['phone'],
                        email=row.get('email', ''),
                        company=row.get('company', ''),
                        category=row.get('category', ''),
                        notes=row.get('notes', '')
                    )
                    imported_count += 1
                except ValueError:
                    # 如果已存在則跳過
                    pass

        return imported_count

    def get_statistics(self) -> Dict:
        """取得統計資訊"""
        categories = {}
        for contact in self.contacts:
            cat = contact.get('category', '未分類')
            categories[cat] = categories.get(cat, 0) + 1

        return {
            'total_contacts': len(self.contacts),
            'categories': categories
        }


def main():
    """命令行介面示範"""
    manager = ContactManager("contacts.json")

    while True:
        print("\n" + "="*50)
        print("📇 CRUD 通訊錄管理系統")
        print("="*50)
        print("1️⃣  新增聯絡人 (CREATE)")
        print("2️⃣  查看聯絡人 (READ)")
        print("3️⃣  修改聯絡人 (UPDATE)")
        print("4️⃣  刪除聯絡人 (DELETE)")
        print("5️⃣  按名稱搜尋")
        print("6️⃣  按分類篩選")
        print("7️⃣  查看統計")
        print("8️⃣  匯出為 CSV")
        print("9️⃣  匯入 CSV")
        print("0️⃣  結束")
        print("="*50)

        choice = input("請選擇功能 (0-9): ").strip()

        try:
            if choice == '1':
                # CREATE
                name = input("名稱: ").strip()
                phone = input("電話: ").strip()
                email = input("信箱 (選填): ").strip()
                company = input("公司 (選填): ").strip()
                category = input("分類 (同事/客戶/家人/朋友): ").strip()
                notes = input("備註 (選填): ").strip()

                contact = manager.create(
                    name, phone, email, company, category, notes)
                print(f"✅ 新增成功！ID: {contact['id']}")

            elif choice == '2':
                # READ ALL
                contacts = manager.read()
                if not contacts:
                    print("📭 目前沒有聯絡人")
                else:
                    print(f"\n📋 共 {len(contacts)} 位聯絡人：\n")
                    for i, c in enumerate(contacts, 1):
                        print(
                            f"{i}. {c['name']} | {c['phone']} | {c.get('email', 'N/A')}")

            elif choice == '3':
                # UPDATE
                contact_id = input("請輸入要修改的聯絡人 ID: ").strip()
                print("請輸入要修改的欄位 (留空表示不修改):")
                name = input("新名稱: ").strip()
                phone = input("新電話: ").strip()
                email = input("新信箱: ").strip()
                company = input("新公司: ").strip()
                category = input("新分類: ").strip()
                notes = input("新備註: ").strip()

                update_dict = {}
                if name:
                    update_dict['name'] = name
                if phone:
                    update_dict['phone'] = phone
                if email:
                    update_dict['email'] = email
                if company:
                    update_dict['company'] = company
                if category:
                    update_dict['category'] = category
                if notes:
                    update_dict['notes'] = notes

                contact = manager.update(contact_id, **update_dict)
                print(f"✅ 修改成功！")

            elif choice == '4':
                # DELETE
                contact_id = input("請輸入要刪除的聯絡人 ID: ").strip()
                contact = manager.delete(contact_id)
                print(f"✅ 已刪除 {contact['name']} 的資料")

            elif choice == '5':
                # SEARCH BY NAME
                name = input("搜尋名稱: ").strip()
                results = manager.read_by_name(name)
                if not results:
                    print(f"❌ 找不到包含 '{name}' 的聯絡人")
                else:
                    print(f"\n🔍 找到 {len(results)} 筆結果：\n")
                    for c in results:
                        print(f"ID: {c['id']} | {c['name']} | {c['phone']}")

            elif choice == '6':
                # FILTER BY CATEGORY
                category = input("搜尋分類: ").strip()
                results = manager.read_by_category(category)
                if not results:
                    print(f"❌ 找不到分類為 '{category}' 的聯絡人")
                else:
                    print(f"\n🏷️  分類 '{category}' ({len(results)} 人)：\n")
                    for c in results:
                        print(f"  • {c['name']} - {c['phone']}")

            elif choice == '7':
                # STATISTICS
                stats = manager.get_statistics()
                print(f"\n📊 統計資訊：")
                print(f"  總聯絡人數: {stats['total_contacts']}")
                print(f"  分類統計:")
                for cat, count in stats['categories'].items():
                    print(f"    • {cat}: {count} 人")

            elif choice == '8':
                # EXPORT
                filename = input("匯出檔案名稱 (預設: contacts_export.csv): ").strip()
                if not filename:
                    filename = "contacts_export.csv"
                result = manager.export_to_csv(filename)
                print(f"✅ {result}")

            elif choice == '9':
                # IMPORT
                filename = input("匯入檔案名稱: ").strip()
                count = manager.import_from_csv(filename)
                print(f"✅ 成功匯入 {count} 筆聯絡人")

            elif choice == '0':
                print("👋 再見！")
                break

            else:
                print("❌ 請輸入有效的選項")

        except Exception as e:
            print(f"❌ 錯誤: {str(e)}")


if __name__ == "__main__":
    main()
