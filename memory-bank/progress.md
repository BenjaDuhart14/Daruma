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
  - styles.py (Alpine Dusk + Daruma logo + FAB)
- [x] update_prices.py script complete
- [x] import_delta_csv.py script complete
- [x] GitHub Actions workflow (runs every 4 hours)
- [x] Config files (requirements.txt, .env.example, .gitignore)
- [x] README.md with setup instructions
- [x] Streamlit config (.streamlit/config.toml)
- [x] **Streamlit UI Complete - Alpine Dusk Theme**
- [x] Supabase database created and populated
- [x] **211 transactions imported**
- [x] **36 holdings tracked**
- [x] **User Authentication COMPLETE**
- [x] **Mobile-First Responsive Design COMPLETE**
- [x] **Supabase Connection on Streamlit Cloud WORKING**
- [x] **Crypto Ticker Mappings Fixed**
- [x] **App LIVE in Production**

### Day 1 UI Enhancements ✅
- [x] Daruma logo SVG (one eye painted, one empty)
- [x] Renamed "Dashboard" to "Home"
- [x] FAB (+) button for quick transaction adding
- [x] Daruma favicon in browser tab
- [x] Sidebar "app" renamed to "Home" via CSS

## What's In Progress
- **Phase 2: Chart Enhancements**
  - Dynamic value display above chart
  - Portfolio allocation donut chart
  - Candlestick chart option

## What's Left to Build

### Phase 2: Chart Enhancements
- [ ] Dynamic value display above chart (updates on hover/touch)
- [ ] Portfolio allocation donut chart on Home page
- [ ] Candlestick chart option for Performance page
- [ ] Improved High/Low markers with better styling

### Phase 3: Native Feel
- [ ] Horizontal scroll period selector (single row)
- [ ] Bottom navigation bar
- [ ] Swipe-to-reveal actions on holdings cards
- [ ] Animated value counters

### Future Enhancements
- [ ] S&P 500 benchmark comparison
- [ ] Edit transactions feature
- [ ] Export data to CSV
- [ ] Currency toggle (USD/CLP)
- [ ] Dividend calendar view

## Current Status
**Phase**: UI Enhancement - Day 1 Complete
**Portfolio Value**: ~$81,000
**Last Updated**: January 13, 2026

---

## Recent Accomplishments (January 13, 2026)

### Day 1: Core Identity & Quick Add
1. **Daruma Logo** - Custom SVG with traditional one-eye-painted design
2. **Home Page Rename** - Dashboard → Home
3. **FAB Button** - Floating action button for quick transaction adding
4. **Favicon** - Daruma doll in browser tab
5. **Sidebar Fix** - "app" → "Home" via CSS

---

## Known Issues
- Some smaller company logos may not load (falls back to initials)
- WSL Git authentication requires manual push from Ubuntu terminal

---

## Key URLs
- **Live App**: https://daruma14.streamlit.app/
- **GitHub Repo**: https://github.com/BenjaDuhart14/Daruma
- **Supabase**: https://pvxetjsadcgaeeqmauzz.supabase.co

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
11. ✅ **Day 1 UI: Daruma Logo + FAB**
12. 🔄 **Day 2 UI: Chart Enhancements** (In Progress)

---

## File Structure
```
src/
├── app.py                    # Home page (Daruma logo, FAB)
├── favicon.svg               # Daruma doll favicon
├── pages/
│   ├── 1_Holdings.py         # Holdings with logos
│   ├── 2_Performance.py      # Performance charts
│   ├── 3_Dividends.py        # Dividend tracking
│   └── 4_Add_Transaction.py  # Transaction form
└── utils/
    ├── auth.py               # Authentication
    ├── styles.py             # Alpine Dusk + Daruma + FAB CSS
    ├── supabase_client.py    # Database operations
    ├── price_fetcher.py      # yfinance integration
    ├── calculations.py       # Portfolio math
    ├── delta_parser.py       # CSV parsing
    └── ticker_mapping.py     # Ticker mappings
```
