"""
Delta CSV import script.
Imports transaction history from Delta app export.
"""

import os
import sys
import argparse
import logging

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dotenv import load_dotenv

load_dotenv()

from utils.supabase_client import (
    get_client,
    insert_transaction,
    transaction_exists
)
from utils.delta_parser import parse_delta_csv, get_import_summary

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def import_csv(file_path: str, dry_run: bool = False) -> dict:
    """
    Import transactions from a Delta CSV file.

    Args:
        file_path: Path to the CSV file
        dry_run: If True, parse but don't insert into database

    Returns:
        Dict with import results
    """
    logger.info(f'Reading CSV file: {file_path}')

    # Read file
    with open(file_path, 'r', encoding='utf-8') as f:
        csv_content = f.read()

    # Parse CSV
    transactions = parse_delta_csv(csv_content)
    summary = get_import_summary(transactions)

    logger.info(f'Parsed {summary["total_transactions"]} transactions')
    logger.info(f'Unique tickers: {summary["unique_tickers"]}')
    logger.info(f'Buy: {summary["buy_count"]}, Sell: {summary["sell_count"]}')
    logger.info(f'Asset types: {summary["asset_types"]}')

    if summary['date_range']:
        logger.info(f'Date range: {summary["date_range"]["earliest"]} to '
                   f'{summary["date_range"]["latest"]}')

    if dry_run:
        logger.info('DRY RUN - No data inserted')
        return {
            'parsed': len(transactions),
            'inserted': 0,
            'skipped': 0,
            'errors': 0,
            'dry_run': True,
            'summary': summary
        }

    # Connect to database and insert
    client = get_client()
    logger.info('Connected to Supabase')

    inserted = 0
    skipped = 0
    errors = 0

    for tx in transactions:
        try:
            # Check for duplicates
            if transaction_exists(client, tx['ticker'], tx['date'], tx['quantity']):
                logger.debug(f'Skipping duplicate: {tx["ticker"]} on {tx["date"]}')
                skipped += 1
                continue

            # Insert transaction
            insert_transaction(client, tx)
            inserted += 1

            if inserted % 50 == 0:
                logger.info(f'Progress: {inserted} inserted...')

        except Exception as e:
            logger.error(f'Error inserting transaction: {e}')
            errors += 1

    logger.info('=' * 50)
    logger.info('IMPORT COMPLETE')
    logger.info(f'Inserted: {inserted}')
    logger.info(f'Skipped (duplicates): {skipped}')
    logger.info(f'Errors: {errors}')
    logger.info('=' * 50)

    return {
        'parsed': len(transactions),
        'inserted': inserted,
        'skipped': skipped,
        'errors': errors,
        'dry_run': False,
        'summary': summary
    }


def main():
    """Main entry point for import script."""
    parser = argparse.ArgumentParser(
        description='Import transactions from Delta CSV export'
    )
    parser.add_argument(
        'file',
        help='Path to the Delta CSV file'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Parse CSV but do not insert into database'
    )

    args = parser.parse_args()

    if not os.path.exists(args.file):
        logger.error(f'File not found: {args.file}')
        sys.exit(1)

    results = import_csv(args.file, dry_run=args.dry_run)

    if results['errors'] > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
