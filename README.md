# Daruma

A personal investment tracker inspired by the Japanese Daruma doll: you paint one eye when setting a goal, the second when you achieve it. Like Munger said, the first $100K is the hardest. Daruma helps you track your portfolio's compound growth, one patient step at a time, until the mountain is built.

## Investment Portfolio Tracker

Track stocks, ETFs, crypto, and Chilean stocks with automatic price updates and dividend tracking. Inspired by the Delta app.

## Features

- Transaction management (manual entry + Delta CSV import)
- Portfolio visualization with P&L
- Performance metrics (1D, 1W, 1M, 3M, YTD, 1Y, ALL)
- Automatic dividend calculation
- Multi-currency support (base: USD)
- Mobile-friendly PWA

## Tech Stack

- **Frontend:** Streamlit Cloud
- **Database:** Supabase (Postgres)
- **Scheduler:** GitHub Actions
- **Price API:** yfinance

## Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd investment-tracker
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up Supabase

1. Create a free account at [supabase.com](https://supabase.com)
2. Create a new project
3. Go to SQL Editor and run the contents of `sql/schema.sql`
4. Get your project URL and anon key from Settings > API

### 5. Configure environment

```bash
cp .env.example .env
# Edit .env with your Supabase credentials
```

### 6. Run locally

```bash
streamlit run src/app.py
```

## Import Delta Data

Export your transactions from Delta app as CSV, then:

```bash
# Preview what will be imported (dry run)
python src/scripts/import_delta_csv.py your_delta_export.csv --dry-run

# Actually import
python src/scripts/import_delta_csv.py your_delta_export.csv
```

## Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set secrets in Streamlit Cloud:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`

## Configure GitHub Actions

Add secrets to your repository (Settings > Secrets and variables > Actions):

- `SUPABASE_URL`
- `SUPABASE_KEY`

The price update workflow runs every 4 hours automatically.

## Project Structure

```
investment-tracker/
├── .github/workflows/     # GitHub Actions
├── src/
│   ├── app.py             # Main Streamlit app
│   ├── pages/             # Streamlit pages
│   ├── utils/             # Utility modules
│   └── scripts/           # Background scripts
├── sql/                   # Database schema
├── memory-bank/           # Project documentation
└── .streamlit/            # Streamlit config
```

## License

Personal use only.
