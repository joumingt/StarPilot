#!/usr/bin/env python3
"""
建立 100 筆假資料測試
"""

import os
from dotenv import load_dotenv
from contact_manager import ContactManager
import random

load_dotenv()

# 假資料池
FIRST_NAMES = ["張", "李", "王", "劉", "陳", "楊", "黃", "吳", "周", "許",
               "郭", "何", "高", "林", "鄭", "謝", "馬", "朱", "熊", "蔣"]

LAST_NAMES = ["三", "四", "五", "偉", "明", "華", "麗", "芳", "娜", "靜",
              "慧", "欣", "雨", "琪", "曼", "瑩", "紅", "杰", "偉", "忠"]

COMPANIES = ["ABC公司", "XYZ集團", "科技有限公司", "製造工業", "服務顧問",
             "軟體開發", "金融投資", "房地產", "醫療健康", "教育訓練"]

CATEGORIES = ["同事", "客戶", "家人", "朋友"]


def generate_phone():
    """生成隨機電話號碼"""
    return f"09{random.randint(10000000, 99999999)}"


def generate_email(name):
    """生成隨機電子郵件"""
    domains = ["gmail.com", "yahoo.com",
               "outlook.com", "company.com", "mail.tw"]
    return f"{name.lower()}@{random.choice(domains)}"


def generate_contact():
    """生成隨機聯絡人"""
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    name = first + last

    return {
        "name": name,
        "phone": generate_phone(),
        "email": generate_email(name),
        "company": random.choice(COMPANIES),
        "category": random.choice(CATEGORIES),
        "notes": f"隨機生成的測試資料"
    }


def main():
    print("🚀 開始建立 100 筆假資料...")
    print()

    try:
        manager = ContactManager()

        success_count = 0
        failed_count = 0

        for i in range(1, 101):
            try:
                contact = generate_contact()
                manager.create(
                    name=contact["name"],
                    phone=contact["phone"],
                    email=contact["email"],
                    company=contact["company"],
                    category=contact["category"],
                    notes=contact["notes"]
                )
                success_count += 1

                # 每 10 筆顯示一次進度
                if i % 10 == 0:
                    print(f"✅ 已建立 {i} 筆")

            except Exception as e:
                failed_count += 1
                if "already exists" in str(e):
                    # 如果電話號碼已存在，重試
                    pass
                else:
                    print(f"   ⚠️  {i} 號失敗: {str(e)}")

        print()
        print("="*60)
        print(f"✅ 建立完成！")
        print(f"   成功: {success_count} 筆")
        print(f"   失敗: {failed_count} 筆")
        print("="*60)
        print()

        # 驗證
        print("📊 驗證資料...")
        all_contacts = manager.read()
        print(f"   資料表中共有 {len(all_contacts)} 筆聯絡人")

        # 統計資訊
        stats = manager.get_statistics()
        print(f"   總人數: {stats['total_contacts']}")
        print(f"   分類統計:")
        for cat, count in stats['categories'].items():
            print(f"     • {cat}: {count} 人")

        print()
        print("🎉 資料已準備就緒，可以開始教學了！")

    except Exception as e:
        print(f"❌ 錯誤: {str(e)}")
        return False

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
