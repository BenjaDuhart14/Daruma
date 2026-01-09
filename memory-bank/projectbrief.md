# Project Brief: Daruma - Investment Portfolio Tracker

## Overview
Personal investment tracking application replicating Delta app functionality. Single-user, cloud-hosted, accessible as PWA from iPhone.

## Core Requirements

### Must Have
- Track investments: ETFs, US stocks, crypto, Chilean stocks
- Currently ~38 assets, but this number can grow over time
- Manual transaction entry (BUY/SELL)
- CSV import from Delta export
- Automatic price updates every 4 hours
- Automatic dividend calculation via yfinance
- Multi-currency support (base: USD)
- Average buy price calculation (weighted)
- P&L tracking ($ and %)
- Performance metrics: 1D, 1W, 1M, 3M, YTD, 1Y, ALL

### Technical Constraints
- All free tiers (Streamlit Cloud, Supabase, GitHub Actions)
- Mobile-first design (iPhone PWA)
- No em-dashes in code/comments
- Simple, maintainable code
- Scalable to handle growing number of assets

## Success Criteria
- 24/7 availability without local PC dependency
- Accurate P&L calculations
- Reliable price updates
- Clean, responsive UI on mobile
