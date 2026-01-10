"""
Daruma - Investment Portfolio Tracker
Main Dashboard - Alpine Dusk Theme
"""

import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
import pandas as pd
import numpy as np

from utils import supabase_client as db
from utils.auth import check_password, logout
from utils.styles import apply_styles, get_chart_layout, section_label, page_header, CHART_COLORS

# Page config
st.set_page_config(
    page_title="Daruma",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Alpine Dusk theme
apply_styles()

# Authentication check
check_password()

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="padding: 20px 0; text-align: center;">
        <div style="
            width: 50px;
            height: 50px;
            margin: 0 auto 12px;
            background: linear-gradient(135deg, #8b5cf6 0%, #06b6d4 100%);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
        ">🎯</div>
        <h3 style="margin: 0; color: #f8fafc; font-size: 18px; font-weight: 700;">Daruma</h3>
        <p style="margin: 4px 0 0; color: #64748b; font-size: 12px;">Portfolio Tracker</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    if st.button("🚪 Cerrar Sesion", use_container_width=True):
        logout()

# Session state
if 'selected_period' not in st.session_state:
    st.session_state.selected_period = '1M'


@st.cache_data(ttl=300)
def get_portfolio_data():
    """Fetch real portfolio data from Supabase."""
    try:
        client = db.get_client()
        holdings_raw = db.get_holdings_with_value(client)
        summary = db.get_portfolio_summary(client)

        holdings = []
        for h in holdings_raw:
            holdings.append({
                'ticker': h['ticker'],
                'name': h['name'] or h['ticker'],
                'shares': float(h['shares'] or 0),
                'avg_price': float(h['avg_buy_price'] or 0),
                'current_value': float(h['current_value'] or 0),
                'current_price': float(h['current_price'] or 0),
                'pnl': float(h['pnl'] or 0),
                'pnl_pct': float(h['pnl_percent'] or 0),
                'type': h['asset_type'] or 'STOCK'
            })

        return {
            'total_value': float(summary.get('total_value') or 0),
            'total_cost': float(summary.get('total_invested') or 0),
            'total_pnl': float(summary.get('total_pnl') or 0),
            'total_pnl_pct': float(summary.get('total_pnl_percent') or 0),
            'holdings': holdings,
            'connected': True
        }
    except Exception as e:
        st.error(f"Database connection error: {str(e)}")
        return {
            'total_value': 0,
            'total_cost': 0,
            'total_pnl': 0,
            'total_pnl_pct': 0,
            'holdings': [],
            'connected': False
        }


@st.cache_data(ttl=300)
def get_portfolio_history(days: int = 365):
    """Fetch portfolio snapshots for chart."""
    try:
        client = db.get_client()
        return db.get_portfolio_snapshots(client, days=days)
    except Exception:
        return []


def create_portfolio_chart(period: str, current_value: float = 0):
    """Create portfolio evolution line chart with Alpine Dusk styling."""
    days_map = {'1D': 1, '1W': 7, '1M': 30, '3M': 90, 'YTD': 180, '1Y': 365, 'ALL': 730}
    days = days_map.get(period, 30)

    snapshots = get_portfolio_history(days)

    if snapshots and len(snapshots) > 1:
        dates = pd.to_datetime([s['snapshot_date'] for s in snapshots])
        values = np.array([float(s['total_value']) for s in snapshots])
    else:
        if current_value > 0:
            dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
            values = np.linspace(current_value * 0.95, current_value, 30)
        else:
            dates = pd.date_range(end=datetime.now(), periods=2, freq='D')
            values = np.array([0, 0])

    is_positive = len(values) < 2 or values[-1] >= values[0]
    line_color = CHART_COLORS['gain'] if is_positive else CHART_COLORS['loss']
    fill_color = 'rgba(16, 185, 129, 0.1)' if is_positive else 'rgba(239, 68, 68, 0.1)'

    fig = go.Figure()

    # Gradient area fill
    fig.add_trace(go.Scatter(
        x=dates,
        y=values,
        mode='lines',
        line=dict(color=line_color, width=2.5),
        fill='tozeroy',
        fillcolor=fill_color,
        hovertemplate='<b>$%{y:,.2f}</b><extra></extra>'
    ))

    # Layout
    layout = get_chart_layout(height=280)
    layout.update(
        xaxis=dict(showgrid=False, showticklabels=True, color='#64748b'),
        yaxis=dict(showgrid=True, gridcolor='rgba(148, 163, 184, 0.08)', tickprefix='$', color='#64748b'),
    )
    fig.update_layout(**layout)

    return fig


def create_movers_chart(holdings: list, top_n: int = 5, show_gainers: bool = True):
    """Create bar chart for top gainers/losers."""
    sorted_holdings = sorted(holdings, key=lambda x: x['pnl_pct'], reverse=show_gainers)

    if show_gainers:
        movers = [h for h in sorted_holdings if h['pnl_pct'] > 0][:top_n]
        bar_color = CHART_COLORS['gain']
    else:
        movers = [h for h in sorted_holdings if h['pnl_pct'] < 0][:top_n]
        movers = sorted(movers, key=lambda x: x['pnl_pct'])
        bar_color = CHART_COLORS['loss']

    if not movers:
        return None

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=[m['ticker'] for m in movers],
        y=[abs(m['pnl_pct']) for m in movers],
        marker=dict(
            color=bar_color,
            cornerradius=6
        ),
        text=[f"{'+' if m['pnl_pct'] > 0 else ''}{m['pnl_pct']:.1f}%" for m in movers],
        textposition='outside',
        textfont=dict(color=bar_color, size=12, family='JetBrains Mono')
    ))

    layout = get_chart_layout(height=200)
    layout.update(
        yaxis=dict(showgrid=False, showticklabels=False),
        bargap=0.4
    )
    fig.update_layout(**layout)

    return fig


