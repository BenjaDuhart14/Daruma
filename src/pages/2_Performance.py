"""
Performance Page - Portfolio performance over time
Alpine Dusk Theme
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import numpy as np
from utils.auth import check_password
from utils.styles import apply_styles, section_label, page_header, get_chart_layout, CHART_COLORS

st.set_page_config(
    page_title="Performance - Daruma",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Alpine Dusk theme
apply_styles()

# Authentication check
check_password()


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
    """Create performance line chart with Alpine Dusk styling."""
    fig = go.Figure()

    is_positive = data['change'] >= 0
    line_color = CHART_COLORS['gain'] if is_positive else CHART_COLORS['loss']
    fill_color = 'rgba(16, 185, 129, 0.1)' if is_positive else 'rgba(239, 68, 68, 0.1)'

    fig.add_trace(go.Scatter(
        x=data['dates'],
        y=data['values'],
        mode='lines',
        line=dict(color=line_color, width=2.5),
        fill='tozeroy',
        fillcolor=fill_color,
        hovertemplate='%{x|%b %d}<br><b>$%{y:,.2f}</b><extra></extra>'
    ))

    # Add high/low markers
    max_idx = list(data['values']).index(data['high'])
    min_idx = list(data['values']).index(data['low'])

    fig.add_trace(go.Scatter(
        x=[data['dates'][max_idx]],
        y=[data['high']],
        mode='markers+text',
        marker=dict(color=CHART_COLORS['gain'], size=10),
        text=[f"High: ${data['high']:,.0f}"],
        textposition='top center',
        textfont=dict(size=11, color=CHART_COLORS['gain']),
        hoverinfo='skip'
    ))

    fig.add_trace(go.Scatter(
        x=[data['dates'][min_idx]],
        y=[data['low']],
        mode='markers+text',
        marker=dict(color=CHART_COLORS['loss'], size=10),
        text=[f"Low: ${data['low']:,.0f}"],
        textposition='bottom center',
        textfont=dict(size=11, color=CHART_COLORS['loss']),
        hoverinfo='skip'
    ))

    layout = get_chart_layout(height=350)
    layout.update(
        yaxis=dict(showgrid=True, gridcolor='rgba(148, 163, 184, 0.08)', tickprefix='$'),
    )
    fig.update_layout(**layout)

    return fig


def create_asset_bar_chart(assets: list):
    """Create horizontal bar chart for asset performance."""
    assets = sorted(assets, key=lambda x: x['change_pct'], reverse=True)

    colors = [CHART_COLORS['gain'] if a['change_pct'] >= 0 else CHART_COLORS['loss'] for a in assets]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=[a['ticker'] for a in assets],
        x=[a['change_pct'] for a in assets],
        orientation='h',
        marker=dict(color=colors, cornerradius=4),
        text=[f"{'+' if a['change_pct'] >= 0 else ''}{a['change_pct']:.1f}%" for a in assets],
        textposition='outside',
        textfont=dict(size=11, family='JetBrains Mono')
    ))

    layout = get_chart_layout(height=400)
    layout.update(
        margin=dict(l=70, r=70, t=10, b=10),
        xaxis=dict(showgrid=True, gridcolor='rgba(148, 163, 184, 0.08)', ticksuffix='%'),
        yaxis=dict(showgrid=False, autorange='reversed'),
    )
    fig.update_layout(**layout)

    return fig


def main():
    page_header("Performance", "Track your investment returns over time", "📈")

    # Period selector
    if 'perf_period' not in st.session_state:
        st.session_state.perf_period = '1M'

    periods = ['1D', '1W', '1M', '3M', 'YTD', '1Y', 'ALL']
    cols = st.columns(len(periods))
    for i, period in enumerate(periods):
        with cols[i]:
            btn_type = "primary" if st.session_state.perf_period == period else "secondary"
            if st.button(period, key=f"perf_{period}", type=btn_type, use_container_width=True):
                st.session_state.perf_period = period
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Get data
    data = get_mock_performance(st.session_state.perf_period)

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        is_positive = data['change'] >= 0
        pnl_class = "gain" if is_positive else "loss"
        sign = "+" if is_positive else ""
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Period Return</div>
            <div class="metric-value" style="color: var(--{pnl_class});">{sign}${data['change']:,.2f}</div>
            <span class="metric-change {pnl_class}">{sign}{data['change_pct']:.2f}%</span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Starting Value</div>
            <div class="metric-value">${data['start_value']:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Current Value</div>
            <div class="metric-value">${data['end_value']:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Period High</div>
            <div class="metric-value" style="color: var(--gain);">${data['high']:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Chart
    section_label("Portfolio Evolution")
    chart = create_performance_chart(data)
    st.plotly_chart(chart, use_container_width=True, config={'displayModeBar': False})

    st.markdown("---")

    # Per-asset performance
    section_label("Performance by Asset")

    asset_data = get_mock_asset_performance(st.session_state.perf_period)
    bar_chart = create_asset_bar_chart(asset_data)
    st.plotly_chart(bar_chart, use_container_width=True, config={'displayModeBar': False})

    # Table view
    with st.expander("📊 View detailed table"):
        df = pd.DataFrame(asset_data)
        df['change_pct'] = df['change_pct'].apply(lambda x: f"{'+' if x >= 0 else ''}{x:.2f}%")
        df['change'] = df['change'].apply(lambda x: f"${x:,.2f}")
        df.columns = ['Ticker', 'Change %', 'Change $']
        st.dataframe(df, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
