# Technical Context: Daruma

## Technology Stack

### Frontend
- **Streamlit Cloud** (free tier)
  - Python-based web framework
  - Auto-deploys from GitHub
  - Sleeps after ~15 min inactivity (wakes on access)
  - Multi-page app support

### Database
- **Supabase** (free tier, Postgres)
  - 500MB storage
  - REST API + Python client
  - Row-level security available

### Scheduler
- **GitHub Actions** (free tier)
  - 2000 minutes/month
  - Cron-based scheduling
  - Runs every 4 hours

### APIs
- **yfinance** (Python library)
  - Unofficial Yahoo Finance API
  - Free, no key required
  - May have rate limits/failures
  - Needs retry logic with backoff

- **Exchange Rate API** (or similar)
  - USD/CLP conversion primarily
  - Free tier available

## Development Setup
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env
# Edit .env with Supabase credentials
streamlit run src/app.py
```

## Dependencies
- streamlit>=1.28.0
- supabase>=2.0.0
- yfinance>=0.2.30
- pandas>=2.0.0
- plotly>=5.18.0
- python-dotenv>=1.0.0
- requests>=2.31.0

## Environment Variables
- `SUPABASE_URL`: Supabase project URL
- `SUPABASE_KEY`: Supabase anon/service key

## Ticker Mapping
Special handling required for:
- **Crypto**: Add `-USD` suffix (BTC -> BTC-USD)
- **Chilean stocks**: Add `.SN` suffix (BCI -> BCI.SN)
- **Standard US stocks/ETFs**: Use as-is

## Known Technical Constraints
- yfinance is unofficial - implement retry with exponential backoff
- Chilean stocks (.SN) may have less coverage
- Streamlit Cloud sleeps after inactivity
- Free tier limits on all services
