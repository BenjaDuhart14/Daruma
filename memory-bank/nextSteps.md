# Next Steps: Daruma

## Overview
Daruma is now **LIVE and fully functional** as a private investment portfolio tracker optimized for iPhone usage.

**Last Updated**: January 13, 2026
**Status**: PRODUCTION READY

---

## COMPLETED: All Critical Fixes

### January 13, 2026 - Crypto Ticker Fix
**Problem**: EWT (Energy Web Token) showing wrong price ($66.62 instead of $0.81)
- yfinance `EWT` returns iShares Taiwan ETF
- yfinance `EWT-USD` returns Energy Web Token

**Solution**: Updated `ticker_mapping.py` with crypto `-USD` suffix mappings:
```python
'EWT': 'EWT-USD',
'AVAIL': 'AVAIL-USD',
'CAKE': 'CAKE-USD',
# Plus 17 more common crypto tickers
```

**Key Learning**: All crypto tickers need `-USD` suffix for yfinance. When adding new cryptos, always add them to `ticker_mapping.py`.

### January 12, 2026 - Supabase Connection
- Fixed `st.secrets` bracket notation (not `.get()`)
- Supports secrets at root level OR under `[auth]` section

### January 11-12, 2026 - UI/UX Fixes
- Hidden sidebar on login
- Mobile-optimized charts
- Transaction history with delete
- Performance page with real data
- Compact period filter buttons

---

## FUTURE ENHANCEMENTS

### High Priority
| Feature | Description | Complexity |
|---------|-------------|------------|
| Portfolio Allocation Pie Chart | Visual breakdown of holdings by value | Medium |
| S&P 500 Benchmark | Compare performance vs index | Medium |
| Edit Transactions | Modify existing transactions (delete works) | Low |

### Medium Priority
| Feature | Description | Complexity |
|---------|-------------|------------|
| Export to CSV | Download transactions/holdings | Low |
| Currency Toggle | Switch display USD/CLP | Medium |
| Dividend Calendar | Visual calendar of payment dates | Medium |

### Low Priority
| Feature | Description | Complexity |
|---------|-------------|------------|
| Price Alerts | Email notifications for price targets | High |
| Multiple Portfolios | Support separate portfolios | High |
| Dark/Light Toggle | Theme switching | Low |

---

## Technical Notes

### Adding New Crypto Tickers
When importing transactions with a new crypto:
1. Add mapping to `src/utils/ticker_mapping.py`:
   ```python
   'NEWCRYPTO': 'NEWCRYPTO-USD',
   ```
2. Run price update or wait for GitHub Actions
3. Click "Refresh Data" in app

### Streamlit Cloud Secrets Format
```toml
SUPABASE_URL = "https://pvxetjsadcgaeeqmauzz.supabase.co"
SUPABASE_KEY = "your-anon-key"

[auth]
email = "your-email"
password = "your-password"
```

### Data Flow
```
transactions (211 records)
    → current_holdings (view)
        → holdings_with_value (view)
            ↑
        current_prices (GitHub Actions every 4h)
            ↑
        ticker_mapping.py (converts to yfinance format)
```

---

## Quick Commands

### Local Development
```bash
cd /home/benjaduhart14/investment-tracker
streamlit run src/app.py --server.port 8502
```

### Manual Price Update
```bash
cd /home/benjaduhart14/investment-tracker
python src/scripts/update_prices.py
```

### Git Push
```bash
cd /home/benjaduhart14/investment-tracker
git add . && git commit -m "message" && git push origin main
```

---

## Key URLs
- **Live App**: https://daruma14.streamlit.app/
- **GitHub Repo**: https://github.com/BenjaDuhart14/Daruma
- **GitHub Actions**: https://github.com/BenjaDuhart14/Daruma/actions
- **Supabase**: https://pvxetjsadcgaeeqmauzz.supabase.co

---

## Troubleshooting

### App shows old data
→ Click "🔄 Refresh Data" in sidebar

### New crypto shows wrong price
→ Add ticker to `ticker_mapping.py` with `-USD` suffix

### Streamlit Cloud not updating
→ Check GitHub Actions logs, may need to reboot app

### Database connection error
→ Verify secrets in Streamlit Cloud dashboard (Settings → Secrets)
