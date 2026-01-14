"""
Holdings Page - List of all assets
Alpine Dusk Theme
"""

import streamlit as st
import pandas as pd
from utils import supabase_client as db
from utils.auth import check_password
from utils.styles import apply_styles, section_label, page_header, get_daruma_logo, render_bottom_nav, render_fab_button

st.set_page_config(
    page_title="Holdings - Daruma",
    page_icon="src/favicon.svg",
    layout="wide",
    initial_sidebar_state="collapsed"
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
    ticker_upper = ticker.upper()

    # Crypto logos from CoinCap (uses symbols directly)
    if asset_type == 'CRYPTO':
        return f"https://assets.coincap.io/assets/icons/{ticker_lower}@2x.png"

    # For stocks and ETFs, use Financial Modeling Prep
    return f"https://financialmodelingprep.com/image-stock/{ticker_upper}.png"


def render_holding_card(h: dict):
    """Render a holding as a mobile-friendly card with logo."""
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
    logo_url = get_logo_url(h['ticker'], h['type'])

    # Mobile-friendly stacked card layout
    st.markdown(f"""
    <div class="data-row-mobile">
        <div class="row-header">
            <div class="row-left">
                <div style="
                    width: 36px;
                    height: 36px;
                    border-radius: 10px;
                    background: linear-gradient(135deg, {type_color}22 0%, {type_color}11 100%);
                    border: 1px solid {type_color}44;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    overflow: hidden;
                    position: relative;
                    flex-shrink: 0;
                ">
                    <img src="{logo_url}" alt="{h['ticker']}" style="width: 22px; height: 22px; object-fit: contain;"
                        onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';"/>
                    <div style="display: none; width: 100%; height: 100%; align-items: center; justify-content: center;
                        font-weight: 700; font-size: 11px; color: {type_color}; position: absolute; top: 0; left: 0;">{initials}</div>
                </div>
                <div>
                    <div class="ticker-name">{h['ticker']}</div>
                    <div class="ticker-details">
                        <span style="padding: 1px 6px; background: {type_color}22; border-radius: 4px; font-size: 9px; color: {type_color};">{h['type']}</span>
                        <span style="margin-left: 6px;">{h['shares']:.2f} shares</span>
                    </div>
                </div>
            </div>
            <span class="pnl-badge {pnl_class}">{sign}{h['pnl_pct']:.1f}%</span>
        </div>
        <div class="row-details">
            <div class="detail-item">
                <div class="detail-label">Avg Price</div>
                <div class="detail-value">${h['avg_price']:,.2f}</div>
            </div>
            <div class="detail-item">
                <div class="detail-label">Current</div>
                <div class="detail-value">${h['current_price']:,.2f}</div>
            </div>
            <div class="detail-item">
                <div class="detail-label">Value</div>
                <div class="detail-value">${h['current_value']:,.0f}</div>
            </div>
            <div class="detail-item">
                <div class="detail-label">P&L</div>
                <div class="detail-value" style="color: var(--{pnl_class});">{sign}${h['pnl']:,.0f}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def main():
    # Page header with Daruma logo
    daruma_header = get_daruma_logo(32)
    st.markdown(f"""
    <div class="page-title">
        <span class="daruma-logo">{daruma_header}</span>
        Holdings
    </div>
    <p class="page-subtitle">Your complete portfolio breakdown</p>
    """, unsafe_allow_html=True)

    # Filters - 2 columns for better mobile display
    sort_options = {
        "Value (High to Low)": ("current_value", True),
        "Value (Low to High)": ("current_value", False),
        "Gain % (High)": ("pnl_pct", True),
        "Loss % (High)": ("pnl_pct", False),
        "Ticker (A-Z)": ("ticker", False)
    }

    col1, col2 = st.columns(2)
    with col1:
        sort_by = st.selectbox("Sort by", list(sort_options.keys()))
    with col2:
        filter_type = st.selectbox("Filter", ["All", "Stocks", "Funds", "Crypto"])

    search = st.text_input("Search", placeholder="Search ticker...")

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

    # Stats - 2x2 grid for mobile
    pnl_class = "gain" if total_pnl >= 0 else "loss"
    sign = "+" if total_pnl >= 0 else ""

    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Assets</div>
            <div class="metric-value">{len(holdings)}</div>
        </div>
        """, unsafe_allow_html=True)

    with row1_col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Value</div>
            <div class="metric-value">${total_value:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    row2_col1, row2_col2 = st.columns(2)
    with row2_col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Invested</div>
            <div class="metric-value">${total_cost:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    with row2_col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">P&L</div>
            <div class="metric-value" style="color: var(--{pnl_class});">{sign}${total_pnl:,.0f}</div>
            <span class="metric-change {pnl_class}">{sign}{total_pnl_pct:.1f}%</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    section_label(f"Assets ({len(holdings)})")

    # Holdings list
    for h in holdings:
        render_holding_card(h)
    
    # Floating Action Button
    render_fab_button()
    
    # Bottom Navigation Bar
    render_bottom_nav(active_page="holdings")


if __name__ == "__main__":
    main()
