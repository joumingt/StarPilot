-- Supabase SQL 設定
-- 在 Supabase 的 SQL Editor 執行此命令以建立資料表

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

-- 建立索引以加快查詢速度
CREATE INDEX IF NOT EXISTS contacts_name_idx ON contacts (name);
CREATE INDEX IF NOT EXISTS contacts_phone_idx ON contacts (phone);
CREATE INDEX IF NOT EXISTS contacts_category_idx ON contacts (category);

-- 啟用 RLS (Row Level Security) - 選擇性，根據需要
-- ALTER TABLE contacts ENABLE ROW LEVEL SECURITY;
