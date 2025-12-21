#!/usr/bin/env python3
"""
Supabase 通訊錄 - 健康檢查腳本
檢查環境設定、依賴套件和資料庫連接
"""

import sys
import os
from pathlib import Path


def check_python():
    """檢查 Python 版本"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    print(f"❌ Python 版本過低: {version.major}.{version.minor} (需要 3.8+)")
    return False


def check_env_file():
    """檢查 .env 檔案"""
    if not Path(".env").exists():
        print("❌ 找不到 .env 檔案")
        return False

    try:
        with open(".env", "r") as f:
            content = f.read()
            has_url = "SUPABASE_URL" in content
            has_key = "SUPABASE_KEY" in content

        if has_url and has_key:
            print("✅ .env 檔案存在且包含必要變數")
            return True
        else:
            print("❌ .env 缺少必要變數")
            if not has_url:
                print("   - 缺少 SUPABASE_URL")
            if not has_key:
                print("   - 缺少 SUPABASE_KEY")
            return False
    except Exception as e:
        print(f"❌ 無法讀取 .env: {str(e)}")
        return False


def check_requirements():
    """檢查依賴套件"""
    try:
        import streamlit
        print(f"✅ streamlit {streamlit.__version__}")
    except ImportError:
        print("❌ streamlit 未安裝")
        return False

    try:
        import supabase
        print(f"✅ supabase {supabase.__version__}")
    except ImportError:
        print("❌ supabase 未安裝")
        return False

    try:
        import dotenv
        print(f"✅ python-dotenv 已安裝")
    except ImportError:
        print("❌ python-dotenv 未安裝")
        return False

    return True


def check_supabase_connection():
    """檢查 Supabase 連接"""
    try:
        from dotenv import load_dotenv
        load_dotenv()

        from supabase import create_client

        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")

        if not url or not key:
            print("❌ SUPABASE_URL 或 SUPABASE_KEY 未設定")
            return False

        client = create_client(url, key)

        # 嘗試讀取資料
        response = client.table("contacts").select("id").limit(1).execute()
        print(f"✅ Supabase 連接成功")
        print(f"   資料表: contacts")
        print(f"   行數: {len(response.data) if response.data else 0}")
        return True

    except Exception as e:
        print(f"❌ Supabase 連接失敗")
        print(f"   原因: {str(e)}")
        if "Could not find the table" in str(e):
            print("   💡 提示: 請先執行 supabase_setup.sql 建立資料表")
            print("   詳見: QUICKSTART_SUPABASE.md")
        return False


def main():
    """執行所有檢查"""
    print("\n" + "="*50)
    print("📇 Supabase 通訊錄 - 健康檢查")
    print("="*50 + "\n")

    checks = [
        ("Python 環境", check_python),
        ("環境變數", check_env_file),
        ("依賴套件", check_requirements),
        ("Supabase 連接", check_supabase_connection),
    ]

    results = []
    for name, check_func in checks:
        print(f"\n🔍 檢查 {name}...")
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ 檢查出錯: {str(e)}")
            results.append((name, False))

    # 總結
    print("\n" + "="*50)
    print("📊 檢查結果")
    print("="*50)

    all_passed = all(result for _, result in results)

    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")

    print("\n" + "="*50)
    if all_passed:
        print("✅ 所有檢查通過！")
        print("🚀 可以執行: streamlit run streamlit_app.py")
    else:
        print("❌ 有檢查未通過，請修正後重試")
        print("📖 詳見 QUICKSTART_SUPABASE.md")
    print("="*50 + "\n")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
