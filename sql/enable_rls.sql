-- ============================================
-- DARUMA - Row Level Security (RLS) Setup
-- ============================================
-- Run this in Supabase SQL Editor to secure your data
-- This blocks ALL access via anon key - you MUST use service_role key
-- ============================================

-- Step 1: Enable RLS on all tables
ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE price_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE current_prices ENABLE ROW LEVEL SECURITY;
ALTER TABLE fx_rates ENABLE ROW LEVEL SECURITY;
ALTER TABLE current_fx_rates ENABLE ROW LEVEL SECURITY;
ALTER TABLE dividends ENABLE ROW LEVEL SECURITY;
ALTER TABLE portfolio_snapshots ENABLE ROW LEVEL SECURITY;

-- Step 2: Create policies that block anon access
-- Since this is a single-user app, we block all anonymous access
-- The service_role key bypasses RLS, so authenticated backend can still access

-- Transactions
CREATE POLICY "Block anon access to transactions"
ON transactions
FOR ALL
TO anon
USING (false);

-- Price History
CREATE POLICY "Block anon access to price_history"
ON price_history
FOR ALL
TO anon
USING (false);

-- Current Prices
CREATE POLICY "Block anon access to current_prices"
ON current_prices
FOR ALL
TO anon
USING (false);

-- FX Rates
CREATE POLICY "Block anon access to fx_rates"
ON fx_rates
FOR ALL
TO anon
USING (false);

-- Current FX Rates
CREATE POLICY "Block anon access to current_fx_rates"
ON current_fx_rates
FOR ALL
TO anon
USING (false);

-- Dividends
CREATE POLICY "Block anon access to dividends"
ON dividends
FOR ALL
TO anon
USING (false);

-- Portfolio Snapshots
CREATE POLICY "Block anon access to portfolio_snapshots"
ON portfolio_snapshots
FOR ALL
TO anon
USING (false);

-- ============================================
-- VERIFICATION QUERIES
-- ============================================
-- Run these to verify RLS is enabled:

-- Check RLS status on all tables
SELECT 
    schemaname,
    tablename,
    rowsecurity
FROM pg_tables
WHERE schemaname = 'public'
AND tablename IN (
    'transactions', 
    'price_history', 
    'current_prices', 
    'fx_rates', 
    'current_fx_rates', 
    'dividends', 
    'portfolio_snapshots'
);

-- Check policies
SELECT 
    schemaname,
    tablename,
    policyname,
    permissive,
    roles,
    cmd
FROM pg_policies
WHERE schemaname = 'public';

-- ============================================
-- IMPORTANT: After running this script
-- ============================================
-- 1. Go to Supabase Dashboard > Settings > API
-- 2. Copy the "service_role" key (NOT anon key)
-- 3. Update Streamlit Cloud secrets:
--    SUPABASE_KEY = "your-service-role-key"
-- 4. Update GitHub Actions secrets with same key
-- 5. NEVER expose service_role key in frontend code
-- ============================================
