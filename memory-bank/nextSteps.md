# Next Steps: Daruma

## Overview
This document outlines the remaining work to have Daruma fully functional as a private, secure investment portfolio tracker.

---

## Phase 1: Data Import (Current)

### 1.1 Import Delta CSV Data
**Status**: Ready to execute
**How**:
1. Export transactions from Delta app (Settings > Export Data > CSV)
2. Go to https://daruma14.streamlit.app/Import
3. Upload CSV file and click "Importar Transacciones"
4. Verify data appears in Holdings page

### 1.2 Verify Price Updates
**Status**: Automated (GitHub Actions every 4 hours)
**How to verify**:
- Check https://github.com/BenjaDuhart14/Daruma/actions
- After import, prices should update within 4 hours
- Can manually trigger workflow from Actions tab

---

## Phase 2: User Authentication (Priority: HIGH)

### Why This Matters
- Currently anyone with the URL can see your portfolio
- Need to protect sensitive financial data
- Supabase provides built-in authentication

### 2.1 Enable Supabase Auth
**Steps**:
1. Go to Supabase Dashboard > Authentication > Providers
2. Enable Email provider (simplest option)
3. Optionally enable Google/GitHub OAuth for easier login

### 2.2 Database Changes
**Add user_id to tables**:
```sql
-- Add user_id column to transactions
ALTER TABLE transactions ADD COLUMN user_id UUID REFERENCES auth.users(id);

-- Add user_id to other tables
ALTER TABLE dividends ADD COLUMN user_id UUID REFERENCES auth.users(id);
ALTER TABLE portfolio_snapshots ADD COLUMN user_id UUID REFERENCES auth.users(id);
```

### 2.3 Row Level Security (RLS)
**Enable RLS so users only see their own data**:
```sql
-- Enable RLS on transactions
ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see their own transactions
CREATE POLICY "Users can view own transactions" ON transactions
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own transactions" ON transactions
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Repeat for other tables...
```

### 2.4 Update Streamlit App
**Changes needed**:
- Add login page (new file: `src/pages/0_Login.py`)
- Add authentication check to all pages
- Store user session in `st.session_state`
- Pass `user_id` when inserting/querying data

**Login page structure**:
```python
# src/pages/0_Login.py
import streamlit as st
from supabase import create_client

def login_page():
    st.title("Daruma - Login")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            # Supabase auth login
            pass

    with tab2:
        # Registration form
        pass
```

### 2.5 Protect All Pages
**Add to each page**:
```python
# At the top of each page
if 'user' not in st.session_state or not st.session_state.user:
    st.warning("Please login first")
    st.switch_page("pages/0_Login.py")
    st.stop()
```

---

## Phase 3: UI Improvements

### 3.1 Visual Enhancements
- [ ] Add loading spinners during data fetch
- [ ] Improve mobile responsiveness
- [ ] Add portfolio allocation pie chart
- [ ] Add performance comparison vs benchmarks (S&P 500)

### 3.2 Functionality Additions
- [ ] Edit/delete transactions
- [ ] Export data to CSV
- [ ] Set target allocations
- [ ] Price alerts (optional)

### 3.3 UX Improvements
- [ ] Remember last selected period
- [ ] Add search/filter in holdings
- [ ] Improve date range selector
- [ ] Add currency conversion display (USD/CLP)

---

## Phase 4: Performance & Polish

### 4.1 Caching Optimization
- Current: 5 minute TTL on all cached functions
- Consider: Different TTL for different data types
  - Holdings: 5 min
  - Historical data: 1 hour
  - User profile: session-based

### 4.2 Error Handling
- [ ] Graceful degradation when Supabase is down
- [ ] Better error messages for users
- [ ] Retry logic for failed API calls

### 4.3 Testing
- [ ] Add basic unit tests for calculations
- [ ] Test Delta CSV parser with edge cases
- [ ] Test authentication flow

---

## Implementation Order (Recommended)

1. **Import Delta CSV** - Get real data flowing
2. **User Authentication** - Protect your data (CRITICAL)
3. **Basic UI Fixes** - Based on what you notice while using
4. **Polish & Features** - Nice-to-haves

---

## Technical Notes

### Supabase Auth with Streamlit
Streamlit doesn't have built-in session management like traditional web apps. Options:
1. **st.session_state** - Store auth token in session (current recommendation)
2. **streamlit-authenticator** - Third-party library
3. **Custom cookies** - More complex, better persistence

### GitHub Actions & User Data
The price update script will need modification for multi-user:
- Query all unique tickers across all users
- Update prices globally (prices are same for everyone)
- Portfolio snapshots need to be per-user

### Security Checklist
- [ ] RLS enabled on all tables with user data
- [ ] No API keys in client-side code
- [ ] HTTPS only (Streamlit Cloud provides this)
- [ ] Password requirements enforced by Supabase

---

## Questions to Decide

1. **Single user vs Multi-user?**
   - Single: Simpler, just add password protection
   - Multi: Full auth system, more complex

2. **Auth method preference?**
   - Email/password (simplest)
   - Google OAuth (convenient)
   - Magic link (no password to remember)

3. **What UI changes are priority?**
   - Need screenshots or descriptions of desired changes

---

## Resources

- [Supabase Auth Docs](https://supabase.com/docs/guides/auth)
- [Streamlit Session State](https://docs.streamlit.io/library/api-reference/session-state)
- [Row Level Security](https://supabase.com/docs/guides/auth/row-level-security)
