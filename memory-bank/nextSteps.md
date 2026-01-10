# Next Steps: Daruma

## Overview
This document outlines the remaining work to have Daruma fully functional as a private, secure investment portfolio tracker optimized for iPhone usage.

---

## ✅ COMPLETED: Phase 1 - Data Import Setup
- Delta CSV import page ready at /Import
- Preview and validation before importing
- Duplicate detection to prevent re-importing same transactions

---

## ✅ COMPLETED: Phase 2 - User Authentication

### What Was Implemented
- **Login Page**: Beautiful Alpine Dusk themed login with floating logo animation
- **Email/Password Auth**: Credentials stored in Streamlit Cloud secrets
- **All Pages Protected**: `check_password()` called on every page
- **Logout Button**: Available in sidebar
- **Session Management**: Using Streamlit session_state

### How to Configure (For Production)
1. Go to https://share.streamlit.io
2. Find your Daruma app → **Settings** → **Secrets**
3. Add your credentials:
```toml
[auth]
email = "your-email@example.com"
password = "your-secure-password"
```

---

## ✅ COMPLETED: Phase 3 - UI Redesign (Alpine Dusk Theme)

### What Was Implemented
- **Design System** (`styles.py`): 700+ lines of CSS with:
  - Deep purple-to-navy gradient backgrounds
  - Mountain silhouette visual effect
  - Glassmorphism cards with purple glow borders
  - JetBrains Mono for numbers, Plus Jakarta Sans for text
  - Green (#10b981) for gains, Red (#ef4444) for losses
  - Purple (#8b5cf6) and Cyan (#06b6d4) accents

- **Login Page**: Floating logo, aurora glow, Charlie Munger quote
- **Dashboard**: Metric cards, portfolio chart, top movers
- **Holdings**: Company/crypto logos, type-colored badges, P&L display
- **Performance**: Period selector, chart with high/low markers
- **Dividends**: Green-themed, yearly/asset breakdown charts
- **Add Transaction**: Styled form with live calculations
- **Import**: Step-by-step wizard with progress indicators

### Logo Sources
- **Stocks/ETFs**: Financial Modeling Prep API (free)
- **Crypto**: CoinGecko CDN with fallback to initials

---

## 🔄 CURRENT: Phase 4 - Mobile Testing & Deployment

### 4.1 Deploy to Streamlit Cloud
**Status**: Code pushed to GitHub, awaiting deployment

**Steps**:
1. Streamlit Cloud should auto-detect the new commit
2. If not, manually trigger redeployment
3. Configure secrets (see Phase 2 above)

### 4.2 Test on iPhone
**Checklist**:
- [ ] Login page displays correctly
- [ ] Dashboard metrics readable on mobile
- [ ] Charts resize properly
- [ ] Holdings list scrolls smoothly
- [ ] Dropdowns open without being cut off
- [ ] Touch targets are large enough
- [ ] P&L colors visible (green/red)
- [ ] Logos load correctly

### 4.3 Import Delta Data
**Steps**:
1. Export from Delta app: Settings → Export Data → CSV
2. Open Daruma on iPhone: https://daruma14.streamlit.app/Import
3. Upload CSV file
4. Review preview and click "Import Transactions"
5. Verify data in Holdings page

---

## 📋 Phase 5 - Feature Enhancements (Future)

### 5.1 High Priority
- [ ] Portfolio allocation pie chart
- [ ] Performance vs S&P 500 benchmark
- [ ] Edit/delete transactions
- [ ] Pull-to-refresh on mobile

### 5.2 Medium Priority
- [ ] Export data to CSV
- [ ] Currency toggle (USD/CLP display)
- [ ] Target allocation setting
- [ ] Dividend calendar view

### 5.3 Low Priority (Nice to Have)
- [ ] Price alerts via email
- [ ] Multiple portfolios support
- [ ] Dark/light theme toggle
- [ ] Widget for iPhone home screen

---

## 📋 Phase 6 - Performance & Polish (Future)

### 6.1 Caching Optimization
- Current: 5 minute TTL on all cached functions
- Future consideration:
  - Holdings: 5 min
  - Historical data: 1 hour
  - Static data: session-based

### 6.2 Error Handling
- [ ] Graceful fallback when Supabase is down
- [ ] Better error messages for users
- [ ] Retry logic for failed API calls
- [ ] Offline indicator

### 6.3 Testing
- [ ] Unit tests for calculations
- [ ] Edge case testing for Delta CSV parser
- [ ] Authentication flow testing

---

## Technical Architecture

### File Structure
```
src/
├── app.py                    # Main dashboard
├── pages/
│   ├── 1_Holdings.py         # Portfolio holdings with logos
│   ├── 2_Performance.py      # Performance charts
│   ├── 3_Dividends.py        # Dividend tracking
│   ├── 4_Add_Transaction.py  # Manual entry form
│   └── 5_Import.py           # Delta CSV import
└── utils/
    ├── auth.py               # Authentication (login page + check)
    ├── styles.py             # Alpine Dusk design system
    ├── supabase_client.py    # Database operations
    ├── price_fetcher.py      # yfinance integration
    ├── calculations.py       # Portfolio math
    └── delta_parser.py       # CSV parsing
```

### Design System (styles.py)
```python
# Key colors
COLORS = {
    'bg_primary': '#0a0a12',      # Deep navy
    'accent_purple': '#8b5cf6',    # Primary accent
    'accent_cyan': '#06b6d4',      # Secondary accent
    'gain': '#10b981',             # Green for profits
    'loss': '#ef4444',             # Red for losses
}

# Usage in pages
from utils.styles import apply_styles, page_header, section_label
apply_styles()  # Apply CSS
page_header("Title", "Subtitle", "🎯")  # Render header
```

### Authentication Flow
```
User visits any page
    ↓
check_password() called
    ↓
Not authenticated? → Show login page → st.stop()
    ↓
Authenticated? → Continue to page content
    ↓
Logout button → Clear session → Redirect to login
```

---

## Resources

- **Streamlit Docs**: https://docs.streamlit.io
- **Supabase Docs**: https://supabase.com/docs
- **Financial Modeling Prep**: https://financialmodelingprep.com
- **CoinGecko API**: https://www.coingecko.com/en/api

---

## Quick Commands

### Local Development
```bash
cd /home/benjaduhart14/investment-tracker
streamlit run src/app.py --server.port 8502
```

### Git Workflow
```bash
git add .
git commit -m "Description of changes"
git push origin main
```

### View Logs
- GitHub Actions: https://github.com/BenjaDuhart14/Daruma/actions
- Streamlit Cloud: App dashboard → Logs
