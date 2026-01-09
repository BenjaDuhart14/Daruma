# System Patterns: Daruma

## Architecture Overview
```
GitHub Actions (cron every 4 hrs)
    -> Python script (fetch prices + FX + dividends)
    -> Supabase (stores all data)
    -> Streamlit Cloud (reads and visualizes)
    -> iPhone (PWA access)
```

## Data Flow Patterns

### Price Update Flow
1. GitHub Action triggers on schedule
2. Script reads unique tickers from `transactions` table
3. For each ticker:
   - Map internal ticker to yfinance format
   - Fetch current price with retry logic
   - Upsert to `current_prices`
   - Insert to `price_history`
4. Fetch and store FX rates
5. Calculate dividends for all tickers
6. Log results and errors

### Transaction Flow
1. User enters transaction via Streamlit form
2. Validate input (required fields, positive amounts)
3. Insert to `transactions` table
4. Views automatically recalculate holdings

### Holdings Calculation
- Uses SQL view `current_holdings`
- Aggregates BUY (+) and SELL (-) quantities
- Calculates weighted average buy price
- Filters to show only positive positions

### P&L Calculation
- Uses SQL view `holdings_with_value`
- Joins holdings with current prices
- P&L = (shares * current_price) - total_cost
- P&L% = P&L / total_cost * 100

## Key Design Decisions

### Database Design
- Separate tables for transactions vs. calculated data
- Views for computed metrics (DRY principle)
- `current_*` tables for fast lookups
- `*_history` tables for time-series data

### Ticker Mapping
- Internal format: simple (BTC, AAPL, BCI)
- yfinance format: with suffixes (BTC-USD, BCI.SN)
- Mapping done at fetch time, not storage

### Dividend Calculation
- Automatic, not manual entry
- Based on yfinance dividend history
- Calculates shares held at each payment date
- UNIQUE constraint prevents duplicates

## Error Handling Patterns
- Individual ticker failures don't stop batch
- Retry with exponential backoff for API calls
- Log all errors for debugging
- Graceful degradation in UI

## File Organization
```
src/
  app.py              # Main dashboard
  pages/              # Streamlit multi-page
  utils/              # Shared utilities
  scripts/            # Background jobs
```
