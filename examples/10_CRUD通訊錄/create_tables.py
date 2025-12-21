#!/usr/bin/env python3
"""
自動建立 Supabase 資料表
"""

import os
from dotenv import load_dotenv
from supabase import create_client

# 載入環境變數
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ 缺少 SUPABASE_URL 或 SUPABASE_KEY")
    exit(1)

# 建立 Supabase 客戶端
client = create_client(SUPABASE_URL, SUPABASE_KEY)

print("🚀 開始建立 Supabase 資料表...")
print(f"   URL: {SUPABASE_URL}")
print()

# SQL 命令
sql_commands = [
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

try:
    # 執行每個 SQL 命令
    for i, sql in enumerate(sql_commands, 1):
        print(f"⏳ 執行命令 {i}/{len(sql_commands)}...")

        # 使用 Supabase 的 rpc 方法執行 SQL
        response = client.rpc('execute_sql', {'sql': sql}).execute()
        print(f"   ✅ 成功")

    print()
    print("="*50)
    print("✅ 資料表建立成功！")
    print("="*50)
    print()
    print("現在可以運行應用了：")
    print("  $ streamlit run streamlit_app.py")
    print()

except Exception as e:
    error_msg = str(e)

    # 嘗試替代方法：直接測試資料表是否存在
    print(f"⚠️  使用 RPC 方法失敗，嘗試替代方法...")
    print()

    try:
        # 嘗試讀取資料表（這會測試資料表是否存在）
        response = client.table("contacts").select("id").limit(1).execute()
        print("✅ 資料表已存在！")
        print()
        print("="*50)
        print("✅ Supabase 連接成功！")
        print("="*50)
        print()
        print("現在可以運行應用了：")
        print("  $ streamlit run streamlit_app.py")
        print()

    except Exception as e2:
        if "Could not find the table" in str(e2):
            print("❌ 資料表不存在")
            print()
            print("這是因為需要用 Service Role Key（管理員密鑰）來建立資料表")
            print()
            print("請手動在 Supabase 建立：")
            print()
            print("1. 登入: https://supabase.com")
            print("2. 進入專案: https://dldbdiqrgqgybswhuabd.supabase.co")
            print("3. SQL Editor → + New Query")
            print("4. 複製以下 SQL:")
            print()
            print("-" * 50)
            for sql in sql_commands:
                print(sql)
            print("-" * 50)
            print()
            print("5. 執行 (Ctrl+Enter)")
            print()
        else:
            print(f"❌ 錯誤: {str(e2)}")
