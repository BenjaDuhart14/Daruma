# Active Context: Daruma

## Current Focus
Project code complete - ready for Supabase deployment and testing.

## Recent Changes
- Project fully initialized with all files
- All Streamlit UI pages created based on Delta app screenshots
- Mock data in place for UI testing
- Backend scripts ready (update_prices.py, import_delta_csv.py)

## Next Steps
1. Create Supabase project and run schema.sql
2. Add Supabase credentials to .env
3. Test locally with real database
4. Deploy to Streamlit Cloud
5. Configure GitHub Actions secrets
6. Import Delta CSV data
7. Verify automated price updates

## Active Decisions

### Decided
- Stack: Streamlit + Supabase + GitHub Actions + yfinance
- All free tiers
- USD as base currency
- Automatic dividend calculation (not manual)
- Dark theme for UI (matching Delta app)
- UI design: Delta-inspired with dark theme, green/red for gains/losses

### Pending
- Caching strategy for Streamlit (st.cache_data)
- Error handling UI for failed price fetches

## Important Patterns
- Follow minimal intervention principle
- Keep files under 200-300 lines
- Surgical precision over broad changes
- Document path not taken
- Ask for visual references before design changes

## Current Session Notes
- Full project structure complete
- UI uses mock data - needs Supabase connection
- Ready for deployment phase
