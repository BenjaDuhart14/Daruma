"""
Calculation utilities for portfolio metrics.
"""

from datetime import datetime, date, timedelta
from typing import Optional
import pandas as pd


def calculate_shares_at_date(transactions: list, ticker: str,
                              target_date: date) -> float:
    """
    Calculate how many shares of a ticker were held at a specific date.

    Args:
        transactions: List of transaction dicts
        ticker: Ticker symbol
        target_date: Date to calculate holdings for

    Returns:
        Number of shares held at that date
    """
    shares = 0.0

    for tx in transactions:
        if tx['ticker'] != ticker:
            continue

        tx_date = tx['date']
        if isinstance(tx_date, str):
            tx_date = datetime.fromisoformat(tx_date.replace('Z', '+00:00')).date()
        elif isinstance(tx_date, datetime):
            tx_date = tx_date.date()

        if tx_date <= target_date:
            if tx['type'] == 'BUY':
                shares += float(tx['quantity'])
            elif tx['type'] == 'SELL':
                shares -= float(tx['quantity'])

    return max(0, shares)


def calculate_period_return(current_value: float, previous_value: float) -> tuple:
    """
    Calculate return for a period.

    Args:
        current_value: Current portfolio value
        previous_value: Value at start of period

    Returns:
        Tuple of (dollar_change, percent_change)
    """
    if previous_value <= 0:
        return (0.0, 0.0)

    dollar_change = current_value - previous_value
    percent_change = (dollar_change / previous_value) * 100

    return (dollar_change, percent_change)


def get_period_start_date(period: str) -> date:
    """
    Get start date for a given period code.

    Args:
        period: Period code ('1D', '1W', '1M', '3M', 'YTD', '1Y', 'ALL')

    Returns:
        Start date for the period
    """
    today = date.today()

    if period == '1D':
        return today - timedelta(days=1)
    elif period == '1W':
        return today - timedelta(weeks=1)
    elif period == '1M':
        return today - timedelta(days=30)
    elif period == '3M':
        return today - timedelta(days=90)
    elif period == 'YTD':
        return date(today.year, 1, 1)
    elif period == '1Y':
        return today - timedelta(days=365)
    elif period == 'ALL':
        return date(2000, 1, 1)  # Far past date
    else:
        return today


def calculate_weighted_avg_price(transactions: list, ticker: str) -> float:
    """
    Calculate weighted average buy price for a ticker.

    Args:
        transactions: List of transaction dicts
        ticker: Ticker symbol

    Returns:
        Weighted average price
    """
    total_cost = 0.0
    total_shares = 0.0

    for tx in transactions:
        if tx['ticker'] != ticker or tx['type'] != 'BUY':
            continue

        qty = float(tx['quantity'])
        price = float(tx['price'])

        total_cost += qty * price
        total_shares += qty

    if total_shares <= 0:
        return 0.0

    return total_cost / total_shares


def format_currency(value: float, currency: str = 'USD') -> str:
    """Format value as currency string."""
    if currency == 'USD':
        return f'${value:,.2f}'
    elif currency == 'CLP':
        return f'${value:,.0f} CLP'
    else:
        return f'{value:,.2f} {currency}'


def format_percent(value: float) -> str:
    """Format value as percentage string."""
    sign = '+' if value >= 0 else ''
    return f'{sign}{value:.2f}%'


def format_pnl(dollar_value: float, percent_value: float) -> str:
    """Format P&L with both dollar and percent."""
    dollar_str = format_currency(dollar_value)
    percent_str = format_percent(percent_value)

    if dollar_value >= 0:
        return f'+{dollar_str} ({percent_str})'
    else:
        return f'{dollar_str} ({percent_str})'
