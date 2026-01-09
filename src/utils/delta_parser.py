"""
Parser for Delta app CSV export format.
"""

import re
import csv
import io
from datetime import datetime
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def parse_ticker_name(base_currency_name: str) -> tuple[str, str]:
    """
    Extract ticker and name from Delta's 'Base currency (name)' field.

    Examples:
        "VOO (Vanguard S&P 500 ETF)" -> ("VOO", "Vanguard S&P 500 ETF")
        "BTC (Bitcoin)" -> ("BTC", "Bitcoin")
        "BRK-B (Berkshire Hathaway Inc)" -> ("BRK-B", "Berkshire Hathaway Inc")

    Args:
        base_currency_name: The 'Base currency (name)' field from Delta CSV

    Returns:
        Tuple of (ticker, name)
    """
    match = re.match(r'^([A-Z0-9\-\.]+)\s*\((.+)\)$', base_currency_name.strip())

    if match:
        ticker = match.group(1)
        name = match.group(2)
        return (ticker, name)

    # Fallback: treat entire string as ticker
    return (base_currency_name.strip(), '')


def parse_delta_csv(csv_content: str) -> list[dict]:
    """
    Parse Delta CSV export and convert to transaction records.

    Expected columns:
    Date, Way, Base amount, Base currency (name), Base type, Quote amount,
    Quote currency, Exchange, Sent/Received from, Sent to, Fee amount,
    Fee currency (name), Broker, Notes, Sync Base Holding, Leverage Metadata

    Args:
        csv_content: Raw CSV content as string

    Returns:
        List of transaction dicts ready for database insertion
    """
    transactions = []
    errors = []

    reader = csv.DictReader(io.StringIO(csv_content))

    for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is 1)
        try:
            # Skip non-BUY/SELL transactions
            way = row.get('Way', '').strip().upper()
            if way not in ('BUY', 'SELL'):
                continue

            # Parse date
            date_str = row.get('Date', '').strip()
            if not date_str:
                errors.append(f'Row {row_num}: Missing date')
                continue

            try:
                tx_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            except ValueError:
                errors.append(f'Row {row_num}: Invalid date format: {date_str}')
                continue

            # Parse ticker and name
            base_currency = row.get('Base currency (name)', '').strip()
            if not base_currency:
                errors.append(f'Row {row_num}: Missing base currency')
                continue

            ticker, name = parse_ticker_name(base_currency)

            # Parse quantity
            quantity_str = row.get('Base amount', '').strip()
            try:
                quantity = float(quantity_str)
            except (ValueError, TypeError):
                errors.append(f'Row {row_num}: Invalid quantity: {quantity_str}')
                continue

            # Parse total amount
            quote_amount_str = row.get('Quote amount', '').strip()
            try:
                total_amount = float(quote_amount_str)
            except (ValueError, TypeError):
                errors.append(f'Row {row_num}: Invalid quote amount: {quote_amount_str}')
                continue

            # Calculate unit price
            if quantity > 0:
                price = total_amount / quantity
            else:
                errors.append(f'Row {row_num}: Zero quantity')
                continue

            # Parse other fields
            asset_type = row.get('Base type', '').strip().upper()
            currency = row.get('Quote currency', 'USD').strip().upper()
            exchange = row.get('Exchange', '').strip()
            notes = row.get('Notes', '').strip()

            transaction = {
                'date': tx_date.isoformat(),
                'ticker': ticker,
                'name': name if name else None,
                'type': way,
                'asset_type': asset_type if asset_type else None,
                'quantity': quantity,
                'price': round(price, 4),
                'total_amount': round(total_amount, 4),
                'currency': currency if currency else 'USD',
                'exchange': exchange if exchange else None,
                'platform': 'Delta Import',
                'notes': notes if notes else None
            }

            transactions.append(transaction)

        except Exception as e:
            errors.append(f'Row {row_num}: Unexpected error: {str(e)}')

    if errors:
        logger.warning(f'CSV parsing completed with {len(errors)} errors')
        for error in errors[:10]:  # Log first 10 errors
            logger.warning(error)

    logger.info(f'Parsed {len(transactions)} transactions from CSV')

    return transactions


def get_import_summary(transactions: list) -> dict:
    """
    Generate summary of parsed transactions.

    Args:
        transactions: List of parsed transaction dicts

    Returns:
        Summary dict with counts and stats
    """
    if not transactions:
        return {
            'total_transactions': 0,
            'unique_tickers': 0,
            'buy_count': 0,
            'sell_count': 0,
            'asset_types': {},
            'date_range': None
        }

    tickers = set(tx['ticker'] for tx in transactions)
    buy_count = sum(1 for tx in transactions if tx['type'] == 'BUY')
    sell_count = sum(1 for tx in transactions if tx['type'] == 'SELL')

    asset_types = {}
    for tx in transactions:
        at = tx.get('asset_type') or 'UNKNOWN'
        asset_types[at] = asset_types.get(at, 0) + 1

    dates = [tx['date'] for tx in transactions]

    return {
        'total_transactions': len(transactions),
        'unique_tickers': len(tickers),
        'tickers': sorted(tickers),
        'buy_count': buy_count,
        'sell_count': sell_count,
        'asset_types': asset_types,
        'date_range': {
            'earliest': min(dates),
            'latest': max(dates)
        }
    }
