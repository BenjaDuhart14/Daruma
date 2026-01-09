# Active Context: Daruma

## Current Focus
Project deployed to GitHub, ready for Streamlit Cloud deployment.

## Recent Changes
- Project fully initialized with all files
- All Streamlit UI pages created based on Delta app screenshots
- Mock data in place for UI testing
- Backend scripts ready (update_prices.py, import_delta_csv.py)
- Supabase database created and schema.sql executed
- .env file configured with Supabase credentials
- Tested locally - Streamlit runs at localhost:8501
- Pushed to GitHub: https://github.com/BenjaDuhart14/Daruma
- Repository is PUBLIC

## Completed Steps
1. [x] Create Supabase project and run schema.sql
2. [x] Add Supabase credentials to .env
3. [x] Test locally (streamlit runs successfully)
4. [x] Push to GitHub (public repo)
5. [ ] Make repo public on GitHub
6. [ ] Deploy to Streamlit Cloud
7. [ ] Configure GitHub Actions secrets
8. [ ] Import Delta CSV data
9. [ ] Verify automated price updates

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
- Caching strategy for Streamlit (st.cache_data)
- Error handling UI for failed price fetches
- Connect UI to real Supabase data (currently mock data)

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
- UI uses mock data - needs Supabase connection
- Ready for Streamlit Cloud deployment
- Security verified: no credentials in repo
