# Daruma Project Handoff

## Quick Start for New Claude Instance

**Read this first, then read the memory-bank files.**

---

## Project Location
```
/home/benjaduhart14/investment-tracker/
```

## What Is This?
Daruma is a personal investment portfolio tracker inspired by the Delta app. It tracks stocks, ETFs, crypto, and Chilean stocks with automatic price updates and dividend tracking.

**Live App**: https://daruma14.streamlit.app/
**GitHub Repo**: https://github.com/BenjaDuhart14/Daruma

---

## Tech Stack
- **Frontend**: Streamlit (Python)
- **Database**: Supabase (PostgreSQL)
- **Price Updates**: GitHub Actions (every 4 hours) + yfinance
- **Hosting**: Streamlit Cloud (free tier)

---

## Current State: WORKING
- [x] Full project structure created
- [x] Database schema deployed to Supabase
- [x] UI connected to real Supabase data
- [x] GitHub Actions running price updates
- [x] Deployed to Streamlit Cloud
- [ ] **PENDING**: Import Delta CSV data (user action)
- [ ] **PENDING**: Add authentication (next coding task)
- [ ] **PENDING**: UI improvements

---

## CRITICAL: Read These Files First

### Memory Bank (Project Documentation)
```
memory-bank/
├── projectbrief.md      # What we're building, requirements
├── productContext.md    # Product decisions, UX patterns
├── techContext.md       # Tech stack, environment setup, SECURITY WARNINGS
├── systemPatterns.md    # Code patterns, architecture decisions
├── activeContext.md     # Current focus, recent changes
├── progress.md          # What's done, what's left
└── nextSteps.md         # DETAILED ROADMAP - READ THIS FOR NEXT TASKS
```

### Key Source Files
```
src/
├── app.py                    # Main dashboard
├── pages/
│   ├── 1_Holdings.py         # Holdings list
│   ├── 2_Performance.py      # Performance metrics
│   ├── 3_Dividends.py        # Dividend tracking
│   ├── 4_Add_Transaction.py  # Manual transaction entry
│   └── 5_Import.py           # Delta CSV import
├── utils/
│   ├── supabase_client.py    # Database operations
│   ├── ticker_mapping.py     # Ticker symbol mapping
│   ├── price_fetcher.py      # yfinance wrapper
│   ├── calculations.py       # P&L calculations
│   └── delta_parser.py       # CSV parser
└── scripts/
    ├── update_prices.py      # GitHub Actions script
    └── import_delta_csv.py   # CLI import script
```

---

## SECURITY - DO NOT BREAK

**This is a PUBLIC repository.** Never commit:
- `.env` files
- API keys or tokens
- Passwords or secrets
- The Supabase credentials

**Credentials are stored in:**
- Local: `.env` file (gitignored)
- Streamlit Cloud: Secrets settings
- GitHub Actions: Repository secrets

---

## Next Task: Authentication

**Decision Made**: Single user with email/password

**Implementation Plan** (from `memory-bank/nextSteps.md`):

1. Create `src/utils/auth.py` with login check function
2. Add credentials to Streamlit Cloud secrets:
   ```toml
   [auth]
   email = "user-email"
   password = "user-password"
   ```
3. Add `check_password()` call to TOP of every page file
4. Add logout button to sidebar

**The full code is already written in `nextSteps.md` - just implement it.**

---

## Important Patterns

1. **Minimal intervention** - Don't refactor code that works
2. **Keep files under 300 lines** - Split if needed
3. **Ask for visuals** - Before any UI design changes, ask user for screenshots/examples
4. **st.cache_data** - Use 5 min TTL for database queries
5. **Never commit secrets** - Always check before committing

---

## Database Schema

Tables: `transactions`, `price_history`, `current_prices`, `fx_rates`, `current_fx_rates`, `dividends`, `portfolio_snapshots`

Views: `current_holdings`, `holdings_with_value`, `dividend_summary`, `dividends_by_year`, `portfolio_summary`

Full schema in: `sql/schema.sql`

---

## Commands

```bash
# Run locally
cd /home/benjaduhart14/investment-tracker
streamlit run src/app.py

# Git push (need PAT token)
git push origin main

# Test price update script
python src/scripts/update_prices.py
```

---

## User Preferences

- Dark theme (Delta app style)
- Spanish labels in UI (Cartera, Dividendos, etc.)
- Green for gains, red for losses
- USD as base currency
- Single user (no multi-tenant)

---

## Start Here

1. Read `memory-bank/nextSteps.md` - has the full implementation plan
2. Read `memory-bank/progress.md` - current status
3. Implement authentication (Phase 2 in nextSteps.md)
4. Wait for user to import Delta CSV before testing with real data
