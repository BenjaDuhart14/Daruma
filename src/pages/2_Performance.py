"""
Performance Page - Portfolio performance over time
Alpine Dusk Theme
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, date
import numpy as np
from utils import supabase_client as db
from utils.auth import check_password
from utils.styles import apply_styles, section_label, page_header, get_chart_layout, CHART_COLORS

st.set_page_config(
    page_title="Performance - Daruma",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply Alpine Dusk theme
apply_styles()

# Authentication check
check_password()


@st.cache_data(ttl=300)
def get_portfolio_performance(period: str):
    """Get real portfolio performance from Supabase snapshots."""
    days_map = {'1D': 1, '1W': 7, '1M': 30, '3M': 90, 'YTD': 180, '1Y': 365, 'ALL': 730}
    days = days_map.get(period, 30)

    try:
        client = db.get_client()
        snapshots = db.get_portfolio_snapshots(client, days=days)

        if snapshots and len(snapshots) > 1:
            dates = pd.to_datetime([s['snapshot_date'] for s in snapshots])
            values = np.array([float(s['total_value'] or 0) for s in snapshots])

            return {
                'dates': dates,
                'values': values,
                'start_value': values[0],
                'end_value': values[-1],
                'change': values[-1] - values[0],
                'change_pct': ((values[-1] - values[0]) / values[0]) * 100 if values[0] > 0 else 0,
                'high': max(values),
                'low': min(values),
                'connected': True
            }
        else:
            # Get current portfolio value as fallback
            summary = db.get_portfolio_summary(client)
            current_value = float(summary.get('total_value') or 0)
            total_cost = float(summary.get('total_invested') or 0)

            dates = pd.date_range(end=datetime.now(), periods=2, freq='D')
            values = np.array([total_cost, current_value]) if total_cost > 0 else np.array([current_value, current_value])

            return {
                'dates': dates,
                'values': values,
                'start_value': total_cost if total_cost > 0 else current_value,
                'end_value': current_value,
                'change': current_value - total_cost,
                'change_pct': ((current_value - total_cost) / total_cost) * 100 if total_cost > 0 else 0,
                'high': current_value,
                'low': min(total_cost, current_value) if total_cost > 0 else current_value,
                'connected': True
            }
    except Exception as e:
        st.error(f"Database error: {str(e)}")
        return {
            'dates': pd.date_range(end=datetime.now(), periods=2, freq='D'),
            'values': np.array([0, 0]),
            'start_value': 0,
            'end_value': 0,
            'change': 0,
            'change_pct': 0,
            'high': 0,
            'low': 0,
            'connected': False
        }


@st.cache_data(ttl=300)
def get_asset_performance():
    """Get real per-asset performance from holdings."""
    try:
        client = db.get_client()
        holdings = db.get_holdings_with_value(client)

        if not holdings:
            return []

        # Calculate P&L percentage for each holding
        assets = []
        for h in holdings:
            pnl_pct = float(h.get('pnl_percent') or 0)
            pnl = float(h.get('pnl') or 0)
            assets.append({
                'ticker': h['ticker'],
                'change_pct': pnl_pct,
                'change': pnl
            })

        return sorted(assets, key=lambda x: x['change_pct'], reverse=True)
    except Exception:
        return []


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
        marker=dict(color=CHART_COLORS['gain'], size=8),
        text=[f"${data['high']:,.0f}"],
        textposition='top center',
        textfont=dict(size=9, color=CHART_COLORS['gain']),
        hoverinfo='skip'
    ))

    fig.add_trace(go.Scatter(
        x=[data['dates'][min_idx]],
        y=[data['low']],
        mode='markers+text',
        marker=dict(color=CHART_COLORS['loss'], size=8),
        text=[f"${data['low']:,.0f}"],
        textposition='bottom center',
        textfont=dict(size=9, color=CHART_COLORS['loss']),
        hoverinfo='skip'
    ))

    layout = get_chart_layout(height=280)
    layout.update(
        margin=dict(l=5, r=5, t=20, b=30),
        yaxis=dict(showgrid=True, gridcolor='rgba(148, 163, 184, 0.08)', tickprefix='$', tickfont=dict(size=10)),
        xaxis=dict(tickfont=dict(size=10)),
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
        textposition='inside',
        textfont=dict(size=10, family='JetBrains Mono', color='white'),
        insidetextanchor='end'
    ))

    layout = get_chart_layout(height=400)
    layout.update(
        margin=dict(l=50, r=10, t=10, b=10),
        xaxis=dict(showgrid=True, gridcolor='rgba(148, 163, 184, 0.08)', ticksuffix='%'),
        yaxis=dict(showgrid=False, autorange='reversed'),
    )
    fig.update_layout(**layout)

    return fig


def main():
    page_header("Performance", "Track your investment returns over time", "📈")

    # Period selector - 4+3 layout for mobile
    if 'perf_period' not in st.session_state:
        st.session_state.perf_period = '1M'

    periods = ['1D', '1W', '1M', '3M', 'YTD', '1Y', 'ALL']

    cols1 = st.columns(4)
    for i, period in enumerate(periods[:4]):
        with cols1[i]:
            btn_type = "primary" if st.session_state.perf_period == period else "secondary"
            if st.button(period, key=f"perf_{period}", type=btn_type, use_container_width=True):
                st.session_state.perf_period = period
                st.rerun()

    cols2 = st.columns(4)
    for i, period in enumerate(periods[4:]):
        with cols2[i]:
            btn_type = "primary" if st.session_state.perf_period == period else "secondary"
            if st.button(period, key=f"perf_{period}", type=btn_type, use_container_width=True):
                st.session_state.perf_period = period
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Get real data from Supabase
    data = get_portfolio_performance(st.session_state.perf_period)

    if not data.get('connected', True):
        st.warning("⚠️ Could not connect to database.")

    # Summary metrics - 2x2 grid for mobile
    is_positive = data['change'] >= 0
    pnl_class = "gain" if is_positive else "loss"
    sign = "+" if is_positive else ""

    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Period Return</div>
            <div class="metric-value" style="color: var(--{pnl_class});">{sign}${data['change']:,.0f}</div>
            <span class="metric-change {pnl_class}">{sign}{data['change_pct']:.1f}%</span>
        </div>
        """, unsafe_allow_html=True)

    with row1_col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Current Value</div>
            <div class="metric-value">${data['end_value']:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    row2_col1, row2_col2 = st.columns(2)
    with row2_col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Start Value</div>
            <div class="metric-value">${data['start_value']:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    with row2_col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Period High</div>
            <div class="metric-value" style="color: var(--gain);">${data['high']:,.0f}</div>
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

    asset_data = get_asset_performance()

    if asset_data:
        bar_chart = create_asset_bar_chart(asset_data)
        st.plotly_chart(bar_chart, use_container_width=True, config={'displayModeBar': False})

        # Table view
        with st.expander("📊 View detailed table"):
            df = pd.DataFrame(asset_data)
            df['change_pct'] = df['change_pct'].apply(lambda x: f"{'+' if x >= 0 else ''}{x:.2f}%")
            df['change'] = df['change'].apply(lambda x: f"${x:,.2f}")
            df.columns = ['Ticker', 'Change %', 'Change $']
            st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No holdings data available. Add transactions to see performance by asset.")


if __name__ == "__main__":
    main()
