"""
Holdings Page - List of all assets
"""

import streamlit as st
import pandas as pd
from utils import supabase_client as db

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


def main():
    st.markdown("### Cartera Principal")

    # Filters and sorting
    col1, col2 = st.columns([2, 2])

    with col1:
        sort_by = st.selectbox(
            "Ordenar por",
            ["Valor (Mayor a menor)", "Valor (Menor a mayor)",
             "Ganancia % (Mayor)", "Perdida % (Mayor)",
             "Ticker (A-Z)"],
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
    holdings = get_holdings()

    if not holdings:
        st.info("No holdings found. Import your Delta CSV to get started!")
        return

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
    elif "Ticker" in sort_by:
        holdings = sorted(holdings, key=lambda x: x['ticker'])

    # Display holdings
    for h in holdings:
        col1, col2, col3 = st.columns([2, 2, 2])

        with col1:
            st.markdown(f"**{h['ticker']}**")
            st.caption(f"{h['shares']:.4f} @ ${h['avg_price']:,.2f}")

        with col2:
            st.markdown(f"**${h['current_value']:,.2f}**")
            if h['current_price'] > 0:
                st.caption(f"Price: ${h['current_price']:,.2f}")

        with col3:
            # Total P&L
            pnl_color = "green" if h['pnl_pct'] >= 0 else "red"
            pnl_sign = "+" if h['pnl_pct'] >= 0 else ""
            st.markdown(f":{pnl_color}[{pnl_sign}${h['pnl']:,.2f}]")
            st.caption(f"({pnl_sign}{h['pnl_pct']:.1f}%)")

        st.markdown("---")

    # Summary at bottom
    total_value = sum(h['current_value'] for h in holdings)
    total_cost = sum(h['avg_price'] * h['shares'] for h in holdings)
    total_pnl = total_value - total_cost
    total_pnl_pct = (total_pnl / total_cost) * 100 if total_cost > 0 else 0

    st.markdown("### Resumen")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Activos", len(holdings))

    with col2:
        st.metric("Valor Total", f"${total_value:,.2f}")

    with col3:
        pnl_sign = "+" if total_pnl >= 0 else ""
        st.metric("P&L Total", f"{pnl_sign}${total_pnl:,.2f}", f"{pnl_sign}{total_pnl_pct:.1f}%")


if __name__ == "__main__":
    main()
