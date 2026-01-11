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
  - auth.py (authentication)
  - styles.py (Alpine Dusk design system + mobile CSS)
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
- [x] **Mobile-First Responsive Design COMPLETE**
  - 3 breakpoints: 768px, 480px, 375px
  - 2x2 grid layouts for metrics
  - Stacked card layouts for holdings
  - Touch-friendly active states
  - Collapsed sidebar by default
- [x] **Spanish to English Translation COMPLETE**
- [x] **Delta CSV Data Imported** (210 transactions, 37 tickers)

## What's In Progress
- [ ] Push latest commit to GitHub (WSL auth issue)
- [ ] Final iPhone testing after Streamlit Cloud redeploy

## What's Left to Build
- [ ] Fine-tune mobile responsiveness if needed after testing
- [ ] Portfolio allocation pie chart
- [ ] Performance comparison vs S&P 500 benchmark
- [ ] Edit/delete transactions feature
- [ ] Export data to CSV
- [ ] Price alerts (optional)

## Current Status
**Phase**: Mobile Redesign Complete - Ready for Final Testing
**Next Step**: Push to GitHub and test on iPhone
**Last Updated**: January 11, 2026 - Mobile redesign + translations complete
**Detailed Plan**: See `nextSteps.md` for full roadmap

## Recent Accomplishments (This Session - January 11, 2026)
1. Added 3 CSS breakpoints for mobile responsiveness (768px, 480px, 375px)
2. Changed all metric layouts from 4 columns to 2x2 grids
3. Split 7 period buttons into 4+3 rows for better touch targets
4. Created mobile-friendly stacked card layout for holdings
5. Added touch-friendly `:active` states (replaces hover on touch devices)
6. Fixed iOS input zoom issue with 16px minimum font size
7. Reduced font sizes and padding for small screens
8. Changed all pages to collapsed sidebar by default
9. Translated all Spanish text to English
10. Imported Delta CSV data (210 transactions)
11. Committed all changes to Git

## Known Issues
- Some smaller company logos may not load (falls back to initials)
- WSL Git authentication requires manual push to GitHub
- Performance page uses mock data (not connected to real snapshots yet)

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
| Jan 11, 2026 | 2x2 grid layouts | 4 columns too cramped on mobile |
| Jan 11, 2026 | Collapsed sidebar default | Sidebar covers screen on mobile |
| Jan 11, 2026 | English-only UI | Consistent language for all users |

## Milestones
1. Backend Ready: Scripts + DB schema complete
2. Frontend Ready: Streamlit app functional
3. Deployed: All services running in cloud
4. Authentication: Login page protecting all routes
5. UI Redesign: Alpine Dusk theme implemented
6. **Mobile Responsive: 3 breakpoints, touch-friendly**
7. **Data Imported: Delta CSV loaded (210 transactions)**
8. Production: Daily use on iPhone begins (pending final test)
