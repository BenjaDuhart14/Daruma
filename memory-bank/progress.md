# Progress: Daruma

## What Works
- [x] Project directory structure created
- [x] Memory Bank initialized
- [x] SQL schema complete (sql/schema.sql)
- [x] Utility modules complete:
  - ticker_mapping.py
  - supabase_client.py (with st.secrets fallback for Streamlit Cloud)
  - price_fetcher.py
  - calculations.py
  - delta_parser.py
  - auth.py (authentication + hidden sidebar on login)
  - styles.py (Alpine Dusk design system + mobile CSS)
- [x] update_prices.py script complete
- [x] import_delta_csv.py script complete
- [x] GitHub Actions workflow configured (runs every 4 hours)
- [x] Config files created (requirements.txt, .env.example, .gitignore)
- [x] README.md with setup instructions
- [x] Streamlit config (.streamlit/config.toml)
- [x] **Streamlit UI Complete - Alpine Dusk Theme**:
  - app.py - Dashboard with glassmorphism cards, portfolio chart
  - 1_Holdings.py - Asset list with company/crypto logos
  - 2_Performance.py - Performance metrics with REAL data from Supabase
  - 3_Dividends.py - Dividend tracking with green theme
  - 4_Add_Transaction.py - Transaction form + history log with delete
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
- [x] **Supabase Connection Fixed for Streamlit Cloud**
- [x] **Performance Page Connected to Real Data**

## What's In Progress
- [ ] Push latest commits to GitHub (9 commits pending)
- [ ] Final iPhone testing after Streamlit Cloud redeploy

## What's Left to Build
- [ ] Portfolio allocation pie chart
- [ ] Performance comparison vs S&P 500 benchmark
- [ ] Edit transactions feature (delete now works)
- [ ] Export data to CSV
- [ ] Price alerts (optional)

## Current Status
**Phase**: All UI/UX Fixes Complete - Ready for Final Testing
**Next Step**: Push to GitHub and test on iPhone
**Last Updated**: January 12, 2026 - Supabase connection fixed, Performance page real data
**Detailed Plan**: See `nextSteps.md` for full roadmap

## Recent Accomplishments (This Session - January 12, 2026)

### Critical Fix: Supabase + Streamlit Cloud Connection
**Problem**: App showed "Database connection error" on Streamlit Cloud because:
- `supabase_client.py` used `os.getenv()` which only works for environment variables
- Streamlit Cloud uses `st.secrets` which is accessed differently

**Solution**: Updated `get_client()` to check both sources:
```python
# Try environment variables first (local dev, GitHub Actions)
url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')

# Fallback to Streamlit secrets (Streamlit Cloud)
if not url or not key:
    if 'SUPABASE_URL' in st.secrets:
        url = st.secrets['SUPABASE_URL']
    if 'SUPABASE_KEY' in st.secrets:
        key = st.secrets['SUPABASE_KEY']
```

**Key Learning**: Use `st.secrets['KEY']` bracket notation, NOT `st.secrets.get('KEY')`.

### Other Fixes This Session
1. Hidden sidebar navigation on login page (security fix)
2. Removed Import page (CLI only now)
3. Added transaction history log with filters and delete
4. Fixed chart overflow (margins 70px → 5-50px)
5. Compact period buttons (height 44px → 36-38px)
6. Smaller data row styling for mobile
7. Performance page now uses real Supabase data

## Known Issues
- Some smaller company logos may not load (falls back to initials)
- WSL Git authentication requires manual push to GitHub
- Portfolio snapshots table may be empty initially (needs GitHub Actions to run)

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
| Jan 12, 2026 | st.secrets fallback | Required for Streamlit Cloud deployment |
| Jan 12, 2026 | Remove Import page | Reduces attack surface, CLI is sufficient |
| Jan 12, 2026 | Real data in Performance | Mock data replaced with Supabase calls |

## Milestones
1. Backend Ready: Scripts + DB schema complete
2. Frontend Ready: Streamlit app functional
3. Deployed: All services running in cloud
4. Authentication: Login page protecting all routes
5. UI Redesign: Alpine Dusk theme implemented
6. Mobile Responsive: 3 breakpoints, touch-friendly
7. Data Imported: Delta CSV loaded (210 transactions)
8. **Streamlit Cloud Fixed**: Database connection working
9. **Real Data**: Performance page using actual portfolio data
10. Production: Daily use on iPhone begins (pending final test)

## File Structure (Current)
```
src/
├── app.py                    # Main dashboard
├── pages/
│   ├── 1_Holdings.py         # Portfolio holdings with logos
│   ├── 2_Performance.py      # Performance (REAL DATA)
│   ├── 3_Dividends.py        # Dividend tracking
│   └── 4_Add_Transaction.py  # Form + transaction log
└── utils/
    ├── auth.py               # Authentication (sidebar hidden on login)
    ├── styles.py             # Alpine Dusk + mobile CSS
    ├── supabase_client.py    # DB ops (st.secrets fallback)
    ├── price_fetcher.py      # yfinance integration
    ├── calculations.py       # Portfolio math
    ├── delta_parser.py       # CSV parsing
    └── ticker_mapping.py     # Ticker conversions
```

Note: `5_Import.py` was deleted - import via CLI only.
