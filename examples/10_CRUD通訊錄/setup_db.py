#!/usr/bin/env python3
"""
使用 Supabase REST API 建立資料表
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print("🚀 開始建立 Supabase 資料表...")
print(f"   URL: {SUPABASE_URL}")
print()

# SQL 命令
SQL_COMMANDS = [
    'CREATE EXTENSION IF NOT EXISTS "uuid-ossp";',
    """CREATE TABLE IF NOT EXISTS contacts (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name VARCHAR(100) NOT NULL,
  phone VARCHAR(20) NOT NULL UNIQUE,
  email VARCHAR(100),
  company VARCHAR(100),
  category VARCHAR(50),
  notes TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);""",
    "CREATE INDEX IF NOT EXISTS contacts_name_idx ON contacts (name);",
    "CREATE INDEX IF NOT EXISTS contacts_phone_idx ON contacts (phone);",
    "CREATE INDEX IF NOT EXISTS contacts_category_idx ON contacts (category);"
]


def execute_sql(sql):
    """使用 Supabase REST API 執行 SQL"""
    url = f"{SUPABASE_URL}/rest/v1/rpc/execute_sql"

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }

    payload = {"sql": sql}

    try:
        response = requests.post(
            url, json=payload, headers=headers, timeout=10)
        return response.status_code, response.text
    except Exception as e:
        return None, str(e)


def create_tables_via_api():
    """透過 API 建立資料表"""

    # 首先試試能否連接
    print("⏳ 測試連接...")
    try:
        test_url = f"{SUPABASE_URL}/rest/v1/"
        headers = {"apikey": SUPABASE_KEY}
        response = requests.get(test_url, headers=headers, timeout=5)
        if response.status_code in [200, 404]:
            print("✅ 連接成功")
        else:
            print(f"⚠️  連接狀態: {response.status_code}")
    except Exception as e:
        print(f"❌ 連接失敗: {str(e)}")
        return False

    print()

    # 執行 SQL 命令
    success_count = 0
    for i, sql in enumerate(SQL_COMMANDS, 1):
        print(f"⏳ 執行命令 {i}/{len(SQL_COMMANDS)}...")
        status, response = execute_sql(sql)

        if status is None:
            print(f"   ❌ 錯誤: {response}")
        elif status in [200, 201]:
            print(f"   ✅ 成功")
            success_count += 1
        else:
            # 嘗試解析錯誤信息
            try:
                error_data = json.loads(response)
                if "already exists" in str(error_data):
                    print(f"   ℹ️  已存在 (跳過)")
                    success_count += 1
                else:
                    print(f"   ⚠️  狀態 {status}: {error_data}")
            except:
                print(f"   ⚠️  狀態 {status}")

    print()
    print("="*60)
    if success_count > 0:
        print(f"✅ 資料表建立完成！({success_count}/{len(SQL_COMMANDS)})")
        print("="*60)
        print()
        print("🎉 現在可以運行應用了：")
        print("  $ streamlit run streamlit_app.py")
        print()
        return True
    else:
        print("❌ 建立失敗，請檢查認証資訊")
        print("="*60)
        return False


if __name__ == "__main__":
    success = create_tables_via_api()
    exit(0 if success else 1)
