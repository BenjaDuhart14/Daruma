"""
Ticker mapping between internal format and yfinance format.
"""

# Mapping from internal ticker to yfinance ticker
TICKER_MAPPING = {
    # Crypto - add -USD suffix for yfinance
    'BTC': 'BTC-USD',
    'ETH': 'ETH-USD',
    'DOGE': 'DOGE-USD',
    'SOL': 'SOL-USD',
    'ADA': 'ADA-USD',
    'XRP': 'XRP-USD',
    'AVAX': 'AVAX-USD',
    'DOT': 'DOT-USD',
    'MATIC': 'MATIC-USD',
    'LINK': 'LINK-USD',
    'EWT': 'EWT-USD',  # Energy Web Token
    'AVAIL': 'AVAIL-USD',  # Avail
    'CAKE': 'CAKE-USD',  # PancakeSwap
    'ATOM': 'ATOM-USD',
    'UNI': 'UNI-USD',
    'AAVE': 'AAVE-USD',
    'LTC': 'LTC-USD',
    'BNB': 'BNB-USD',
    'NEAR': 'NEAR-USD',
    'ALGO': 'ALGO-USD',
    'XLM': 'XLM-USD',
    'VET': 'VET-USD',
    'FIL': 'FIL-USD',
    'THETA': 'THETA-USD',
    'FTM': 'FTM-USD',
    'SAND': 'SAND-USD',
    'MANA': 'MANA-USD',
    'AXS': 'AXS-USD',
    'SHIB': 'SHIB-USD',
    # Chilean stocks - add .SN suffix
    'SQM-B': 'SQM-B.SN',
    'BCI': 'BCI.SN',
    'FALABELLA': 'FALABELLA.SN',
    'SANTANDER': 'BSANTANDER.SN',
    'CHILE': 'CHILE.SN',
    'COPEC': 'COPEC.SN',
    'CENCOSUD': 'CENCOSUD.SN',
    'ENELAM': 'ENELAM.SN',
    'CCU': 'CCU.SN',
    # US stocks/ETFs - use as-is (no mapping needed)
}

# Reverse mapping for converting yfinance ticker back to internal
REVERSE_MAPPING = {v: k for k, v in TICKER_MAPPING.items()}


def get_yfinance_ticker(ticker: str) -> str:
    """
    Convert internal ticker to yfinance format.

    Args:
        ticker: Internal ticker symbol (e.g., 'BTC', 'SQM-B')

    Returns:
        yfinance-compatible ticker (e.g., 'BTC-USD', 'SQM-B.SN')
    """
    return TICKER_MAPPING.get(ticker, ticker)


def get_internal_ticker(yfinance_ticker: str) -> str:
    """
    Convert yfinance ticker back to internal format.

    Args:
        yfinance_ticker: yfinance ticker symbol (e.g., 'BTC-USD')

    Returns:
        Internal ticker (e.g., 'BTC')
    """
    return REVERSE_MAPPING.get(yfinance_ticker, yfinance_ticker)


def is_crypto(ticker: str) -> bool:
    """Check if ticker is a cryptocurrency."""
    yf_ticker = get_yfinance_ticker(ticker)
    return yf_ticker.endswith('-USD')


def is_chilean_stock(ticker: str) -> bool:
    """Check if ticker is a Chilean stock."""
    yf_ticker = get_yfinance_ticker(ticker)
    return yf_ticker.endswith('.SN')
