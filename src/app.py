"""
Daruma - Investment Portfolio Tracker
Main Dashboard
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd

# Page config
st.set_page_config(
    page_title="Daruma",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Delta-like dark theme
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #0E1117;
    }

    /* Hide default header */
    header[data-testid="stHeader"] {
        background-color: #0E1117;
    }

    /* Large value display */
    .big-value {
        font-size: 48px;
        font-weight: 700;
        color: #FAFAFA;
        margin: 0;
        line-height: 1.2;
    }

    .currency-label {
        font-size: 20px;
        color: #888;
        margin-left: 8px;
    }

    /* Gain/Loss colors */
    .gain {
        color: #4CAF50;
        font-weight: 600;
    }

    .loss {
        color: #F44336;
        font-weight: 600;
    }

    /* Period selector pills */
    .period-pill {
        display: inline-block;
        padding: 8px 16px;
        margin: 4px;
        border-radius: 20px;
        background-color: #262730;
        color: #FAFAFA;
        cursor: pointer;
    }

    .period-pill.active {
        background-color: #4CAF50;
    }

    /* Filter chips */
    .filter-chip {
        display: inline-block;
        padding: 6px 14px;
        margin: 4px;
        border-radius: 16px;
        border: 1px solid #444;
        background-color: transparent;
        color: #FAFAFA;
        font-size: 14px;
    }

    /* Card container */
    .metric-card {
        background-color: #1E1E1E;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
    }

    /* Asset row */
    .asset-row {
        background-color: #1A1A1A;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 8px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* Section title */
    .section-title {
        color: #888;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }

    .section-header {
        color: #FAFAFA;
        font-size: 20px;
        font-weight: 600;
        margin-bottom: 16px;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Metric styling */
    [data-testid="stMetricValue"] {
        font-size: 28px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'selected_period' not in st.session_state:
    st.session_state.selected_period = '1D'

if 'selected_filters' not in st.session_state:
    st.session_state.selected_filters = []


def get_mock_data():
    """Return mock data for UI development. Replace with Supabase calls."""
    return {
        'total_value': 81889.40,
        'total_cost': 75000.00,
        'daily_change': 339.93,
        'daily_change_pct': 0.42,
        'holdings': [
            {'ticker': 'VOO', 'name': 'Vanguard S&P 500 ETF', 'shares': 28.18, 'avg_price': 637.14, 'current_value': 17956.96, 'daily_change': 86.53, 'daily_pct': 0.48, 'type': 'FUND'},
            {'ticker': 'AMZN', 'name': 'Amazon', 'shares': 31.39, 'avg_price': 245.93, 'current_value': 7719.56, 'daily_change': -11.30, 'daily_pct': -0.15, 'type': 'STOCK'},
            {'ticker': 'QQQM', 'name': 'Invesco NASDAQ 100', 'shares': 21.01, 'avg_price': 257.28, 'current_value': 5406.04, 'daily_change': 38.45, 'daily_pct': 0.72, 'type': 'FUND'},
            {'ticker': 'TSLA', 'name': 'Tesla', 'shares': 12.19, 'avg_price': 442.71, 'current_value': 5397.36, 'daily_change': 84.24, 'daily_pct': 1.59, 'type': 'STOCK'},
            {'ticker': 'ARKK', 'name': 'ARK Innovation ETF', 'shares': 60, 'avg_price': 80.67, 'current_value': 4840.20, 'daily_change': 4.80, 'daily_pct': 0.10, 'type': 'FUND'},
            {'ticker': 'ETH', 'name': 'Ethereum', 'shares': 1.4897, 'avg_price': 3124.89, 'current_value': 4655.09, 'daily_change': 39.09, 'daily_pct': 0.85, 'type': 'CRYPTO'},
            {'ticker': 'BTC', 'name': 'Bitcoin', 'shares': 0.05, 'avg_price': 45000, 'current_value': 4750.00, 'daily_change': 125.00, 'daily_pct': 2.70, 'type': 'CRYPTO'},
        ]
    }


def create_portfolio_chart(period: str):
    """Create portfolio evolution line chart."""
    # Mock data - replace with actual price history
    days = {'1H': 0.04, '1D': 1, '1W': 7, '1M': 30, '3M': 90, 'YTD': 180, '1Y': 365, 'ALL': 730}
    num_points = max(20, int(days.get(period, 30) * 2))

    dates = pd.date_range(end=datetime.now(), periods=num_points, freq='H' if period == '1H' else 'D')

    # Simulated values with some variation
    import numpy as np
    np.random.seed(42)
    base = 81000
    values = base + np.cumsum(np.random.randn(num_points) * 200)
    values[-1] = 81889.40  # End at current value

    fig = go.Figure()

    # Determine color based on trend
    color = '#4CAF50' if values[-1] >= values[0] else '#F44336'

    fig.add_trace(go.Scatter(
        x=dates,
        y=values,
        mode='lines',
        line=dict(color=color, width=2),
        fill='tozeroy',
        fillcolor=f'rgba({44 if color == "#4CAF50" else 244}, {175 if color == "#4CAF50" else 67}, {80 if color == "#4CAF50" else 54}, 0.1)',
        hovertemplate='$%{y:,.2f}<extra></extra>'
    ))

    # Add min/max annotations
    max_val = max(values)
    min_val = min(values)
    max_idx = list(values).index(max_val)
    min_idx = list(values).index(min_val)

    fig.add_annotation(x=dates[max_idx], y=max_val, text=f'${max_val:,.2f}',
                      showarrow=False, yshift=15, font=dict(size=11, color='#888'))
    fig.add_annotation(x=dates[min_idx], y=min_val, text=f'${min_val:,.2f}',
                      showarrow=False, yshift=-15, font=dict(size=11, color='#888'))

    fig.update_layout(
        plot_bgcolor='#0E1117',
        paper_bgcolor='#0E1117',
        margin=dict(l=0, r=0, t=10, b=0),
        height=250,
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        showlegend=False,
        hovermode='x unified'
    )

    return fig


def create_movers_chart(holdings: list, top_n: int = 5, show_gainers: bool = True):
    """Create bar chart for top gainers or losers."""
    sorted_holdings = sorted(holdings, key=lambda x: x['daily_pct'], reverse=show_gainers)

    if show_gainers:
        movers = [h for h in sorted_holdings if h['daily_pct'] > 0][:top_n]
        color = '#4CAF50'
    else:
        movers = [h for h in sorted_holdings if h['daily_pct'] < 0][:top_n]
        movers = sorted(movers, key=lambda x: x['daily_pct'])  # Most negative first
        color = '#F44336'

    if not movers:
        return None

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=[m['ticker'] for m in movers],
        y=[abs(m['daily_pct']) for m in movers],
        marker_color=color,
        text=[f"{'+' if m['daily_pct'] > 0 else ''}{m['daily_pct']:.2f}%" for m in movers],
        textposition='outside',
        textfont=dict(color=color, size=12)
    ))

    fig.update_layout(
        plot_bgcolor='#1A1A1A',
        paper_bgcolor='#1A1A1A',
        margin=dict(l=10, r=10, t=30, b=40),
        height=200,
        xaxis=dict(showgrid=False, color='#888'),
        yaxis=dict(showgrid=False, showticklabels=False),
        showlegend=False,
        bargap=0.3
    )

    return fig


# Main app
def main():
    data = get_mock_data()

    # Header
    st.markdown("### Portfolios")

    # Asset type filters
    col1, col2, col3, col4 = st.columns([1, 1, 1, 3])
    with col1:
        crypto_filter = st.checkbox("Crypto", key="crypto")
    with col2:
        stocks_filter = st.checkbox("Acciones", key="stocks")
    with col3:
        funds_filter = st.checkbox("Fondos", key="funds")

    st.markdown("---")

    # Total value display
    st.markdown('<p class="section-title">Valor total</p>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col1:
        change_class = "gain" if data['daily_change'] >= 0 else "loss"
        sign = "+" if data['daily_change'] >= 0 else ""

        st.markdown(f"""
        <p class="big-value">{data['total_value']:,.2f}<span class="currency-label">USD</span></p>
        <p class="{change_class}">{sign}{data['daily_change']:,.2f} {sign}{data['daily_change_pct']:.2f}%</p>
        """, unsafe_allow_html=True)

    # Portfolio chart
    chart = create_portfolio_chart(st.session_state.selected_period)
    st.plotly_chart(chart, use_container_width=True, config={'displayModeBar': False})

    # Period selector
    periods = ['1H', '1D', '1W', '1M', 'YTD', '1Y', 'ALL']
    cols = st.columns(len(periods))
    for i, period in enumerate(periods):
        with cols[i]:
            if st.button(period, key=f"period_{period}",
                        type="primary" if st.session_state.selected_period == period else "secondary",
                        use_container_width=True):
                st.session_state.selected_period = period
                st.rerun()

    st.markdown("---")

    # Daily movers section
    st.markdown('<p class="section-title">PERMANECE EN LA CIMA</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Top Gainers**")
        gainers_chart = create_movers_chart(data['holdings'], show_gainers=True)
        if gainers_chart:
            st.plotly_chart(gainers_chart, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("No gainers today")

    with col2:
        st.markdown("**Top Losers**")
        losers_chart = create_movers_chart(data['holdings'], show_gainers=False)
        if losers_chart:
            st.plotly_chart(losers_chart, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("No losers today")

    st.markdown("---")

    # Quick holdings preview
    st.markdown('<p class="section-title">TOP HOLDINGS</p>', unsafe_allow_html=True)

    # Sort by value
    sorted_holdings = sorted(data['holdings'], key=lambda x: x['current_value'], reverse=True)[:5]

    for h in sorted_holdings:
        col1, col2, col3 = st.columns([2, 2, 2])

        with col1:
            st.markdown(f"**{h['ticker']}**")
            st.caption(f"{h['shares']:.2f} | ${h['avg_price']:,.2f}")

        with col2:
            st.markdown(f"${h['current_value']:,.2f}")

        with col3:
            change_color = "green" if h['daily_pct'] >= 0 else "red"
            sign = "+" if h['daily_pct'] >= 0 else ""
            st.markdown(f":{change_color}[{sign}${h['daily_change']:,.2f} {sign}{h['daily_pct']:.2f}%]")

        st.markdown("---")


if __name__ == "__main__":
    main()
