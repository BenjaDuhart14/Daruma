"""
Holdings Page - List of all assets
"""

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Holdings - Daruma",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .stApp { background-color: #0E1117; }
    header[data-testid="stHeader"] { background-color: #0E1117; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .holding-ticker {
        font-size: 18px;
        font-weight: 600;
        color: #FAFAFA;
    }

    .holding-details {
        font-size: 13px;
        color: #888;
    }

    .holding-value {
        font-size: 18px;
        font-weight: 600;
        color: #FAFAFA;
        text-align: right;
    }

    .gain { color: #4CAF50; }
    .loss { color: #F44336; }
</style>
""", unsafe_allow_html=True)


def get_mock_holdings():
    """Mock data - replace with Supabase calls."""
    return [
        {'ticker': 'VOO', 'name': 'Vanguard S&P 500 ETF', 'shares': 28.18, 'avg_price': 637.14, 'current_price': 637.25, 'current_value': 17956.96, 'daily_change': 86.53, 'daily_pct': 0.48, 'pnl': 3.10, 'pnl_pct': 0.02, 'type': 'FUND'},
        {'ticker': 'AMZN', 'name': 'Amazon', 'shares': 31.39, 'avg_price': 245.93, 'current_price': 245.89, 'current_value': 7719.56, 'daily_change': -11.30, 'daily_pct': -0.15, 'pnl': -1.26, 'pnl_pct': -0.02, 'type': 'STOCK'},
        {'ticker': 'QQQM', 'name': 'Invesco NASDAQ 100', 'shares': 21.01, 'avg_price': 257.28, 'current_price': 257.31, 'current_value': 5406.04, 'daily_change': 38.45, 'daily_pct': 0.72, 'pnl': 0.63, 'pnl_pct': 0.01, 'type': 'FUND'},
        {'ticker': 'TSLA', 'name': 'Tesla', 'shares': 12.19, 'avg_price': 442.71, 'current_price': 442.77, 'current_value': 5397.36, 'daily_change': 84.24, 'daily_pct': 1.59, 'pnl': 0.73, 'pnl_pct': 0.01, 'type': 'STOCK'},
        {'ticker': 'ARKK', 'name': 'ARK Innovation ETF', 'shares': 60, 'avg_price': 80.67, 'current_price': 80.67, 'current_value': 4840.20, 'daily_change': 4.80, 'daily_pct': 0.10, 'pnl': 0.00, 'pnl_pct': 0.00, 'type': 'FUND'},
        {'ticker': 'ETH', 'name': 'Ethereum', 'shares': 1.4897, 'avg_price': 3124.89, 'current_price': 3125.50, 'current_value': 4655.09, 'daily_change': 39.09, 'daily_pct': 0.85, 'pnl': 0.91, 'pnl_pct': 0.02, 'type': 'CRYPTO'},
        {'ticker': 'BTC', 'name': 'Bitcoin', 'shares': 0.05, 'avg_price': 45000, 'current_price': 95000, 'current_value': 4750.00, 'daily_change': 125.00, 'daily_pct': 2.70, 'pnl': 2500.00, 'pnl_pct': 111.11, 'type': 'CRYPTO'},
        {'ticker': 'COST', 'name': 'Costco', 'shares': 4.68, 'avg_price': 922.58, 'current_price': 922.00, 'current_value': 4315.03, 'daily_change': 34.00, 'daily_pct': 0.79, 'pnl': -2.71, 'pnl_pct': -0.06, 'type': 'STOCK'},
        {'ticker': 'AAPL', 'name': 'Apple', 'shares': 12.95, 'avg_price': 257.00, 'current_price': 257.05, 'current_value': 3328.80, 'daily_change': -26.42, 'daily_pct': -0.79, 'pnl': 0.65, 'pnl_pct': 0.02, 'type': 'STOCK'},
        {'ticker': 'GOOGL', 'name': 'Alphabet', 'shares': 8.99, 'avg_price': 329.90, 'current_price': 329.74, 'current_value': 2964.40, 'daily_change': 40.08, 'daily_pct': 1.37, 'pnl': -1.44, 'pnl_pct': -0.05, 'type': 'STOCK'},
    ]


def main():
    st.markdown("### Cartera Principal")

    # Filters and sorting
    col1, col2 = st.columns([2, 2])

    with col1:
        sort_by = st.selectbox(
            "Ordenar por",
            ["Valor (Mayor a menor)", "Valor (Menor a mayor)",
             "Ganancia % (Mayor)", "Perdida % (Mayor)",
             "Cambio diario % (Mayor)", "Ticker (A-Z)"],
            label_visibility="collapsed"
        )

    with col2:
        filter_type = st.selectbox(
            "Filtrar por tipo",
            ["Todos", "Acciones", "Fondos", "Crypto"],
            label_visibility="collapsed"
        )

    st.markdown("---")

    # Get and filter holdings
    holdings = get_mock_holdings()

    # Apply type filter
    if filter_type == "Acciones":
        holdings = [h for h in holdings if h['type'] == 'STOCK']
    elif filter_type == "Fondos":
        holdings = [h for h in holdings if h['type'] == 'FUND']
    elif filter_type == "Crypto":
        holdings = [h for h in holdings if h['type'] == 'CRYPTO']

    # Apply sorting
    if "Valor (Mayor a menor)" in sort_by:
        holdings = sorted(holdings, key=lambda x: x['current_value'], reverse=True)
    elif "Valor (Menor a mayor)" in sort_by:
        holdings = sorted(holdings, key=lambda x: x['current_value'])
    elif "Ganancia %" in sort_by:
        holdings = sorted(holdings, key=lambda x: x['pnl_pct'], reverse=True)
    elif "Perdida %" in sort_by:
        holdings = sorted(holdings, key=lambda x: x['pnl_pct'])
    elif "Cambio diario" in sort_by:
        holdings = sorted(holdings, key=lambda x: x['daily_pct'], reverse=True)
    elif "Ticker" in sort_by:
        holdings = sorted(holdings, key=lambda x: x['ticker'])

    # Display holdings
    for h in holdings:
        col1, col2, col3 = st.columns([2, 2, 2])

        with col1:
            st.markdown(f"**{h['ticker']}**")
            st.caption(f"{h['shares']:.4f} | ${h['avg_price']:,.2f}")

        with col2:
            st.markdown(f"**${h['current_value']:,.2f}**")
            st.caption(f"@ ${h['current_price']:,.2f}")

        with col3:
            # Daily change
            daily_color = "green" if h['daily_pct'] >= 0 else "red"
            daily_sign = "+" if h['daily_pct'] >= 0 else ""
            st.markdown(f":{daily_color}[{daily_sign}${h['daily_change']:,.2f} {daily_sign}{h['daily_pct']:.2f}%]")

            # Total P&L
            pnl_color = "green" if h['pnl_pct'] >= 0 else "red"
            pnl_sign = "+" if h['pnl_pct'] >= 0 else ""
            st.caption(f"P&L: {pnl_sign}${h['pnl']:,.2f} ({pnl_sign}{h['pnl_pct']:.2f}%)")

        st.markdown("---")

    # Summary at bottom
    total_value = sum(h['current_value'] for h in holdings)
    total_daily = sum(h['daily_change'] for h in holdings)
    total_daily_pct = (total_daily / (total_value - total_daily)) * 100 if total_value > total_daily else 0

    st.markdown("### Resumen")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Activos", len(holdings))

    with col2:
        st.metric("Valor Total", f"${total_value:,.2f}")

    with col3:
        daily_sign = "+" if total_daily >= 0 else ""
        st.metric("Cambio Hoy", f"{daily_sign}${total_daily:,.2f}", f"{daily_sign}{total_daily_pct:.2f}%")


if __name__ == "__main__":
    main()
