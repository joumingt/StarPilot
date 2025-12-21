#!/usr/bin/env python3
"""
使用 Supabase 管理 API 建立資料表
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
ADMIN_TOKEN = "sbp_4997925840a9447a06e3d584f0a78a8d919e5fe2"

# 從 URL 中提取項目 ID
# 例如：https://dldbdiqrgqgybswhuabd.supabase.co → dldbdiqrgqgybswhuabd
PROJECT_ID = SUPABASE_URL.split(
    "://")[1].split(".")[0] if SUPABASE_URL else None

print("🚀 開始建立 Supabase 資料表...")
print(f"   URL: {SUPABASE_URL}")
print(f"   Project ID: {PROJECT_ID}")
print()

# SQL 命令（一次性執行）
SQL_SCRIPT = """
-- 啟用 UUID 擴展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 建立 contacts 資料表
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

-- 建立索引
CREATE INDEX IF NOT EXISTS contacts_name_idx ON contacts (name);
CREATE INDEX IF NOT EXISTS contacts_phone_idx ON contacts (phone);
CREATE INDEX IF NOT EXISTS contacts_category_idx ON contacts (category);
"""


def execute_sql():
    """透過管理 API 執行 SQL"""

    url = f"https://api.supabase.com/v1/projects/{PROJECT_ID}/database/query"

    headers = {
        "Authorization": f"Bearer {ADMIN_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "query": SQL_SCRIPT
    }

    print("⏳ 發送 SQL 命令到 Supabase...")

    try:
        response = requests.post(
            url, json=payload, headers=headers, timeout=15)

        print(f"   狀態碼: {response.status_code}")

        if response.status_code in [200, 201]:
            print("✅ 成功")
            print()
            print("="*60)
            print("✅ 資料表建立完成！")
            print("="*60)
            return True
        else:
            try:
                data = response.json()
                print(
                    f"   響應: {json.dumps(data, indent=2, ensure_ascii=False)}")
            except:
                print(f"   響應: {response.text}")

            # 嘗試檢查資料表是否已存在
            print()
            print("⏳ 檢查資料表是否已存在...")
            return check_table_exists()

    except Exception as e:
        print(f"❌ 錯誤: {str(e)}")
        return check_table_exists()


def check_table_exists():
    """檢查資料表是否已存在"""
    from supabase import create_client

    try:
        client = create_client(SUPABASE_URL, os.getenv("SUPABASE_KEY"))
        response = client.table("contacts").select("id").limit(1).execute()
        print("✅ 資料表已存在！")
        print()
        print("="*60)
        print("✅ 資料庫已準備就緒")
        print("="*60)
        return True
    except Exception as e:
        error_msg = str(e)
        if "Could not find the table" in error_msg:
            print(f"❌ 資料表尚未建立")
        else:
            print(f"⚠️  錯誤: {error_msg}")
        return False


if __name__ == "__main__":
    success = execute_sql()
    if success:
        print()
        print("🎉 現在可以運行應用了：")
        print("  $ streamlit run streamlit_app.py")
        print()
        exit(0)
    else:
        exit(1)
