# Active Context: Daruma

## Current Focus
App deployed and connected to Supabase. Waiting for Delta CSV import. Planning user authentication system.

## Recent Changes
- Project fully initialized with all files
- All Streamlit UI pages created based on Delta app screenshots
- UI connected to real Supabase data (no more mock data)
- Backend scripts ready (update_prices.py, import_delta_csv.py)
- Supabase database created and schema.sql executed
- GitHub Actions configured and running (price updates every 4 hours)
- Deployed to Streamlit Cloud: https://daruma14.streamlit.app/
- Repository is PUBLIC

## Completed Steps
1. [x] Create Supabase project and run schema.sql
2. [x] Add Supabase credentials to .env
3. [x] Test locally (streamlit runs successfully)
4. [x] Push to GitHub (public repo)
5. [x] Make repo public on GitHub
6. [x] Deploy to Streamlit Cloud
7. [x] Configure GitHub Actions secrets
8. [x] Connect UI to real Supabase data
9. [x] Verify automated price updates
10. [ ] Import Delta CSV data
11. [ ] Add user authentication (protect portfolio privacy)

## Active Decisions

### Decided
- Stack: Streamlit + Supabase + GitHub Actions + yfinance
- All free tiers
- USD as base currency
- Automatic dividend calculation (not manual)
- Dark theme for UI (matching Delta app)
- UI design: Delta-inspired with dark theme, green/red for gains/losses
- Repository is PUBLIC (required for Streamlit Cloud free tier)

### Pending
- User authentication system (Supabase Auth)
- Row Level Security (RLS) for multi-user support
- UI improvements based on user feedback

## Important Patterns
- Follow minimal intervention principle
- Keep files under 200-300 lines
- Surgical precision over broad changes
- Document path not taken
- Ask for visual references before design changes
- **NEVER commit credentials to public repo**

## Learnings This Session
- WSL path: Windows `C:\Users\...` maps to `/mnt/c/Users/...`
- Streamlit Cloud requires public repo for free tier
- GitHub PAT needs `workflow` scope to push GitHub Actions files
- pip install on modern Debian needs `--break-system-packages` flag
- Git user config needed: name + email (use GitHub noreply email for privacy)

## Current Session Notes
- Full project structure complete
- UI connected to real Supabase data
- App deployed at https://daruma14.streamlit.app/
- GitHub Actions running price updates every 4 hours
- Security verified: no credentials in repo
- Next priority: User authentication for privacy
