-- ============================================
-- DARUMA - Investment Portfolio Tracker
-- Database Schema for Supabase (Postgres)
-- ============================================

-- ============================================
-- TABLES
-- ============================================

-- Transactions (manual entry + Delta CSV import)
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    date TIMESTAMPTZ NOT NULL,
    ticker VARCHAR(20) NOT NULL,
    name VARCHAR(100),
    type VARCHAR(20) NOT NULL CHECK (type IN ('BUY', 'SELL')),
    asset_type VARCHAR(20),
    quantity DECIMAL(18,8) NOT NULL,
    price DECIMAL(18,4) NOT NULL,
    total_amount DECIMAL(18,4),
    currency VARCHAR(3) DEFAULT 'USD',
    exchange VARCHAR(100),
    platform VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_transactions_ticker ON transactions(ticker);
CREATE INDEX idx_transactions_date ON transactions(date);
CREATE INDEX idx_transactions_type ON transactions(type);

-- Price history (updated automatically every 4 hours)
CREATE TABLE price_history (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(20) NOT NULL,
    price DECIMAL(18,4) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    recorded_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_price_history_ticker_date ON price_history(ticker, recorded_at);

-- Current prices (latest price per ticker for fast queries)
CREATE TABLE current_prices (
    ticker VARCHAR(20) PRIMARY KEY,
    price DECIMAL(18,4) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- FX rates history
CREATE TABLE fx_rates (
    id SERIAL PRIMARY KEY,
    pair VARCHAR(10) NOT NULL,
    rate DECIMAL(18,6) NOT NULL,
    recorded_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_fx_rates_pair_date ON fx_rates(pair, recorded_at);

-- Current FX rates (latest rate per pair)
CREATE TABLE current_fx_rates (
    pair VARCHAR(10) PRIMARY KEY,
    rate DECIMAL(18,6) NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Dividends (calculated automatically from yfinance)
CREATE TABLE dividends (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(20) NOT NULL,
    payment_date DATE NOT NULL,
    dividend_per_share DECIMAL(18,6) NOT NULL,
    shares_at_date DECIMAL(18,8) NOT NULL,
    total_received DECIMAL(18,4) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    calculated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(ticker, payment_date)
);

CREATE INDEX idx_dividends_ticker ON dividends(ticker);
CREATE INDEX idx_dividends_date ON dividends(payment_date);

-- Portfolio value snapshots (for historical chart)
CREATE TABLE portfolio_snapshots (
    id SERIAL PRIMARY KEY,
    snapshot_date DATE NOT NULL UNIQUE,
    total_value DECIMAL(18,4) NOT NULL,
    total_cost DECIMAL(18,4) NOT NULL,
    recorded_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_portfolio_snapshots_date ON portfolio_snapshots(snapshot_date);

-- ============================================
-- VIEWS
-- ============================================

-- Current holdings with average buy price
CREATE VIEW current_holdings AS
SELECT
    ticker,
    MAX(name) as name,
    MAX(asset_type) as asset_type,
    SUM(CASE
        WHEN type = 'BUY' THEN quantity
        WHEN type = 'SELL' THEN -quantity
        ELSE 0
    END) as shares,
    SUM(CASE
        WHEN type = 'BUY' THEN quantity * price
        WHEN type = 'SELL' THEN -quantity * price
        ELSE 0
    END) as total_cost,
    CASE
        WHEN SUM(CASE WHEN type = 'BUY' THEN quantity ELSE 0 END) > 0
        THEN SUM(CASE WHEN type = 'BUY' THEN quantity * price ELSE 0 END) /
             SUM(CASE WHEN type = 'BUY' THEN quantity ELSE 0 END)
        ELSE 0
    END as avg_buy_price,
    MIN(CASE WHEN type = 'BUY' THEN date END) as first_buy_date,
    MAX(CASE WHEN type = 'BUY' THEN date END) as last_buy_date
FROM transactions
GROUP BY ticker
HAVING SUM(CASE
    WHEN type = 'BUY' THEN quantity
    WHEN type = 'SELL' THEN -quantity
    ELSE 0
END) > 0;

-- Holdings with current value and P&L
CREATE VIEW holdings_with_value AS
SELECT
    h.ticker,
    h.name,
    h.asset_type,
    h.shares,
    h.avg_buy_price,
    h.total_cost,
    h.first_buy_date,
    h.last_buy_date,
    cp.price as current_price,
    cp.updated_at as price_updated_at,
    h.shares * cp.price as current_value,
    (h.shares * cp.price) - h.total_cost as pnl,
    CASE
        WHEN h.total_cost > 0
        THEN ((h.shares * cp.price) - h.total_cost) / h.total_cost * 100
        ELSE 0
    END as pnl_percent
FROM current_holdings h
LEFT JOIN current_prices cp ON h.ticker = cp.ticker;

-- Dividend summary by ticker
CREATE VIEW dividend_summary AS
SELECT
    ticker,
    SUM(total_received) as total_dividends,
    COUNT(*) as dividend_count,
    MAX(payment_date) as last_dividend_date,
    MIN(payment_date) as first_dividend_date
FROM dividends
GROUP BY ticker;

-- Dividends by year
CREATE VIEW dividends_by_year AS
SELECT
    EXTRACT(YEAR FROM payment_date)::INTEGER as year,
    ticker,
    SUM(total_received) as total_received,
    COUNT(*) as payments
FROM dividends
GROUP BY EXTRACT(YEAR FROM payment_date), ticker
ORDER BY year DESC, total_received DESC;

-- Portfolio summary
CREATE VIEW portfolio_summary AS
SELECT
    SUM(current_value) as total_value,
    SUM(total_cost) as total_invested,
    SUM(pnl) as total_pnl,
    CASE
        WHEN SUM(total_cost) > 0
        THEN SUM(pnl) / SUM(total_cost) * 100
        ELSE 0
    END as total_pnl_percent,
    COUNT(*) as num_holdings
FROM holdings_with_value;
