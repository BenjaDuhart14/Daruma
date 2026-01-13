# Next Steps: Daruma

## Overview
Daruma is **LIVE** and undergoing **iPhone-First UI Enhancement** inspired by Delta app.

**Last Updated**: January 13, 2026
**Current Phase**: Day 2 - Chart Enhancements

---

## COMPLETED: Day 1 - Core Identity & Quick Add ✅

### What Was Done
| Task | Description | Status |
|------|-------------|--------|
| Daruma Logo | Custom SVG (one eye painted, one empty) | ✅ |
| Home Rename | Dashboard → Home in header | ✅ |
| FAB Button | Floating + button for quick add | ✅ |
| Favicon | Daruma doll in browser tab | ✅ |
| Sidebar Rename | "app" → "Home" via CSS | ✅ |

### Files Created/Modified
- `src/favicon.svg` - NEW
- `src/app.py` - Daruma logo, FAB
- `src/utils/styles.py` - Logo SVG, FAB CSS, sidebar CSS
- All pages - Favicon update

---

## COMPLETED: Phase 2 - Chart Enhancements ✅

### What Was Done
| # | Task | Description | Status |
|---|------|-------------|--------|
| 2.1 | **Dynamic Value Display** | Large value above chart with animations, period change badge | ✅ |
| 2.2 | **Allocation Donut Chart** | Portfolio breakdown by asset (top 8 + Others) | ✅ |

### Features Implemented
- Animated value display with fadeIn/countUp effects
- Period change shown as colored badge (+$X / +X%)
- "Hover chart for details" hint
- Enhanced hover tooltips with styled dark background
- Donut chart with Alpine Dusk color palette
- Center annotation showing total portfolio value

---

## COMPLETED: Phase 3 - Native Feel ✅

### What Was Done
| # | Task | Description | Status |
|---|------|-------------|--------|
| 3.1 | **Horizontal Period Selector** | Single-row scrolling pills with active state | ✅ |
| 3.2 | **Bottom Navigation** | Fixed nav bar with 4 items (Home, Holdings, Stats, Dividends) | ✅ |
| 3.3 | **Animated Counters** | CSS animations with staggered delays | ✅ |

### Features Implemented
- Horizontal scrollable period pills (1D, 1W, 1M, 3M, YTD, 1Y, ALL)
- Bottom nav with emoji icons and active state highlighting
- FAB button repositioned above bottom nav
- Smooth CSS animations on metric values
- Content padding adjusted for bottom nav

---

## Technical Notes

### Git Commands (Always Run at End)
```bash
cd ~/investment-tracker
git add -A
git commit -m "message"
git push origin main
```

### Local Development
```bash
cd ~/investment-tracker
streamlit run src/app.py
```

### Adding New Crypto Tickers
1. Add to `src/utils/ticker_mapping.py`:
   ```python
   'NEWCRYPTO': 'NEWCRYPTO-USD',
   ```
2. Run price update or wait for GitHub Actions
3. Click "Refresh Data" in app

---

## Key URLs
- **Live App**: https://daruma14.streamlit.app/
- **GitHub Repo**: https://github.com/BenjaDuhart14/Daruma
- **GitHub Actions**: https://github.com/BenjaDuhart14/Daruma/actions
- **Supabase**: (see Streamlit Cloud secrets)

---

## Delta App Inspiration Reference

### Chart Features to Replicate
- Drag-to-scrub with vertical cursor line
- Value display updates in real-time on touch
- Period selector as horizontal scrolling pills
- Smooth animations between time periods

### UI Elements to Add
- Allocation breakdown (donut chart)
- "Why Is It Moving?" insights (future)
- Bottom tab navigation
- Pull-to-refresh indicator

---

## Troubleshooting

### App shows old data
→ Click "🔄 Refresh Data" in sidebar

### New crypto shows wrong price
→ Add ticker to `ticker_mapping.py` with `-USD` suffix

### CSS changes not showing
→ Hard refresh (Ctrl+Shift+R) or clear browser cache

### Favicon not updating
→ Clear browser cache or check in incognito mode
