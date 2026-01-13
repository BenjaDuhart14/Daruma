# Active Context: Daruma

## Current Focus
**iPhone-First UI Enhancement Project** - Implementing Delta app-inspired improvements for better mobile UX.

## Recent Changes (This Session - January 13, 2026)

### Day 1 Implementation: Core Identity & Quick Add ✅

#### 1. Daruma Logo Implementation
- Created custom SVG Daruma doll logo (one eye painted, one empty)
- Represents the investment journey: "first $100K is the hardest"
- Logo displays in page headers and sidebar
- Created `src/favicon.svg` for browser tab

#### 2. Page Rename: Dashboard → Home
- Main page now displays "Home" instead of "Dashboard"
- CSS renames "app" to "Home" in sidebar navigation
- Keeps link clickable for navigation back to home

#### 3. Floating Action Button (FAB)
- Purple-to-cyan gradient "+" button
- Fixed position bottom-right
- Links to Add Transaction page
- Pulse animation for visibility
- iPhone safe area support

#### 4. Favicon Update
- Browser tab now shows Daruma doll SVG
- Replaces previous 🎯 bullseye emoji
- Applied to all pages for consistency

---

## Files Modified This Session
```
src/app.py                    # Home rename, Daruma logo, FAB button
src/utils/styles.py           # Daruma SVG, FAB CSS, sidebar rename CSS
src/pages/1_Holdings.py       # Daruma logo in header, favicon
src/pages/2_Performance.py    # Daruma logo in header, favicon
src/pages/3_Dividends.py      # Daruma logo in header, favicon
src/pages/4_Add_Transaction.py # Daruma logo in header, favicon
src/favicon.svg               # NEW - Daruma doll SVG favicon
```

---

## UI Enhancement Plan

### Phase 1: Quick Wins ✅ COMPLETED
- [x] Daruma SVG logo across all pages
- [x] Rename "Dashboard" to "Home"
- [x] FAB (+) button for quick transaction adding
- [x] Daruma favicon in browser tab
- [x] Rename "app" to "Home" in sidebar nav

### Phase 2: Chart Enhancements ✅ COMPLETED
- [x] Dynamic value display above chart with animations
- [x] Portfolio allocation donut chart on Home
- [x] Enhanced hover tooltips

### Phase 3: Native Feel ✅ COMPLETED
- [x] Horizontal scroll period selector (single row pills)
- [x] Bottom navigation bar on all pages
- [x] Animated value counters with staggered delays
- [x] FAB repositioned above bottom nav

---

## Active Decisions

### Design
- Daruma logo: One eye painted (goal set), one empty (goal in progress)
- Alpine Dusk theme: Dark purple/cyan gradient aesthetic
- FAB button: Quick access to add transactions
- Mobile-first: All components optimized for iPhone

### Technical
- SVG favicon requires file (not inline) for Streamlit
- CSS pseudo-elements for sidebar text replacement
- Keep app.py filename for Streamlit Cloud compatibility

---

## Key URLs
- **Live App**: https://daruma14.streamlit.app/
- **GitHub Repo**: https://github.com/BenjaDuhart14/Daruma
- **Supabase**: (see Streamlit Cloud secrets)

---

## Git Commands for This Project
```bash
cd ~/investment-tracker
git add -A
git commit -m "message"
git push origin main
```
