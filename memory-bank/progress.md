# Progress: Daruma

## What Works
- [x] Project directory structure created
- [x] Memory Bank initialized
- [x] SQL schema complete (sql/schema.sql)
- [x] Utility modules complete:
  - ticker_mapping.py (with crypto `-USD` suffix mappings)
  - supabase_client.py (st.secrets + os.getenv fallback)
  - price_fetcher.py
  - calculations.py
  - delta_parser.py
  - auth.py (authentication + hidden sidebar on login)
  - styles.py (Alpine Dusk design system + mobile CSS)
- [x] update_prices.py script complete
- [x] import_delta_csv.py script complete
- [x] GitHub Actions workflow (runs every 4 hours)
- [x] Config files (requirements.txt, .env.example, .gitignore)
- [x] README.md with setup instructions
- [x] Streamlit config (.streamlit/config.toml)
- [x] **Streamlit UI Complete - Alpine Dusk Theme**:
  - app.py - Dashboard with logos, Refresh Data button
  - 1_Holdings.py - Asset list with company/crypto logos
  - 2_Performance.py - Performance with REAL Supabase data
  - 3_Dividends.py - Dividend tracking
  - 4_Add_Transaction.py - Transaction form + history log
- [x] Supabase database created and populated
- [x] **211 transactions imported**
- [x] **36 holdings tracked**
- [x] **User Authentication COMPLETE**
- [x] **Mobile-First Responsive Design COMPLETE**
- [x] **Supabase Connection on Streamlit Cloud WORKING**
- [x] **Crypto Ticker Mappings Fixed (EWT, AVAIL, CAKE)**
- [x] **App LIVE in Production**

## What's In Progress
- Nothing currently in progress - app is functional!

## What's Left to Build (Future Enhancements)
- [ ] Portfolio allocation pie chart
- [ ] Performance comparison vs S&P 500 benchmark
- [ ] Edit transactions feature (delete works)
- [ ] Export data to CSV
- [ ] Currency toggle (USD/CLP)
- [ ] Dividend calendar view
- [ ] Price alerts (optional)

## Current Status
**Phase**: PRODUCTION - App is live and functional
**Portfolio Value**: ~$82,000 (after EWT correction)
**Last Updated**: January 13, 2026

---

## Recent Accomplishments (January 13, 2026)

### Critical Fix: Crypto Ticker Mappings
**Problem**: EWT showing $66.62 instead of $0.81
- `EWT` in yfinance = iShares Taiwan ETF (wrong ticker!)
- `EWT-USD` in yfinance = Energy Web Token (correct)

**Solution**: Added to `ticker_mapping.py`:
```python
'EWT': 'EWT-USD',
'AVAIL': 'AVAIL-USD',
'CAKE': 'CAKE-USD',
# Plus 17 more crypto tickers
```

### Other Fixes This Session
1. Added "Refresh Data" button to sidebar (clears cache)
2. Company logos on Dashboard
3. Fixed dropdown text sizes (14px)
4. Removed temporary Debug page
5. Verified app working on Streamlit Cloud

---

## Known Issues
- Sidebar shows "app" instead of "Home" (requires Streamlit Cloud config change)
- Some smaller company logos may not load (falls back to initials)
- WSL Git authentication requires manual push

---

## Key URLs
- **Live App**: https://daruma14.streamlit.app/
- **GitHub Repo**: https://github.com/BenjaDuhart14/Daruma
- **Supabase**: https://pvxetjsadcgaeeqmauzz.supabase.co

---

## Evolution of Decisions
| Date | Decision | Rationale |
|------|----------|-----------|
| Initial | yfinance | Free, covers most tickers |
| Initial | Supabase | Better Postgres support |
| Initial | Streamlit | Faster dev, Python-native |
| Initial | GitHub Actions | Free, integrated |
| Jan 2026 | Single-user auth | Simple, no DB changes |
| Jan 2026 | Alpine Dusk theme | Modern fintech look |
| Jan 12 | st.secrets fallback | Streamlit Cloud compat |
| Jan 13 | Crypto `-USD` suffix | yfinance requires it |

---

## Milestones
1. ✅ Backend Ready
2. ✅ Frontend Ready
3. ✅ Deployed to Cloud
4. ✅ Authentication
5. ✅ Alpine Dusk Theme
6. ✅ Mobile Responsive
7. ✅ Data Imported (211 transactions)
8. ✅ Streamlit Cloud Connection Fixed
9. ✅ Crypto Tickers Fixed
10. ✅ **PRODUCTION READY**

---

## File Structure
```
src/
├── app.py                    # Main dashboard (with Refresh button)
├── pages/
│   ├── 1_Holdings.py         # Holdings with logos
│   ├── 2_Performance.py      # Real Supabase data
│   ├── 3_Dividends.py        # Dividend tracking
│   └── 4_Add_Transaction.py  # Form + history log
└── utils/
    ├── auth.py               # Auth (hidden sidebar on login)
    ├── styles.py             # Alpine Dusk + mobile CSS
    ├── supabase_client.py    # DB ops (dual secrets source)
    ├── price_fetcher.py      # yfinance integration
    ├── calculations.py       # Portfolio math
    ├── delta_parser.py       # CSV parsing
    └── ticker_mapping.py     # Crypto/stock ticker mappings
```
