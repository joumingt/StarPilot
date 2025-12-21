#!/usr/bin/env python3
"""
透過 Supabase SQL API 建立資料表
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL or not SERVICE_ROLE_KEY:
    print("❌ 缺少認證資訊")
    exit(1)

print("🚀 開始建立 Supabase 資料表...")
print(f"   URL: {SUPABASE_URL}")
print()

# 完整的 SQL 指令（一次性執行）
FULL_SQL = """
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS contacts (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name VARCHAR(100) NOT NULL,
  phone VARCHAR(20) NOT NULL UNIQUE,
  email VARCHAR(100),
  company VARCHAR(100),
  category VARCHAR(50),
  notes TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

CREATE INDEX IF NOT EXISTS contacts_name_idx ON contacts (name);
CREATE INDEX IF NOT EXISTS contacts_phone_idx ON contacts (phone);
CREATE INDEX IF NOT EXISTS contacts_category_idx ON contacts (category);
"""


def init_db():
    """透過 SQL 初始化資料庫"""

    # Supabase 提供的 SQL 執行端點
    url = f"{SUPABASE_URL}/rest/v1/rpc/sql"

    headers = {
        "apikey": SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SERVICE_ROLE_KEY}",
        "Content-Type": "application/json"
    }

    payload = {"query": FULL_SQL}

    print("⏳ 發送 SQL 命令到 Supabase...")

    try:
        response = requests.post(
            url, json=payload, headers=headers, timeout=10)

        if response.status_code in [200, 201]:
            print("✅ 成功")
            print()
            print("="*60)
            print("✅ 資料表建立完成！")
            print("="*60)
            return True
        else:
            print(f"⚠️  狀態碼: {response.status_code}")
            try:
                data = response.json()
                print(f"   響應: {data}")
            except:
                print(f"   響應: {response.text}")

            # 嘗試檢查資料表是否已存在
            print()
            print("⏳ 檢查資料表是否已存在...")
            return check_table_exists()

    except Exception as e:
        print(f"❌ 錯誤: {str(e)}")
        return False


def check_table_exists():
    """檢查資料表是否已存在"""
    from supabase import create_client

    try:
        client = create_client(SUPABASE_URL, SERVICE_ROLE_KEY)
        response = client.table("contacts").select("id").limit(1).execute()
        print("✅ 資料表已存在！")
        print()
        print("="*60)
        print("✅ 資料庫已準備就緒")
        print("="*60)
        return True
    except Exception as e:
        print(f"❌ 資料表不存在: {str(e)}")
        return False


if __name__ == "__main__":
    success = init_db()
    if success:
        print()
        print("🎉 現在可以運行應用了：")
        print("  $ streamlit run streamlit_app.py")
        print()
        exit(0)
    else:
        exit(1)
