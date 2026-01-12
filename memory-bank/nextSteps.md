# Next Steps: Daruma

## Overview
This document outlines the remaining work to have Daruma fully functional as a private, secure investment portfolio tracker optimized for iPhone usage.

**Last Updated**: January 12, 2026

---

## CURRENT SPRINT: Data & UI Fixes - ALL COMPLETE

### Phase 0A: Fix Supabase Connection in Streamlit Cloud
**Status**: COMPLETED
**Priority**: CRITICAL

**Problem**: `supabase_client.py` uses `os.getenv()` but Streamlit Cloud secrets are commented out.

**Solution**:
1. Go to https://share.streamlit.io
2. Find Daruma app -> Settings -> Secrets
3. Add:
```toml
SUPABASE_URL = "https://pvxetjsadcgaeeqmauzz.supabase.co"
SUPABASE_KEY = "your-key-here"
```

---

### Phase 0B: Populate current_prices Table
**Status**: COMPLETED
**Priority**: CRITICAL

**Problem**: `current_prices` table is empty, so `holdings_with_value` view shows NULL values.

**Solution**:
```bash
cd /home/benjaduhart14/investment-tracker
source venv/bin/activate
python src/scripts/update_prices.py
```

Or trigger GitHub Actions manually.

---

### Phase 0C: Fix GitHub Actions Workflow
**Status**: COMPLETED
**Priority**: CRITICAL

**Problem**: Workflow ran 6 minutes ago but nothing happened.

**Investigation**:
- [ ] Check workflow logs at https://github.com/BenjaDuhart14/Daruma/actions
- [ ] Verify SUPABASE_URL and SUPABASE_KEY secrets are set in GitHub
- [ ] Check if yfinance is fetching prices correctly
- [ ] Review any error messages in logs

---

### Phase 1: Hide Sidebar Navigation on Login Page
**Status**: COMPLETED
**Priority**: CRITICAL

**Problem**: Users can see page navigation (Holdings, Performance, etc.) before authenticating.

**Solution**: Add CSS to hide Streamlit's auto-generated sidebar nav on login page:
```css
[data-testid="stSidebarNav"] { display: none; }
```

**Files to modify**:
- `src/utils/auth.py` - Add CSS in `_apply_login_styles()`

---

### Phase 2: Delete Import Page
**Status**: COMPLETED
**Priority**: HIGH

**Problem**: Import functionality should be done via CLI, not exposed in the app.

**Solution**:
```bash
rm src/pages/5_Import.py
```

---

### Phase 3: Add Transaction History Log
**Status**: COMPLETED
**Priority**: HIGH

**Problem**: No way to verify transactions were saved correctly in Add Transaction page.

**Solution**: Add "Recent Transactions" section showing:
- Last 10-20 transactions
- Date, Ticker, Type (BUY/SELL), Quantity, Price
- Delete button for each row
- Filter by ticker

**Files to modify**:
- `src/pages/4_Add_Transaction.py`

---

### Phase 4: Fix Chart Overflow Issues
**Status**: COMPLETED
**Priority**: CRITICAL

**Problem**: Charts have 70px left/right margins, leaving only 235px on 375px screens.

**Solution**:
- Reduce margins to `l=10, r=10` on mobile
- Use `textposition='inside'` for bar labels
- Add responsive margin calculation

**Files to modify**:
- `src/utils/styles.py` - Chart CSS
- `src/app.py` - Dashboard charts
- `src/pages/2_Performance.py` - Performance charts
- `src/pages/3_Dividends.py` - Dividend charts

---

### Phase 5: Mobile-Friendly Period Filters
**Status**: COMPLETED
**Priority**: HIGH

**Problem**: 4-column button layout breaks on mobile (480px = ~114px per button).

**Solution**:
- Use horizontal scrollable container OR
- Reduce to pill-style buttons with smaller padding
- Ensure 44px minimum touch target

