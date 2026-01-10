"""
Holdings Page - List of all assets
Alpine Dusk Theme
"""

import streamlit as st
import pandas as pd
from utils import supabase_client as db
from utils.auth import check_password
from utils.styles import apply_styles, section_label, page_header

st.set_page_config(
    page_title="Holdings - Daruma",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Alpine Dusk theme
apply_styles()

# Authentication check
check_password()


@st.cache_data(ttl=300)
def get_holdings():
    """Fetch holdings from Supabase."""
    try:
        client = db.get_client()
        holdings_raw = db.get_holdings_with_value(client)

        holdings = []
        for h in holdings_raw:
            holdings.append({
                'ticker': h['ticker'],
                'name': h['name'] or h['ticker'],
                'shares': float(h['shares'] or 0),
                'avg_price': float(h['avg_buy_price'] or 0),
                'current_price': float(h['current_price'] or 0),
                'current_value': float(h['current_value'] or 0),
                'pnl': float(h['pnl'] or 0),
                'pnl_pct': float(h['pnl_percent'] or 0),
                'type': h['asset_type'] or 'STOCK'
            })
        return holdings
    except Exception as e:
        st.error(f"Error loading holdings: {str(e)}")
        return []


def get_logo_url(ticker: str, asset_type: str) -> str:
    """Get logo URL for a ticker. Returns URL for stocks/ETFs/crypto."""
    ticker_lower = ticker.lower()

    # Crypto logos from CoinGecko CDN (common coins)
    crypto_ids = {
        'btc': 'bitcoin', 'eth': 'ethereum', 'sol': 'solana', 'ada': 'cardano',
        'dot': 'polkadot', 'link': 'chainlink', 'avax': 'avalanche-2', 'matic': 'matic-network',
        'atom': 'cosmos', 'uni': 'uniswap', 'aave': 'aave', 'ltc': 'litecoin',
        'xrp': 'ripple', 'doge': 'dogecoin', 'shib': 'shiba-inu', 'bnb': 'binancecoin',
        'ewt': 'energy-web-token', 'near': 'near', 'algo': 'algorand', 'xlm': 'stellar',
        'vet': 'vechain', 'fil': 'filecoin', 'theta': 'theta-token', 'ftm': 'fantom',
        'sand': 'the-sandbox', 'mana': 'decentraland', 'axs': 'axie-infinity',
    }

    if asset_type == 'CRYPTO' and ticker_lower in crypto_ids:
        coin_id = crypto_ids[ticker_lower]
        return f"https://assets.coingecko.com/coins/images/1/small/{coin_id}.png"

    # For stocks and ETFs, use multiple fallback sources
    # Primary: Financial Modeling Prep (good coverage)
    return f"https://financialmodelingprep.com/image-stock/{ticker.upper()}.png"


def render_holding_card(h: dict):
    """Render a holding as a styled card with logo."""
    is_positive = h['pnl_pct'] >= 0
    pnl_class = "gain" if is_positive else "loss"
    sign = "+" if is_positive else ""
    initials = h['ticker'][:2].upper()

    # Asset type badge colors
    type_colors = {
        'STOCK': '#8b5cf6',
        'FUND': '#06b6d4',
        'CRYPTO': '#f59e0b'
    }
    type_color = type_colors.get(h['type'], '#8b5cf6')

    # Get logo URL
    logo_url = get_logo_url(h['ticker'], h['type'])

    st.markdown(f"""
    <div class="data-row" style="padding: 20px;">
        <div style="display: flex; align-items: center; flex: 2;">
            <div style="
                width: 44px;
                height: 44px;
                border-radius: 12px;
                background: linear-gradient(135deg, {type_color}22 0%, {type_color}11 100%);
                border: 1px solid {type_color}44;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-right: 14px;
                overflow: hidden;
                position: relative;
            ">
                <img
                    src="{logo_url}"
                    alt="{h['ticker']}"
                    style="
                        width: 28px;
                        height: 28px;
                        object-fit: contain;
                        border-radius: 4px;
                    "
                    onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';"
                />
                <div style="
                    display: none;
                    width: 100%;
                    height: 100%;
                    align-items: center;
                    justify-content: center;
                    font-weight: 700;
                    font-size: 14px;
                    color: {type_color};
                    position: absolute;
                    top: 0;
                    left: 0;
                ">{initials}</div>
            </div>
            <div>
                <div class="ticker-name">{h['ticker']}</div>
                <div class="ticker-details">
                    <span style="
                        display: inline-block;
                        padding: 2px 8px;
                        background: {type_color}22;
                        border-radius: 4px;
                        font-size: 10px;
                        color: {type_color};
                        margin-right: 8px;
                    ">{h['type']}</span>
                    {h['shares']:.4f} shares
                </div>
            </div>
        </div>
        <div style="flex: 1; text-align: center;">
            <div style="font-size: 11px; color: var(--text-muted); margin-bottom: 4px;">AVG PRICE</div>
            <div class="value-display">${h['avg_price']:,.2f}</div>
        </div>
        <div style="flex: 1; text-align: center;">
            <div style="font-size: 11px; color: var(--text-muted); margin-bottom: 4px;">CURRENT</div>
            <div class="value-display">${h['current_price']:,.2f}</div>
        </div>
        <div style="flex: 1; text-align: center;">
            <div style="font-size: 11px; color: var(--text-muted); margin-bottom: 4px;">VALUE</div>
            <div class="value-display">${h['current_value']:,.2f}</div>
        </div>
        <div style="flex: 1; text-align: right;">
            <span class="pnl-badge {pnl_class}" style="font-size: 14px;">
                {sign}${h['pnl']:,.2f}<br>
                <span style="font-size: 12px;">({sign}{h['pnl_pct']:.1f}%)</span>
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def main():
    page_header("Holdings", "Your complete portfolio breakdown", "💼")

    # Filters row
    col1, col2, col3 = st.columns([2, 2, 2])

    with col1:
        sort_options = {
            "Value (High to Low)": ("current_value", True),
            "Value (Low to High)": ("current_value", False),
            "Gain % (High)": ("pnl_pct", True),
            "Loss % (High)": ("pnl_pct", False),
            "Ticker (A-Z)": ("ticker", False)
        }
        sort_by = st.selectbox("Sort by", list(sort_options.keys()), label_visibility="collapsed")

    with col2:
        filter_type = st.selectbox("Filter by type", ["All", "Stocks", "Funds", "Crypto"], label_visibility="collapsed")

    with col3:
        search = st.text_input("Search ticker", placeholder="🔍 Search...", label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)

    # Get holdings
    holdings = get_holdings()

    if not holdings:
        st.markdown("""
        <div style="
            text-align: center;
            padding: 80px 20px;
            background: var(--bg-card);
            border-radius: 16px;
            border: 1px dashed var(--border-subtle);
        ">
            <div style="font-size: 64px; margin-bottom: 20px;">💼</div>
            <h3 style="color: var(--text-primary); margin-bottom: 8px;">No Holdings Found</h3>
            <p style="color: var(--text-secondary);">Import your Delta CSV to populate your portfolio.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    # Apply filters
    if filter_type == "Stocks":
        holdings = [h for h in holdings if h['type'] == 'STOCK']
    elif filter_type == "Funds":
        holdings = [h for h in holdings if h['type'] == 'FUND']
    elif filter_type == "Crypto":
        holdings = [h for h in holdings if h['type'] == 'CRYPTO']

    # Apply search
    if search:
        holdings = [h for h in holdings if search.upper() in h['ticker'].upper()]

    # Apply sorting
    sort_key, sort_reverse = sort_options[sort_by]
    holdings = sorted(holdings, key=lambda x: x[sort_key], reverse=sort_reverse)

    # Summary stats
    total_value = sum(h['current_value'] for h in holdings)
    total_cost = sum(h['avg_price'] * h['shares'] for h in holdings)
    total_pnl = total_value - total_cost
    total_pnl_pct = (total_pnl / total_cost) * 100 if total_cost > 0 else 0

    # Stats row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Assets</div>
            <div class="metric-value">{len(holdings)}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Portfolio Value</div>
            <div class="metric-value">${total_value:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Invested</div>
            <div class="metric-value">${total_cost:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        pnl_class = "gain" if total_pnl >= 0 else "loss"
        sign = "+" if total_pnl >= 0 else ""
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total P&L</div>
            <div class="metric-value" style="color: var(--{pnl_class});">{sign}${total_pnl:,.2f}</div>
            <span class="metric-change {pnl_class}">{sign}{total_pnl_pct:.1f}%</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    section_label(f"Assets ({len(holdings)})")

    # Holdings list
    for h in holdings:
        render_holding_card(h)


if __name__ == "__main__":
    main()
