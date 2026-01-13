# Active Context: Daruma

## Current Focus
**App is LIVE and fully functional!** All data showing correctly on Streamlit Cloud. Real portfolio value: ~$82k (after EWT price correction). Ready for daily use.

## Recent Changes (This Session - January 13, 2026)

### 1. App Deployment Verified Working
- Confirmed real data displaying on Streamlit Cloud
- Total Value: ~$82,000 (corrected after EWT fix)
- Total P&L: +$22,000 (+37%)
- 36 assets tracked

### 2. Fixed Crypto Ticker Mappings
**Problem**: EWT (Energy Web Token) was showing $66.62 instead of ~$0.81
- yfinance `EWT` = iShares Taiwan ETF (wrong!)
- yfinance `EWT-USD` = Energy Web Token (correct)

**Solution**: Updated `ticker_mapping.py` to include:
```python
'EWT': 'EWT-USD',   # Energy Web Token
'AVAIL': 'AVAIL-USD',  # Avail
'CAKE': 'CAKE-USD',  # PancakeSwap
# Plus 17 more common crypto tickers
```

### 3. Added Refresh Data Button
- New "🔄 Refresh Data" button in sidebar
- Clears `@st.cache_data` cache and forces reload
- Useful for seeing updated prices immediately

### 4. Removed Debug Page
- Deleted `src/pages/9_Debug.py` after confirming app works
- Was only needed for troubleshooting Supabase connection

### 5. UI Improvements
- Company logos on Dashboard (same as Holdings page)
- Fixed dropdown text sizes (14px)
- Page title changed to "Home - Daruma" (browser tab)
- Note: Sidebar still shows "app" (filename-based, requires Streamlit Cloud config change)

---

## Previous Changes (January 12, 2026)

### Supabase Connection Fix
- `supabase_client.py` now checks both `st.secrets` and `os.getenv()`
- Supports secrets at root level OR under `[auth]` section
- Key learning: Use `st.secrets['KEY']` not `st.secrets.get('KEY')`

### Other Fixes
- Hidden sidebar on login page
- Removed Import page (CLI only)
- Transaction history with delete
- Mobile-optimized charts and buttons
- Performance page with real data

---

## Completed Steps
1. [x] Supabase project + schema
2. [x] Local development
3. [x] GitHub deployment
4. [x] Streamlit Cloud deployment
5. [x] GitHub Actions (price updates every 4 hours)
6. [x] User authentication
7. [x] Alpine Dusk theme
8. [x] Company/crypto logos
9. [x] Mobile-first responsive design
10. [x] Delta CSV import (211 transactions)
11. [x] **Supabase connection on Streamlit Cloud**
12. [x] **Real data on all pages**
13. [x] **Crypto ticker mappings fixed**
14. [x] **App verified working in production**

---

## Active Decisions

### Decided
- Stack: Streamlit + Supabase + GitHub Actions + yfinance
- All free tiers
- USD as base currency
- Single-user auth via Streamlit secrets
- Alpine Dusk theme, mobile-first
- Crypto tickers use `-USD` suffix in yfinance

### Pending
- Portfolio allocation pie chart
- Performance vs S&P 500 benchmark

---

## Important Patterns
- **Crypto tickers**: Must add to `ticker_mapping.py` with `-USD` suffix
- **Streamlit secrets**: Use bracket notation `st.secrets['KEY']`
- **Cache**: Use "Refresh Data" button or wait 5 min for auto-refresh
- **Never commit credentials** to public repo

---

## Key Files Modified This Session
```
src/app.py                    # Added Refresh Data button, logos
src/utils/ticker_mapping.py   # Added EWT, AVAIL, CAKE + 17 cryptos
src/utils/styles.py           # Dropdown text size fixes
src/pages/9_Debug.py          # DELETED (was temporary)
```

## Session Commits (January 13, 2026)
1. `334c0ab` fix: Date calculation bug
2. `e55b016` feat: Rename App to Home, logos, dropdown fixes
3. `f564ebd` feat: Add Refresh Data button
4. `31abe7e` chore: Remove debug page
5. `0fb4377` fix: Add missing crypto ticker mappings

---

## Next Actions
1. **Push to GitHub** (commits pending)
2. Click "Refresh Data" in app to see corrected values
3. Monitor GitHub Actions for price updates

---

## Key URLs
- **Live App**: https://daruma14.streamlit.app/
- **GitHub Repo**: https://github.com/BenjaDuhart14/Daruma
- **Supabase**: https://pvxetjsadcgaeeqmauzz.supabase.co
- **GitHub Actions**: https://github.com/BenjaDuhart14/Daruma/actions
