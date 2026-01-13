# Active Context: Daruma

## Current Focus
All major UI/UX fixes complete. Final polish applied: renamed App to Home, added company logos to Dashboard, fixed dropdown text sizes. Ready for push to GitHub and iPhone testing.

## Recent Changes (This Session - January 13, 2026)

### 1. Renamed App Page to Home
- Changed page_title from "Daruma" to "Home - Daruma" in `src/app.py`

### 2. Added Company Logos to Dashboard
- Added `get_logo_url()` function to `app.py` (same as Holdings page)
- Updated `render_holding_row()` to display logos with fallback to initials
- Supports stocks/ETFs via Financial Modeling Prep and crypto via CoinGecko

### 3. Fixed Dropdown Text Size
- Added `font-size: 14px` to selectbox elements in `styles.py`
- Fixed dropdown menu item sizes for both desktop and mobile
- Ensures consistent text size across all dropdown components

---

## Previous Changes (January 12, 2026)

### 1. Fixed Supabase Connection for Streamlit Cloud
**Problem**: `supabase_client.py` used `os.getenv()` which works locally and in GitHub Actions, but Streamlit Cloud stores secrets differently via `st.secrets`.

**Solution**: Updated `get_client()` in `supabase_client.py` to check both:
```python
# Try environment variables first (local dev, GitHub Actions)
url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')

# Fallback to Streamlit secrets (Streamlit Cloud)
if not url or not key:
    try:
        import streamlit as st
        if not url and 'SUPABASE_URL' in st.secrets:
            url = st.secrets['SUPABASE_URL']
        if not key and 'SUPABASE_KEY' in st.secrets:
            key = st.secrets['SUPABASE_KEY']
    except Exception:
        pass
```

**Key Learning**: `st.secrets` uses bracket notation `st.secrets['KEY']`, NOT `.get()` method.

### 2. Hidden Sidebar on Login Page
- Added CSS to `auth.py` to hide sidebar before authentication:
```css
[data-testid="stSidebar"] { display: none !important; }
[data-testid="stSidebarNav"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
```

### 3. Removed Import Page
- Deleted `src/pages/5_Import.py`
- Import functionality remains available via CLI script only

### 4. Added Transaction History Log
- Updated `src/pages/4_Add_Transaction.py` with:
  - Shows last 20 transactions (was 5)
  - Filter by ticker dropdown
  - Filter by type (BUY/SELL)
  - Delete button for each transaction
  - Added `delete_transaction()` function to `supabase_client.py`

### 5. Fixed Chart Overflow on Mobile
- Reduced margins from 70px to 5-50px
- Changed horizontal bar text from `'outside'` to `'inside'`
- Reduced font sizes from 11-12px to 9-10px
- Reduced chart heights for better mobile fit

### 6. Compact Period Filter Buttons
- 480px: height 38px, padding 8px, font 12px
- 375px: height 36px, padding 6px, font 11px

### 7. Improved Data Row Display
- Reduced padding and gaps in `.data-row-mobile`
- Smaller fonts: labels 8px, values 12px (11px on 375px)

### 8. Performance Page Real Data
- Replaced `get_mock_performance()` with `get_portfolio_performance()`
- Replaced `get_mock_asset_performance()` with `get_asset_performance()`
- Uses `portfolio_snapshots` table and `holdings_with_value` view
- Added 5-minute cache TTL

## Completed Steps
1. [x] Create Supabase project and run schema.sql
2. [x] Add Supabase credentials to .env
3. [x] Test locally
4. [x] Push to GitHub (public repo)
5. [x] Deploy to Streamlit Cloud
6. [x] Configure GitHub Actions secrets
7. [x] Connect UI to real Supabase data
8. [x] Verify automated price updates (runs every 4 hours)
9. [x] Implement user authentication
10. [x] Redesign UI with Alpine Dusk theme
11. [x] Add company/crypto logos
12. [x] Configure secrets on Streamlit Cloud
13. [x] Mobile-first responsive redesign
14. [x] Translate Spanish to English
15. [x] Import Delta CSV data (210 transactions)
16. [x] **Fix Supabase connection for Streamlit Cloud**
17. [x] **Hide sidebar on login page**
18. [x] **Remove Import page**
19. [x] **Add transaction history with delete**
20. [x] **Fix chart overflow on mobile**
21. [x] **Compact period filter buttons**
22. [x] **Improve data row display**
23. [x] **Connect Performance page to real data**
24. [ ] Final iPhone testing

## Active Decisions

### Decided
- Stack: Streamlit + Supabase + GitHub Actions + yfinance
- All free tiers
- USD as base currency
- Automatic dividend calculation
- Single-user authentication (email/password in Streamlit secrets)
- Alpine Dusk theme (dark purple gradient, glassmorphism)
- Mobile-first design with 3 breakpoints
- 2x2 grid layouts for metrics (not 4 columns)
- Sidebar collapsed by default on all pages
- All UI text in English
- Repository is PUBLIC (required for Streamlit Cloud free tier)
- **Supabase credentials via st.secrets on Streamlit Cloud**
- **Import via CLI only (no in-app import page)**

### Pending
- Portfolio allocation pie chart
- Performance vs benchmark comparison

## Important Patterns
- Follow minimal intervention principle
- Keep files under 200-300 lines
- Surgical precision over broad changes
- **NEVER commit credentials to public repo**
- Use `apply_styles()` at top of each page
- Use `check_password()` before any page content
- Use 2-column layouts for mobile compatibility
- Always test on iPhone after UI changes
- **Use `st.secrets['KEY']` not `st.secrets.get('KEY')` for Streamlit Cloud**

## Key Files Modified This Session
```
src/app.py                    # Renamed to Home, added logos, render_holding_row with logos
src/utils/styles.py           # Dropdown text size fixes (14px)
```

## Current Session Commits (January 13, 2026)
1. `334c0ab` fix: Date calculation bug causing 'day out of range' error
2. `e55b016` feat: Rename App to Home, add logos to Dashboard, fix dropdown sizes

## Next Actions
1. **Push to GitHub** (2 commits pending)
2. **Test on iPhone** (verify all mobile fixes + new changes)
3. Gather feedback on mobile UX

## Key URLs
- **GitHub Repo**: https://github.com/BenjaDuhart14/Daruma
- **Supabase Project**: https://pvxetjsadcgaeeqmauzz.supabase.co
- **Streamlit Cloud**: https://daruma14.streamlit.app/
- **GitHub Actions**: https://github.com/BenjaDuhart14/Daruma/actions
