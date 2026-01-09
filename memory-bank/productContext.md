# Product Context: Daruma

## Why This Project Exists
The user needs a personal investment tracker that:
- Replicates Delta app functionality
- Runs in the cloud 24/7
- Is accessible from iPhone as PWA
- Costs nothing to operate (free tiers only)

## Problems It Solves
1. **Centralized tracking**: All investments (stocks, ETFs, crypto, Chilean stocks) in one place
2. **Performance visibility**: Clear P&L metrics across different time periods
3. **Dividend tracking**: Automatic calculation of dividends received
4. **Mobile access**: Quick portfolio checks from iPhone
5. **Historical data**: Track portfolio evolution over time

## User Experience Goals
- **Fast**: Quick loading, responsive UI
- **Clear**: Easy to understand P&L at a glance
- **Accurate**: Reliable price data and calculations
- **Simple**: Minimal clicks to add transactions or view data

## Key User Flows
1. **Daily check**: Open app, see total value and daily change
2. **Add transaction**: Quick form to log buys/sells
3. **Review performance**: Check P&L by period
4. **Track dividends**: See income received over time
5. **Import history**: Bulk import from Delta CSV

## Design Process
**IMPORTANT**: When design decisions are needed (UI layout, colors, component styling, etc.), ask the user for pictures or images of what they want. The user will provide visual examples to guide the design.

## Design Principles
- Mobile-first layout
- Green = profit, Red = loss (universal convention)
- Prominent total value display
- Sortable/filterable tables
- Dark theme (Streamlit default)
- Always request visual references before making design choices
