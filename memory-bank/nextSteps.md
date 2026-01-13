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

## NEXT: Day 2 - Chart Enhancements

### Priority Tasks
| # | Task | Description | Complexity |
|---|------|-------------|------------|
| 2.1 | **Dynamic Value Display** | Show value above chart that updates on hover/touch | High |
| 2.2 | **Allocation Donut Chart** | Portfolio breakdown by asset on Home page | Medium |
| 2.3 | **Candlestick Option** | Toggle between line and candlestick on Performance | Medium |
| 2.4 | **High/Low Markers** | Better styled markers on chart | Low |

### Implementation Notes

#### 2.1 Dynamic Value Display
```python
# Add to chart section in app.py
# Display current value that updates on hover
st.markdown(f"""
<div class="chart-value-display">
    <span class="value">${value:,.0f}</span>
    <span class="change {pnl_class}">{sign}{change_pct:.1f}%</span>
</div>
""")
```

#### 2.2 Allocation Donut Chart
```python
# Add to Home page after metrics
fig = go.Figure(data=[go.Pie(
    labels=[h['ticker'] for h in holdings[:8]],
    values=[h['current_value'] for h in holdings[:8]],
    hole=0.65,  # Donut style
    marker=dict(colors=['#8b5cf6', '#06b6d4', ...])
)])
```

---

## FUTURE: Day 3 - Native Feel

### Tasks
| # | Task | Description | Complexity |
|---|------|-------------|------------|
| 3.1 | **Horizontal Period Selector** | Single-row scrolling pills | Medium |
| 3.2 | **Bottom Navigation** | Fixed nav bar at bottom | Medium |
| 3.3 | **Swipe Actions** | Swipe-to-reveal on holdings | High |
| 3.4 | **Animated Counters** | Smooth number transitions | Low |

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
- **Supabase**: https://pvxetjsadcgaeeqmauzz.supabase.co

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
