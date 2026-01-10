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
  - **auth.py** (NEW - authentication)
  - **styles.py** (NEW - Alpine Dusk design system)
- [x] update_prices.py script complete
- [x] import_delta_csv.py script complete
- [x] GitHub Actions workflow configured
- [x] Config files created (requirements.txt, .env.example, .gitignore)
- [x] README.md with setup instructions
- [x] Streamlit config (.streamlit/config.toml)
- [x] **Streamlit UI Complete - Alpine Dusk Theme**:
  - app.py - Dashboard with glassmorphism cards, portfolio chart
  - 1_Holdings.py - Asset list with company/crypto logos
  - 2_Performance.py - Performance metrics with styled charts
  - 3_Dividends.py - Dividend tracking with green theme
  - 4_Add_Transaction.py - Styled transaction form
  - 5_Import.py - Delta CSV import wizard
- [x] Supabase database created (schema.sql executed)
- [x] Local .env configured with credentials
- [x] Tested locally (Streamlit runs at localhost:8501/8502)
- [x] Pushed to GitHub: https://github.com/BenjaDuhart14/Daruma
- [x] **User Authentication COMPLETE**
  - Login page with Alpine Dusk styling
  - Email/password authentication via Streamlit secrets
  - All pages protected with check_password()
  - Logout button in sidebar

## What's In Progress
- [ ] Testing on iPhone (mobile responsiveness)
- [ ] Streamlit Cloud deployment with new UI

## What's Left to Build
- [ ] Import actual Delta CSV data
- [ ] Test end-to-end flow with real data on mobile
- [ ] Fine-tune mobile responsiveness if needed
- [ ] Add portfolio allocation pie chart
- [ ] Add performance comparison vs benchmarks (S&P 500)
- [ ] Edit/delete transactions feature
- [ ] Export data to CSV
- [ ] Price alerts (optional)

## Current Status
**Phase**: UI Redesign Complete - Ready for Mobile Testing
**Next Step**: Deploy to Streamlit Cloud and test on iPhone
**Last Updated**: January 2026 - Alpine Dusk theme complete
**Detailed Plan**: See `nextSteps.md` for full roadmap

## Recent Accomplishments (This Session)
1. ✅ Implemented full authentication system with styled login page
2. ✅ Created Alpine Dusk design system (700+ lines of CSS)
3. ✅ Redesigned all 6 pages with new theme
4. ✅ Added company/crypto logos (Financial Modeling Prep + CoinGecko APIs)
5. ✅ Fixed dropdown z-index for mobile compatibility
6. ✅ Committed and pushed to GitHub

## Known Issues
- Some smaller company logos may not load (falls back to initials)
- Streamlit dropdown z-index may need further mobile testing

## Key URLs
- **GitHub Repo**: https://github.com/BenjaDuhart14/Daruma
- **Supabase Project**: https://pvxetjsadcgaeeqmauzz.supabase.co
- **Streamlit Cloud**: https://daruma14.streamlit.app/

## Evolution of Decisions
| Date | Decision | Rationale |
|------|----------|-----------|
| Initial | Use yfinance | Free, covers most tickers |
| Initial | Supabase over Firebase | Better Postgres support, simpler |
| Initial | Streamlit over React | Faster development, Python-native |
| Initial | GitHub Actions over cron | Free, integrated with repo |
| Jan 2026 | Single-user auth | Simple password gate, no DB changes needed |
| Jan 2026 | Alpine Dusk theme | Modern fintech look, mobile-first design |
| Jan 2026 | Financial Modeling Prep for logos | Free API, good stock coverage |

## Milestones
1. ✅ **Backend Ready**: Scripts + DB schema complete
2. ✅ **Frontend Ready**: Streamlit app functional
3. ✅ **Deployed**: All services running in cloud
4. ✅ **Authentication**: Login page protecting all routes
5. ✅ **UI Redesign**: Alpine Dusk theme implemented
6. ⬜ **Data Imported**: Delta CSV loaded
7. ⬜ **Production**: Daily use on iPhone begins
