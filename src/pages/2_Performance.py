"""
Performance Page - Portfolio performance over time
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

st.set_page_config(
    page_title="Performance - Daruma",
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

    .big-metric {
        font-size: 36px;
        font-weight: 700;
        color: #FAFAFA;
    }

    .gain { color: #4CAF50; }
    .loss { color: #F44336; }
</style>
""", unsafe_allow_html=True)


def get_mock_performance(period: str):
    """Mock performance data - replace with Supabase calls."""
    days_map = {'1D': 1, '1W': 7, '1M': 30, '3M': 90, 'YTD': 180, '1Y': 365, 'ALL': 730}
    days = days_map.get(period, 30)

    np.random.seed(42)
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    base = 75000
    values = base + np.cumsum(np.random.randn(days) * 300)
    values[-1] = 81889.40

    return {
        'dates': dates,
        'values': values,
        'start_value': values[0],
        'end_value': values[-1],
        'change': values[-1] - values[0],
        'change_pct': ((values[-1] - values[0]) / values[0]) * 100,
        'high': max(values),
        'low': min(values)
    }


def get_mock_asset_performance(period: str):
    """Mock per-asset performance."""
    return [
        {'ticker': 'BTC', 'change_pct': 15.5, 'change': 637.50},
        {'ticker': 'TSLA', 'change_pct': 8.2, 'change': 410.00},
        {'ticker': 'ETH', 'change_pct': 5.1, 'change': 225.30},
        {'ticker': 'VOO', 'change_pct': 3.2, 'change': 558.40},
        {'ticker': 'GOOGL', 'change_pct': 2.8, 'change': 80.50},
        {'ticker': 'QQQM', 'change_pct': 1.9, 'change': 100.20},
        {'ticker': 'ARKK', 'change_pct': 0.5, 'change': 24.00},
        {'ticker': 'COST', 'change_pct': -0.3, 'change': -12.90},
        {'ticker': 'AAPL', 'change_pct': -1.2, 'change': -40.50},
        {'ticker': 'AMZN', 'change_pct': -2.1, 'change': -166.20},
    ]


def create_performance_chart(data: dict):
    """Create performance line chart."""
    fig = go.Figure()

    color = '#4CAF50' if data['change'] >= 0 else '#F44336'

    fig.add_trace(go.Scatter(
        x=data['dates'],
        y=data['values'],
        mode='lines',
        line=dict(color=color, width=2),
        fill='tozeroy',
        fillcolor=f'rgba({44 if color == "#4CAF50" else 244}, {175 if color == "#4CAF50" else 67}, {80 if color == "#4CAF50" else 54}, 0.1)',
        hovertemplate='%{x}<br>$%{y:,.2f}<extra></extra>'
    ))

    fig.update_layout(
        plot_bgcolor='#0E1117',
        paper_bgcolor='#0E1117',
        margin=dict(l=0, r=0, t=10, b=40),
        height=300,
        xaxis=dict(showgrid=False, color='#888'),
        yaxis=dict(showgrid=True, gridcolor='#262730', color='#888', tickprefix='$'),
        showlegend=False,
        hovermode='x unified'
    )

    return fig


def create_asset_bar_chart(assets: list):
    """Create horizontal bar chart for asset performance."""
    # Sort by performance
    assets = sorted(assets, key=lambda x: x['change_pct'], reverse=True)

    colors = ['#4CAF50' if a['change_pct'] >= 0 else '#F44336' for a in assets]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=[a['ticker'] for a in assets],
        x=[a['change_pct'] for a in assets],
        orientation='h',
        marker_color=colors,
        text=[f"{'+' if a['change_pct'] >= 0 else ''}{a['change_pct']:.1f}%" for a in assets],
        textposition='outside',
        textfont=dict(size=11)
    ))

    fig.update_layout(
        plot_bgcolor='#1A1A1A',
        paper_bgcolor='#1A1A1A',
        margin=dict(l=60, r=60, t=10, b=10),
        height=400,
        xaxis=dict(showgrid=True, gridcolor='#262730', color='#888', ticksuffix='%'),
        yaxis=dict(showgrid=False, color='#FAFAFA', autorange='reversed'),
        showlegend=False
    )

    return fig


def main():
    st.markdown("### Performance")

    # Period selector
    periods = ['1D', '1W', '1M', '3M', 'YTD', '1Y', 'ALL']

    if 'perf_period' not in st.session_state:
        st.session_state.perf_period = '1M'

    cols = st.columns(len(periods))
    for i, period in enumerate(periods):
        with cols[i]:
            if st.button(period, key=f"perf_{period}",
                        type="primary" if st.session_state.perf_period == period else "secondary",
                        use_container_width=True):
                st.session_state.perf_period = period
                st.rerun()

    st.markdown("---")

    # Get data
    data = get_mock_performance(st.session_state.perf_period)

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        change_color = "green" if data['change'] >= 0 else "red"
        sign = "+" if data['change'] >= 0 else ""
        st.metric(
            "Rendimiento",
            f"{sign}${data['change']:,.2f}",
            f"{sign}{data['change_pct']:.2f}%"
        )

    with col2:
        st.metric("Valor Inicial", f"${data['start_value']:,.2f}")

    with col3:
        st.metric("Valor Actual", f"${data['end_value']:,.2f}")

    with col4:
        st.metric("Maximo", f"${data['high']:,.2f}")

    st.markdown("---")

    # Chart
    st.markdown("#### Evolucion del Portafolio")
    chart = create_performance_chart(data)
    st.plotly_chart(chart, use_container_width=True, config={'displayModeBar': False})

    st.markdown("---")

    # Per-asset performance
    st.markdown("#### Rendimiento por Activo")

    asset_data = get_mock_asset_performance(st.session_state.perf_period)
    bar_chart = create_asset_bar_chart(asset_data)
    st.plotly_chart(bar_chart, use_container_width=True, config={'displayModeBar': False})

    # Table view
    with st.expander("Ver tabla detallada"):
        df = pd.DataFrame(asset_data)
        df['change_pct'] = df['change_pct'].apply(lambda x: f"{'+' if x >= 0 else ''}{x:.2f}%")
        df['change'] = df['change'].apply(lambda x: f"${x:,.2f}")
        df.columns = ['Ticker', 'Cambio %', 'Cambio $']
        st.dataframe(df, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
