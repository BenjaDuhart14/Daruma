"""
Price fetching utilities using yfinance with retry logic.
"""

import time
import logging
from typing import Optional, Tuple
from datetime import datetime, timedelta

import yfinance as yf
import pandas as pd

from .ticker_mapping import get_yfinance_ticker

logger = logging.getLogger(__name__)


def fetch_price_with_retry(ticker: str, max_retries: int = 3,
                           base_delay: float = 1.0) -> Optional[float]:
    """
    Fetch current price for a ticker with exponential backoff retry.

    Args:
        ticker: Internal ticker symbol
        max_retries: Maximum number of retry attempts
        base_delay: Base delay in seconds (doubles each retry)

    Returns:
        Current price or None if failed
    """
    yf_ticker = get_yfinance_ticker(ticker)

    for attempt in range(max_retries):
        try:
            stock = yf.Ticker(yf_ticker)

            # Try to get current price from info
            info = stock.info
            price = info.get('regularMarketPrice') or info.get('currentPrice')

            if price and price > 0:
                logger.info(f'Fetched price for {ticker}: ${price:.4f}')
                return float(price)

            # Fallback: get last close from history
            hist = stock.history(period='1d')
            if not hist.empty:
                price = hist['Close'].iloc[-1]
                logger.info(f'Fetched price (from history) for {ticker}: ${price:.4f}')
                return float(price)

            logger.warning(f'No price data found for {ticker}')
            return None

        except Exception as e:
            delay = base_delay * (2 ** attempt)
            logger.warning(f'Attempt {attempt + 1} failed for {ticker}: {e}. '
                          f'Retrying in {delay}s...')
            if attempt < max_retries - 1:
                time.sleep(delay)

    logger.error(f'Failed to fetch price for {ticker} after {max_retries} attempts')
    return None


def fetch_dividend_history(ticker: str) -> pd.DataFrame:
    """
    Fetch dividend history for a ticker.

    Args:
        ticker: Internal ticker symbol

    Returns:
        DataFrame with dividend history (date index, dividend amount)
    """
    yf_ticker = get_yfinance_ticker(ticker)

    try:
        stock = yf.Ticker(yf_ticker)
        dividends = stock.dividends

        if dividends is not None and not dividends.empty:
            logger.info(f'Found {len(dividends)} dividend payments for {ticker}')
            return dividends

        logger.debug(f'No dividend history found for {ticker}')
        return pd.DataFrame()

    except Exception as e:
        logger.error(f'Error fetching dividends for {ticker}: {e}')
        return pd.DataFrame()


def fetch_fx_rate(base: str = 'USD', quote: str = 'CLP') -> Optional[float]:
    """
    Fetch current FX rate using yfinance.

    Args:
        base: Base currency (e.g., 'USD')
        quote: Quote currency (e.g., 'CLP')

    Returns:
        Exchange rate (1 base = X quote) or None if failed
    """
    pair_ticker = f'{base}{quote}=X'

    try:
        ticker = yf.Ticker(pair_ticker)
        info = ticker.info
        rate = info.get('regularMarketPrice') or info.get('ask') or info.get('bid')

        if rate and rate > 0:
            logger.info(f'Fetched FX rate {base}/{quote}: {rate:.4f}')
            return float(rate)

        # Fallback to history
        hist = ticker.history(period='1d')
        if not hist.empty:
            rate = hist['Close'].iloc[-1]
            logger.info(f'Fetched FX rate (from history) {base}/{quote}: {rate:.4f}')
            return float(rate)

        logger.warning(f'No FX rate found for {base}/{quote}')
        return None

    except Exception as e:
        logger.error(f'Error fetching FX rate {base}/{quote}: {e}')
        return None


def fetch_multiple_prices(tickers: list[str]) -> dict[str, Optional[float]]:
    """
    Fetch prices for multiple tickers.

    Args:
        tickers: List of internal ticker symbols

    Returns:
        Dict mapping ticker to price (or None if failed)
    """
    results = {}

    for ticker in tickers:
        price = fetch_price_with_retry(ticker)
        results[ticker] = price
        # Small delay between requests to avoid rate limiting
        time.sleep(0.5)

    success_count = sum(1 for p in results.values() if p is not None)
    logger.info(f'Fetched prices: {success_count}/{len(tickers)} successful')

    return results
