#!/usr/bin/env python3
"""
使用 Service Role Key 自動建立 Supabase 資料表
"""

import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL or not SERVICE_ROLE_KEY:
    print("❌ 缺少 SUPABASE_URL 或 SUPABASE_SERVICE_KEY")
    exit(1)

print("🚀 開始建立 Supabase 資料表...")
print(f"   URL: {SUPABASE_URL}")
print()

# 使用 Service Role 創建客戶端
admin_client = create_client(SUPABASE_URL, SERVICE_ROLE_KEY)

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
        print("⏳ 測試連接...")
        # 先嘗試讀取以測試連接
        response = admin_client.table(
            "contacts").select("id").limit(1).execute()
        print("✅ 資料表已存在！")
        return True

    except Exception as e:
        error_msg = str(e)

        if "Could not find the table" not in error_msg:
            print(f"❌ 連接錯誤: {error_msg}")
            return False

        print("⏳ 資料表不存在，正在建立...")
        print()

        # 使用 RPC 執行 SQL
        try:
            # 先建立一個 SQL 執行函數（如果不存在）
            create_function_sql = """
            CREATE OR REPLACE FUNCTION public.execute_sql(sql text)
            RETURNS void AS $$
            BEGIN
              EXECUTE sql;
            END;
            $$ LANGUAGE plpgsql;
            """

            # 直接執行 SQL 命令
            for i, sql in enumerate(SQL_COMMANDS, 1):
                print(f"⏳ 執行命令 {i}/{len(SQL_COMMANDS)}...")
                try:
                    # 使用 postgrest 直接執行（需要有合適的 RPC）
                    admin_client.rpc("execute_sql", {"sql": sql}).execute()
                    print(f"   ✅ 成功")
                except Exception as rpc_error:
                    if "execute_sql" in str(rpc_error):
                        # 如果 RPC 不存在，嘗試用 SQL 客戶端
                        print(f"   ⚠️  無法使用 RPC，嘗試其他方式...")
                        break
                    else:
                        print(f"   ⚠️  {str(rpc_error)}")

            # 檢查是否建立成功
            response = admin_client.table(
                "contacts").select("id").limit(1).execute()
            print()
            print("="*60)
            print("✅ 資料表建立成功！")
            print("="*60)
            return True

        except Exception as e:
            print(f"❌ 建立失敗: {str(e)}")
            return False


if __name__ == "__main__":
    success = create_tables()
    if success:
        print()
        print("🎉 現在可以運行應用了：")
        print("  $ streamlit run streamlit_app.py")
        print()
        exit(0)
    else:
        exit(1)
