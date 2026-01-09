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
- [x] Supabase database created (schema.sql executed)
- [x] Local .env configured with credentials
- [x] Tested locally (Streamlit runs at localhost:8501)
- [x] Pushed to GitHub: https://github.com/BenjaDuhart14/Daruma

## What's In Progress
- [ ] Make repo public on GitHub
- [ ] Deploy to Streamlit Cloud

## What's Left to Build
- [ ] Configure GitHub Actions secrets (SUPABASE_URL, SUPABASE_KEY)
- [ ] Connect UI to real Supabase data (replace mock data)
- [ ] Import actual Delta CSV data
- [ ] Test end-to-end flow with real data
- [ ] Verify automated price updates work

## Current Status
**Phase**: Ready for Streamlit Cloud Deployment
**Blocker**: Need to make GitHub repo public first
**Last Updated**: Pushed to GitHub

## Known Issues
- Streamlit deprecation warnings for `use_container_width` (cosmetic, doesn't affect function)
- UI currently shows mock data, not connected to Supabase yet

## Key URLs
- **GitHub Repo**: https://github.com/BenjaDuhart14/Daruma
- **Supabase Project**: https://pvxetjsadcgaeeqmauzz.supabase.co
- **Streamlit Cloud**: (pending deployment)

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
