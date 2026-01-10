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

### Decision: SINGLE USER
Simple password protection using Streamlit secrets. No database changes needed.

### Why This Approach
- Currently anyone with the URL can see your portfolio
- Single user = simple password gate
- Password stored securely in Streamlit Cloud secrets
- No database modifications required
- Quick to implement

### 2.1 Add Credentials to Streamlit Secrets
**In Streamlit Cloud**:
1. Go to https://share.streamlit.io
2. Click on your Daruma app > Settings > Secrets
3. Add:
```toml
[auth]
email = "your-email@example.com"
password = "your-secure-password-here"
```

### 2.2 Create Auth Helper
**New file: `src/utils/auth.py`**
```python
import streamlit as st

def check_password():
    """Returns True if user entered correct email and password."""

    def credentials_entered():
        if (st.session_state["login_email"] == st.secrets["auth"]["email"] and
            st.session_state["login_password"] == st.secrets["auth"]["password"]):
            st.session_state["authenticated"] = True
            del st.session_state["login_password"]  # Don't store password
        else:
            st.session_state["authenticated"] = False

    if "authenticated" not in st.session_state:
        st.markdown("### Login to Daruma")
        st.text_input("Email", key="login_email")
        st.text_input("Password", type="password", key="login_password")
        st.button("Login", on_click=credentials_entered)
        st.stop()

    if not st.session_state.get("authenticated"):
        st.markdown("### Login to Daruma")
        st.text_input("Email", key="login_email")
        st.text_input("Password", type="password", key="login_password")
        st.button("Login", on_click=credentials_entered)
        st.error("Invalid email or password")
        st.stop()

    return True
```

### 2.3 Protect All Pages
**Add to the TOP of each page file** (app.py and all pages/*.py):
```python
from utils.auth import check_password
check_password()  # Will stop execution if not authenticated
```

### 2.4 Optional: Add Logout Button
**Add to sidebar in app.py**:
```python
with st.sidebar:
    if st.button("Logout"):
        st.session_state["authenticated"] = False
        st.rerun()
```

### Implementation Checklist
- [ ] Create `src/utils/auth.py`
- [ ] Add password to Streamlit Cloud secrets
- [ ] Add `check_password()` to app.py
- [ ] Add `check_password()` to all page files
- [ ] Add logout button to sidebar
- [ ] Test locally with `.streamlit/secrets.toml`

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

1. ~~**Single user vs Multi-user?**~~ **DECIDED: Single user**

2. ~~**Auth method preference?**~~ **DECIDED: Email/password (Streamlit secrets)**

3. **What UI changes are priority?**
   - Need screenshots or descriptions of desired changes
   - Will collect feedback after using the app with real data

---

## Resources

- [Supabase Auth Docs](https://supabase.com/docs/guides/auth)
- [Streamlit Session State](https://docs.streamlit.io/library/api-reference/session-state)
- [Row Level Security](https://supabase.com/docs/guides/auth/row-level-security)
