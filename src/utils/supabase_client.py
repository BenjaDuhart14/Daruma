"""
Supabase client and database operations.
"""

import os
from datetime import datetime, date
from typing import Optional
from decimal import Decimal

from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()


def get_client() -> Client:
    """Get Supabase client instance."""
    # Try environment variables first (local dev, GitHub Actions)
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_KEY')

    # Fallback to Streamlit secrets (Streamlit Cloud)
    if not url or not key:
        try:
            import streamlit as st
            url = st.secrets.get('SUPABASE_URL', url)
            key = st.secrets.get('SUPABASE_KEY', key)
        except Exception:
            pass

    if not url or not key:
        raise ValueError('SUPABASE_URL and SUPABASE_KEY must be set')

    return create_client(url, key)


# ----- Transactions -----

def get_all_transactions(client: Client) -> list:
    """Get all transactions ordered by date."""
    response = client.table('transactions').select('*').order('date', desc=True).execute()
    return response.data


def get_unique_tickers(client: Client) -> list[str]:
    """Get list of unique tickers from transactions."""
    response = client.table('transactions').select('ticker').execute()
    tickers = set(row['ticker'] for row in response.data)
    return list(tickers)


def insert_transaction(client: Client, transaction: dict) -> dict:
    """Insert a new transaction."""
    response = client.table('transactions').insert(transaction).execute()
    return response.data[0] if response.data else None


def transaction_exists(client: Client, ticker: str, date_str: str, quantity: float) -> bool:
    """Check if a transaction already exists (for deduplication)."""
    response = client.table('transactions').select('id').eq(
        'ticker', ticker
    ).eq(
        'date', date_str
    ).eq(
        'quantity', quantity
    ).execute()
    return len(response.data) > 0


# ----- Prices -----

def upsert_current_price(client: Client, ticker: str, price: float, currency: str = 'USD'):
    """Update or insert current price for a ticker."""
    data = {
        'ticker': ticker,
        'price': price,
        'currency': currency,
        'updated_at': datetime.utcnow().isoformat()
    }
    client.table('current_prices').upsert(data).execute()


def insert_price_history(client: Client, ticker: str, price: float, currency: str = 'USD'):
    """Insert a price history record."""
    data = {
        'ticker': ticker,
        'price': price,
        'currency': currency
    }
    client.table('price_history').insert(data).execute()


def get_current_prices(client: Client) -> dict:
    """Get all current prices as dict {ticker: price}."""
    response = client.table('current_prices').select('ticker, price').execute()
    return {row['ticker']: float(row['price']) for row in response.data}


def get_price_history(client: Client, ticker: str, days: int = 365) -> list:
    """Get price history for a ticker."""
    from_date = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    from_date = from_date.replace(day=from_date.day - days) if days else None

    query = client.table('price_history').select('*').eq('ticker', ticker)
    if from_date:
        query = query.gte('recorded_at', from_date.isoformat())

    response = query.order('recorded_at').execute()
    return response.data


# ----- FX Rates -----

def upsert_current_fx_rate(client: Client, pair: str, rate: float):
    """Update or insert current FX rate."""
    data = {
        'pair': pair,
        'rate': rate,
        'updated_at': datetime.utcnow().isoformat()
    }
    client.table('current_fx_rates').upsert(data).execute()


def insert_fx_history(client: Client, pair: str, rate: float):
    """Insert FX rate history record."""
    data = {
        'pair': pair,
        'rate': rate
    }
    client.table('fx_rates').insert(data).execute()


def get_current_fx_rate(client: Client, pair: str) -> Optional[float]:
    """Get current FX rate for a pair."""
    response = client.table('current_fx_rates').select('rate').eq('pair', pair).execute()
    if response.data:
        return float(response.data[0]['rate'])
    return None


# ----- Dividends -----

def upsert_dividend(client: Client, ticker: str, payment_date: date,
                    dividend_per_share: float, shares_at_date: float,
                    total_received: float, currency: str = 'USD'):
    """Insert or update dividend record."""
    data = {
        'ticker': ticker,
        'payment_date': payment_date.isoformat(),
        'dividend_per_share': dividend_per_share,
        'shares_at_date': shares_at_date,
        'total_received': total_received,
        'currency': currency,
        'calculated_at': datetime.utcnow().isoformat()
    }
    client.table('dividends').upsert(
        data,
        on_conflict='ticker,payment_date'
    ).execute()


def get_dividends(client: Client, ticker: Optional[str] = None) -> list:
    """Get dividends, optionally filtered by ticker."""
    query = client.table('dividends').select('*')
    if ticker:
        query = query.eq('ticker', ticker)
    response = query.order('payment_date', desc=True).execute()
    return response.data


# ----- Views (read-only) -----

def get_holdings_with_value(client: Client) -> list:
    """Get holdings with current value and P&L from view."""
    response = client.table('holdings_with_value').select('*').execute()
    return response.data


def get_portfolio_summary(client: Client) -> dict:
    """Get portfolio summary from view."""
    response = client.table('portfolio_summary').select('*').execute()
    return response.data[0] if response.data else {}


def get_dividend_summary(client: Client) -> list:
    """Get dividend summary by ticker from view."""
    response = client.table('dividend_summary').select('*').execute()
    return response.data


def get_dividends_by_year(client: Client) -> list:
    """Get dividends aggregated by year from view."""
    response = client.table('dividends_by_year').select('*').execute()
    return response.data


# ----- Portfolio Snapshots -----

def insert_portfolio_snapshot(client: Client, snapshot_date: date,
                               total_value: float, total_cost: float):
    """Insert or update portfolio snapshot."""
    data = {
        'snapshot_date': snapshot_date.isoformat(),
        'total_value': total_value,
        'total_cost': total_cost
    }
    client.table('portfolio_snapshots').upsert(
        data,
        on_conflict='snapshot_date'
    ).execute()


def get_portfolio_snapshots(client: Client, days: Optional[int] = None) -> list:
    """Get portfolio snapshots for chart."""
    query = client.table('portfolio_snapshots').select('*')
    if days:
        from_date = date.today().replace(day=date.today().day - days)
        query = query.gte('snapshot_date', from_date.isoformat())
    response = query.order('snapshot_date').execute()
    return response.data