def render_holding_row(h: dict):
    """Render a single holding row with Alpine Dusk styling."""
    is_positive = h['pnl_pct'] >= 0
    pnl_class = "gain" if is_positive else "loss"
    sign = "+" if is_positive else ""

    # Generate initials for badge
    initials = h['ticker'][:2].upper()

    st.markdown(f"""
    <div class="data-row">
        <div style="display: flex; align-items: center; flex: 2;">
            <div class="ticker-badge">{initials}</div>
            <div>
                <div class="ticker-name">{h['ticker']}</div>
                <div class="ticker-details">{h['shares']:.4f} shares @ ${h['avg_price']:,.2f}</div>
            </div>
        </div>
        <div style="flex: 1; text-align: right;">
            <div class="value-display">${h['current_value']:,.2f}</div>
        </div>
        <div style="flex: 1; text-align: right;">
            <span class="pnl-badge {pnl_class}">{sign}${h['pnl']:,.2f} ({sign}{h['pnl_pct']:.1f}%)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def main():
    data = get_portfolio_data()

    # Page header
    page_header("Dashboard", "Track your portfolio performance", "📊")

    if not data['connected']:
        st.warning("⚠️ Not connected to database. Please check your Supabase credentials.")

    # Main metrics row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Value</div>
            <div class="metric-value-large">${data['total_value']:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        pnl_class = "gain" if data['total_pnl'] >= 0 else "loss"
        sign = "+" if data['total_pnl'] >= 0 else ""
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total P&L</div>
            <div class="metric-value" style="color: var(--{pnl_class});">{sign}${data['total_pnl']:,.2f}</div>
            <span class="metric-change {pnl_class}">{sign}{data['total_pnl_pct']:.2f}%</span>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Invested</div>
            <div class="metric-value">${data['total_cost']:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        asset_count = len(data['holdings'])
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Assets</div>
            <div class="metric-value">{asset_count}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Period selector
    section_label("Portfolio Performance")

    periods = ['1D', '1W', '1M', '3M', 'YTD', '1Y', 'ALL']
    cols = st.columns(len(periods))
    for i, period in enumerate(periods):
        with cols[i]:
            btn_type = "primary" if st.session_state.selected_period == period else "secondary"
            if st.button(period, key=f"period_{period}", type=btn_type, use_container_width=True):
                st.session_state.selected_period = period
                st.rerun()

    # Portfolio chart
    chart = create_portfolio_chart(st.session_state.selected_period, data['total_value'])
    st.plotly_chart(chart, use_container_width=True, config={'displayModeBar': False})

    st.markdown("---")

    # Performance section
    if data['holdings']:
        section_label("Top Movers")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**🟢 Top Gainers**")
            gainers_chart = create_movers_chart(data['holdings'], show_gainers=True)
            if gainers_chart:
                st.plotly_chart(gainers_chart, use_container_width=True, config={'displayModeBar': False})
            else:
                st.info("No gainers yet")

        with col2:
            st.markdown("**🔴 Top Losers**")
            losers_chart = create_movers_chart(data['holdings'], show_gainers=False)
            if losers_chart:
                st.plotly_chart(losers_chart, use_container_width=True, config={'displayModeBar': False})
            else:
                st.info("No losers yet")

        st.markdown("---")

        # Holdings list
        section_label("Holdings")

        sorted_holdings = sorted(data['holdings'], key=lambda x: x['current_value'], reverse=True)[:8]

        for h in sorted_holdings:
            render_holding_row(h)

    else:
        st.markdown("""
        <div style="
            text-align: center;
            padding: 60px 20px;
            background: var(--bg-card);
            border-radius: 16px;
            border: 1px dashed var(--border-subtle);
        ">
            <div style="font-size: 48px; margin-bottom: 16px;">📈</div>
            <h3 style="color: var(--text-primary); margin-bottom: 8px;">No Holdings Yet</h3>
            <p style="color: var(--text-secondary);">Import your Delta CSV or add transactions manually to get started.</p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
