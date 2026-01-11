# Active Context: Daruma

## Current Focus
Mobile-first responsive redesign complete. All Spanish text translated to English. Delta CSV data imported (210 transactions). Ready for final iPhone testing.

## Recent Changes (This Session - January 11, 2026)

### 1. Mobile-First Responsive Redesign
- Added 3 CSS breakpoints: 768px (tablet), 480px (mobile), 375px (small mobile)
- Changed all pages to collapsed sidebar by default
- Converted 4-column metric layouts to 2x2 grids
- Split 7 period buttons into 4+3 rows for better touch targets
- Created new `.data-row-mobile` CSS class with stacked layout
- Added touch-friendly `:active` states (replaces hover on touch devices)
- Reduced font sizes: 48px to 24px, 32px to 18px on mobile
- Fixed iOS input zoom with 16px minimum font size
- Reduced card padding from 24px to 12-14px on mobile

### 2. Spanish to English Translation
- "Cerrar Sesion" to "Sign Out"
- "Iniciar Sesion" to "Sign In"
- "Email o password incorrectos" to "Incorrect email or password"
- "tu@email.com" to "your@email.com"

### 3. Delta CSV Data Import
- Imported 210 transactions from Delta app
- 37 unique tickers
- Date range: July 2021 to January 2026
- 1 new transaction inserted, 209 duplicates skipped (already existed)

## Completed Steps
1. [x] Create Supabase project and run schema.sql
2. [x] Add Supabase credentials to .env
3. [x] Test locally
4. [x] Push to GitHub (public repo)
5. [x] Deploy to Streamlit Cloud
6. [x] Configure GitHub Actions secrets
7. [x] Connect UI to real Supabase data
8. [x] Verify automated price updates
9. [x] Implement user authentication
10. [x] Redesign UI with Alpine Dusk theme
11. [x] Add company/crypto logos
12. [x] Configure secrets on Streamlit Cloud
13. [x] **Mobile-first responsive redesign**
14. [x] **Translate Spanish to English**
15. [x] **Import Delta CSV data**
16. [ ] Final iPhone testing

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

### Pending
- Portfolio allocation pie chart
- Performance vs benchmark comparison

## Important Patterns
- Follow minimal intervention principle
- Keep files under 200-300 lines
- Surgical precision over broad changes
- Document path not taken
- Ask for visual references before design changes
- **NEVER commit credentials to public repo**
- Use `apply_styles()` at top of each page
- Use `check_password()` before any page content
- Use 2-column layouts for mobile compatibility
- Always test on iPhone after UI changes

## Key Files Modified This Session
```
src/utils/styles.py          # Added 3 mobile breakpoints + helper classes
src/utils/auth.py            # English translations
src/app.py                   # Mobile layouts, 2x2 grids, English
src/pages/1_Holdings.py      # Mobile card layout with stacked details
src/pages/2_Performance.py   # Mobile layout, 4+3 period buttons
src/pages/3_Dividends.py     # Mobile layout
src/pages/4_Add_Transaction.py # Sidebar collapsed
src/pages/5_Import.py        # Mobile layout, 2x2 metrics
```

## Current Session Notes
- Commit `8d425d2`: "fix: Mobile-first responsive redesign + translate Spanish to English"
- 8 files changed, 491 insertions, 185 deletions
- Need to push to GitHub (auth issue in WSL)
- Streamlit Cloud will auto-deploy after push

## Next Actions
1. **Push to GitHub** (manual push needed due to WSL auth)
2. **Test on iPhone** (verify mobile responsiveness after deploy)
3. Gather feedback on mobile UX
4. Iterate on design if needed

## Key URLs
- **GitHub Repo**: https://github.com/BenjaDuhart14/Daruma
- **Supabase Project**: https://pvxetjsadcgaeeqmauzz.supabase.co
- **Streamlit Cloud**: https://daruma14.streamlit.app/
- **GitHub Actions**: https://github.com/BenjaDuhart14/Daruma/actions
