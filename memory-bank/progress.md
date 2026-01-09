# Progress: Daruma

## What Works
- [x] Project directory structure created
- [x] Memory Bank initialized
- [x] SQL schema complete (sql/schema.sql)
- [x] Utility modules complete:
  - ticker_mapping.py
  - supabase_client.py
  - price_fetcher.py
  - calculations.py
  - delta_parser.py
- [x] update_prices.py script complete
- [x] import_delta_csv.py script complete
- [x] GitHub Actions workflow configured
- [x] Config files created (requirements.txt, .env.example, .gitignore)
- [x] README.md with setup instructions
- [x] Streamlit config (.streamlit/config.toml)
- [x] Streamlit UI complete (based on Delta app design):
  - app.py - Main dashboard with portfolio value, chart, top movers
  - 1_Holdings.py - Asset list with sorting/filtering
  - 2_Performance.py - Performance metrics by period
  - 3_Dividends.py - Dividend tracking and charts
  - 4_Add_Transaction.py - Manual transaction form
  - 5_Import.py - Delta CSV import with preview

## What's In Progress
- [ ] Connect UI to Supabase (currently using mock data)

## What's Left to Build
- [ ] Deploy to Supabase (run schema.sql)
- [ ] Deploy to Streamlit Cloud
- [ ] Configure GitHub Actions secrets
- [ ] Replace mock data with real Supabase queries
- [ ] Test end-to-end flow
- [ ] Import actual Delta CSV data

## Current Status
**Phase**: Full UI Complete with Mock Data
**Blocker**: None - Ready for Supabase setup
**Last Updated**: All pages created

## Known Issues
None yet - project just started.

## Evolution of Decisions
| Date | Decision | Rationale |
|------|----------|-----------|
| Initial | Use yfinance | Free, covers most tickers |
| Initial | Supabase over Firebase | Better Postgres support, simpler |
| Initial | Streamlit over React | Faster development, Python-native |
| Initial | GitHub Actions over cron | Free, integrated with repo |

## Milestones
1. **Backend Ready**: Scripts + DB schema complete
2. **Frontend Ready**: Streamlit app functional
3. **Deployed**: All services running in cloud
4. **Data Imported**: Delta CSV loaded
5. **Production**: Daily use begins
