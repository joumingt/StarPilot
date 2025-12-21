#!/usr/bin/env python3
"""
使用 PostgreSQL 直接連接建立 Supabase 資料表
"""

import psycopg2
from psycopg2 import sql

# PostgreSQL 連接字符串
CONNECTION_STRING = "postgresql://postgres:fx7SsONmauV08BHr@db.dldbdiqrgqgybswhuabd.supabase.co:5432/postgres"

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


def create_tables():
    """建立資料表"""
    try:
        print("🚀 連接到 PostgreSQL...")
        conn = psycopg2.connect(CONNECTION_STRING)
        cursor = conn.cursor()

        print("✅ 連接成功！")
        print()

        # 執行每個 SQL 命令
        for i, command in enumerate(SQL_COMMANDS, 1):
            print(f"⏳ 執行命令 {i}/{len(SQL_COMMANDS)}...")
            try:
                cursor.execute(command)
                conn.commit()
                print(f"   ✅ 成功")
            except psycopg2.errors.DuplicateObject:
                # 如果物件已存在，忽略錯誤
                conn.rollback()
                print(f"   ℹ️  已存在 (跳過)")
            except Exception as e:
                conn.rollback()
                print(f"   ❌ 錯誤: {str(e)}")

        cursor.close()
        conn.close()

        print()
        print("="*60)
        print("✅ 資料表建立成功！")
        print("="*60)
        print()
        print("現在可以運行應用了：")
        print("  $ streamlit run streamlit_app.py")
        print()

        return True

    except Exception as e:
        print()
        print("❌ 連接失敗")
        print(f"   原因: {str(e)}")
        print()
        print("請檢查：")
        print("  1. 連接字符串是否正確")
        print("  2. 網路是否可以連接到 Supabase")
        print()
        return False


if __name__ == "__main__":
    success = create_tables()
    exit(0 if success else 1)