**Files to modify**:
- `src/app.py` - Dashboard period selector
- `src/pages/2_Performance.py` - Performance period selector
- `src/utils/styles.py` - Button CSS

---

### Phase 6: Fix Data Row/Card Display on Mobile
**Status**: COMPLETED
**Priority**: MEDIUM

**Problem**: 2-column grid too cramped at 375px width.

**Solution**:
- Stack to 1 column on <375px
- Increase font contrast
- Add proper spacing between items

**Files to modify**:
- `src/utils/styles.py` - `.data-row-mobile` CSS
- `src/pages/1_Holdings.py` - Holdings card layout

---

### Phase 7: Connect Performance Page to Real Data
**Status**: COMPLETED
**Priority**: HIGH

**Problem**: Performance page uses mock data (`get_mock_performance()`), not real portfolio.

**Solution**:
- Replace mock functions with Supabase calls
- Use `portfolio_snapshots` table for historical chart
- Calculate real performance metrics from transactions

**Files to modify**:
- `src/pages/2_Performance.py` - Replace mock data functions

---

## COMPLETED PHASES

### Phase 1 (Old) - Data Import Setup
- Delta CSV import page ready
- Preview and validation before importing
- Duplicate detection working

### Phase 2 (Old) - User Authentication
- Login page with Alpine Dusk theme
- Email/password auth via Streamlit secrets
- All pages protected with `check_password()`
- Logout button in sidebar

### Phase 3 (Old) - UI Redesign (Alpine Dusk Theme)
- 900+ lines of CSS in `styles.py`
- Glassmorphism cards, purple gradients
- Green/red for gains/losses

### Phase 4 (Old) - Mobile-First Responsive Design
- 3 breakpoints: 768px, 480px, 375px
- 2x2 grid layouts for metrics
- Touch-optimized active states

### Phase 5 (Old) - Data Import
- 210 transactions imported from Delta CSV
- 37 unique tickers

---

## FUTURE ENHANCEMENTS

### High Priority
- [ ] Portfolio allocation pie chart
- [ ] Performance vs S&P 500 benchmark
- [ ] Edit/delete transactions

### Medium Priority
- [ ] Export data to CSV
- [ ] Currency toggle (USD/CLP display)
- [ ] Dividend calendar view

### Low Priority
- [ ] Price alerts via email
- [ ] Multiple portfolios support
- [ ] Dark/light theme toggle

---

## Technical Architecture

### File Structure (After Phase 2)
```
src/
├── app.py                    # Main dashboard
├── pages/
│   ├── 1_Holdings.py         # Portfolio holdings with logos
│   ├── 2_Performance.py      # Performance charts (needs real data)
│   ├── 3_Dividends.py        # Dividend tracking
│   └── 4_Add_Transaction.py  # Manual entry + transaction log
└── utils/
    ├── auth.py               # Authentication
    ├── styles.py             # Alpine Dusk design system
    ├── supabase_client.py    # Database operations
    ├── price_fetcher.py      # yfinance integration
    ├── calculations.py       # Portfolio math
    └── delta_parser.py       # CSV parsing
```

### Data Flow
```
transactions (210 records)
    → current_holdings (view)
        → holdings_with_value (view)
            ↑
        current_prices (populated by GitHub Actions)
            ↑
        update_prices.py (runs every 4 hours)
```

---

## Quick Commands

### Local Development
```bash
cd /home/benjaduhart14/investment-tracker
streamlit run src/app.py --server.port 8502
```

### Run Price Update Manually
```bash
cd /home/benjaduhart14/investment-tracker
python src/scripts/update_prices.py
```

### Git Workflow
```bash
git add .
git commit -m "Description of changes"
git push origin main
```

---

## Key URLs
- **Live App**: https://daruma14.streamlit.app/
- **GitHub Repo**: https://github.com/BenjaDuhart14/Daruma
- **GitHub Actions**: https://github.com/BenjaDuhart14/Daruma/actions
- **Supabase**: https://pvxetjsadcgaeeqmauzz.supabase.co
