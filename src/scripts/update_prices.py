"""
Automated price update script.
Runs via GitHub Actions every 4 hours.

Tasks:
1. Fetch current prices for all tickers in portfolio
2. Update current_prices and price_history tables
3. Fetch and store FX rates
4. Calculate and store dividends
5. Create portfolio snapshot
"""

import os
import sys
import logging
from datetime import date, datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dotenv import load_dotenv

load_dotenv()

from utils.supabase_client import (
    get_client,
    get_unique_tickers,
    get_all_transactions,
    upsert_current_price,
    insert_price_history,
    upsert_current_fx_rate,
    insert_fx_history,
    upsert_dividend,
    get_holdings_with_value,
    insert_portfolio_snapshot
)
from utils.price_fetcher import (
    fetch_price_with_retry,
    fetch_dividend_history,
    fetch_fx_rate
)
from utils.calculations import calculate_shares_at_date

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def update_prices(client) -> dict:
    """
    Fetch and update prices for all tickers.

    Returns:
        Dict with success/failure counts
    """
    logger.info('Starting price update...')

    tickers = get_unique_tickers(client)
    logger.info(f'Found {len(tickers)} unique tickers')

    success = 0
    failed = 0
    failed_tickers = []

    for ticker in tickers:
        price = fetch_price_with_retry(ticker)

        if price is not None:
            upsert_current_price(client, ticker, price)
            insert_price_history(client, ticker, price)
            success += 1
        else:
            failed += 1
            failed_tickers.append(ticker)

    logger.info(f'Price update complete: {success} success, {failed} failed')
    if failed_tickers:
        logger.warning(f'Failed tickers: {failed_tickers}')

    return {
        'success': success,
        'failed': failed,
        'failed_tickers': failed_tickers
    }


def update_fx_rates(client) -> dict:
    """
    Fetch and update FX rates.

    Returns:
        Dict with results
    """
    logger.info('Starting FX rate update...')

    pairs = [
        ('USD', 'CLP'),
        ('EUR', 'USD'),
    ]

    results = {}

    for base, quote in pairs:
        pair_name = f'{base}/{quote}'
        rate = fetch_fx_rate(base, quote)

        if rate is not None:
            upsert_current_fx_rate(client, pair_name, rate)
            insert_fx_history(client, pair_name, rate)
            results[pair_name] = rate
            logger.info(f'Updated FX rate {pair_name}: {rate}')
        else:
            results[pair_name] = None
            logger.warning(f'Failed to fetch FX rate {pair_name}')

    return results


def update_dividends(client) -> dict:
    """
    Calculate and update dividends for all tickers.

    Returns:
        Dict with dividend counts
    """
    logger.info('Starting dividend calculation...')

    tickers = get_unique_tickers(client)
    transactions = get_all_transactions(client)

    total_dividends = 0
    tickers_with_dividends = 0

    for ticker in tickers:
        div_history = fetch_dividend_history(ticker)

        if div_history.empty:
            continue

        tickers_with_dividends += 1

        for payment_date, dividend_per_share in div_history.items():
            # Convert timestamp to date
            if hasattr(payment_date, 'date'):
                pay_date = payment_date.date()
            else:
                pay_date = payment_date

            # Calculate shares held at dividend date
            shares = calculate_shares_at_date(transactions, ticker, pay_date)

            if shares <= 0:
                continue

            # Calculate total dividend received
            total_received = shares * float(dividend_per_share)

            # Store dividend
            upsert_dividend(
                client,
                ticker=ticker,
                payment_date=pay_date,
                dividend_per_share=float(dividend_per_share),
                shares_at_date=shares,
                total_received=total_received
            )

            total_dividends += 1

    logger.info(f'Dividend update complete: {total_dividends} records from '
                f'{tickers_with_dividends} tickers')

    return {
        'total_records': total_dividends,
        'tickers_with_dividends': tickers_with_dividends
    }


def create_portfolio_snapshot(client) -> dict:
    """
    Create a snapshot of current portfolio value.

    Returns:
        Dict with snapshot data
    """
    logger.info('Creating portfolio snapshot...')

    holdings = get_holdings_with_value(client)

    if not holdings:
        logger.warning('No holdings found for snapshot')
        return {'total_value': 0, 'total_cost': 0}

    total_value = sum(float(h.get('current_value') or 0) for h in holdings)
    total_cost = sum(float(h.get('total_cost') or 0) for h in holdings)

    insert_portfolio_snapshot(client, date.today(), total_value, total_cost)

    logger.info(f'Snapshot created: value=${total_value:,.2f}, cost=${total_cost:,.2f}')

    return {
        'total_value': total_value,
        'total_cost': total_cost,
        'date': date.today().isoformat()
    }


def main():
    """Main entry point for price update script."""
    logger.info('=' * 50)
    logger.info('DARUMA - Price Update Script')
    logger.info(f'Started at: {datetime.utcnow().isoformat()}')
    logger.info('=' * 50)

    try:
        client = get_client()
        logger.info('Connected to Supabase')

        # Update prices
        price_results = update_prices(client)

        # Update FX rates
        fx_results = update_fx_rates(client)

        # Update dividends
        dividend_results = update_dividends(client)

        # Create snapshot
        snapshot_results = create_portfolio_snapshot(client)

        # Summary
        logger.info('=' * 50)
        logger.info('UPDATE COMPLETE')
        logger.info(f'Prices: {price_results["success"]} updated, '
                   f'{price_results["failed"]} failed')
        logger.info(f'FX Rates: {len([r for r in fx_results.values() if r])} updated')
        logger.info(f'Dividends: {dividend_results["total_records"]} records')
        logger.info(f'Portfolio Value: ${snapshot_results["total_value"]:,.2f}')
        logger.info('=' * 50)

    except Exception as e:
        logger.error(f'Script failed with error: {e}')
        raise


if __name__ == '__main__':
    main()
