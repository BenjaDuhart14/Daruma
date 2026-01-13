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
from utils.styles import apply_styles, get_chart_layout, section_label, page_header, CHART_COLORS, get_daruma_logo, render_fab_button, render_bottom_nav


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

    # For stocks and ETFs, use Financial Modeling Prep
    return f"https://financialmodelingprep.com/image-stock/{ticker.upper()}.png"

# Page config - use Daruma favicon
st.set_page_config(
    page_title="Home - Daruma",
    page_icon="src/favicon.svg",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply Alpine Dusk theme
apply_styles()

# Authentication check
check_password()

# Sidebar
with st.sidebar:
    daruma_logo = get_daruma_logo(50)
    st.markdown(f"""
    <div style="padding: 20px 0; text-align: center;">
        <div class="sidebar-logo">
            {daruma_logo}
        </div>
        <h3 style="margin: 0; color: #f8fafc; font-size: 18px; font-weight: 700;">Daruma</h3>
        <p style="margin: 4px 0 0; color: #64748b; font-size: 12px;">Portfolio Tracker</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    if st.button("🚪 Sign Out", use_container_width=True):
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
            'total_invested': float(summary.get('total_invested') or 0),
            'total_pnl': float(summary.get('total_pnl') or 0),
            'total_pnl_pct': float(summary.get('total_pnl_percent') or 0),
            'holdings': holdings,
            'connected': True
        }
    except Exception as e:
        st.error(f"Database connection error: {str(e)}")
        return {
            'total_value': 0,
            'total_invested': 0,
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


def create_portfolio_chart(period: str, current_value: float = 0, total_cost: float = 0):
    """Create portfolio evolution line chart with Alpine Dusk styling and crosshairs.
    
    Uses current_value from live data, and historical snapshots if available.
    Falls back to a simple cost->current line if no historical data.
    """
    days_map = {'1D': 1, '1W': 7, '1M': 30, '3M': 90, 'YTD': 180, '1Y': 365, 'ALL': 730}
    days = days_map.get(period, 30)

    snapshots = get_portfolio_history(days)
    
    # Determine if we have valid historical data
    has_history = snapshots and len(snapshots) > 1
    
    if has_history:
        dates = pd.to_datetime([s['snapshot_date'] for s in snapshots])
        values = np.array([float(s['total_value']) for s in snapshots])
        # Replace the last value with actual current value (live data)
        values[-1] = current_value
    else:
        # No historical data - create a simple line from cost to current
        if current_value > 0:
            num_points = min(days, 30) if days > 1 else 2
            dates = pd.date_range(end=datetime.now(), periods=num_points, freq='D')
            # Interpolate from invested cost to current value
            start_val = total_cost if total_cost > 0 else current_value * 0.9
            values = np.linspace(start_val, current_value, num_points)
        else:
            dates = pd.date_range(end=datetime.now(), periods=2, freq='D')
            values = np.array([0, 0])

    # Always use current_value as the end value (live data)
    end_value = current_value
    start_value = values[0] if len(values) > 0 else total_cost
    
    is_positive = end_value >= start_value
    line_color = CHART_COLORS['gain'] if is_positive else CHART_COLORS['loss']
    fill_color = 'rgba(16, 185, 129, 0.1)' if is_positive else 'rgba(239, 68, 68, 0.1)'
    
    # Calculate period change for display
    period_change = end_value - start_value
    period_change_pct = ((end_value - start_value) / start_value * 100) if start_value > 0 else 0

    fig = go.Figure()

    # Main line with gradient area fill
    fig.add_trace(go.Scatter(
        x=dates,
        y=values,
        mode='lines',
        line=dict(color=line_color, width=2.5),
        fill='tozeroy',
        fillcolor=fill_color,
        hovertemplate='<b style="font-size:14px">%{x|%b %d, %Y}</b><br><span style="font-size:18px;font-weight:bold">$%{y:,.0f}</span><extra></extra>',
        name='Portfolio',
        hoverlabel=dict(
            bgcolor='rgba(20, 20, 35, 0.95)',
            bordercolor=line_color,
            font=dict(family='JetBrains Mono', size=13, color='#f8fafc')
        )
    ))
    
    # Add start point marker
    if len(values) > 0:
        fig.add_trace(go.Scatter(
            x=[dates[0]],
            y=[values[0]],
            mode='markers',
            marker=dict(color='#64748b', size=6, symbol='circle'),
            hovertemplate='Start: <b>$%{y:,.2f}</b><extra></extra>',
            name='Start'
        ))
    
    # Add end point marker (current)
    if len(values) > 0:
        fig.add_trace(go.Scatter(
            x=[dates[-1]],
            y=[current_value],  # Always use live current value
            mode='markers',
            marker=dict(color=line_color, size=10, symbol='circle', 
                       line=dict(color='white', width=2)),
            hovertemplate='Current: <b>$%{y:,.2f}</b><extra></extra>',
            name='Current'
        ))

    # Layout - mobile optimized with crosshair spikes
    layout = get_chart_layout(height=220)
    layout.update(
        margin=dict(l=5, r=5, t=5, b=30),
        xaxis=dict(
            showgrid=False, 
            showticklabels=True, 
            color='#64748b', 
            tickfont=dict(size=10),
            showspikes=True,
            spikecolor='#8b5cf6',
            spikethickness=1,
            spikedash='solid',
            spikemode='across',
            spikesnap='cursor'
        ),
        yaxis=dict(
            showgrid=True, 
            gridcolor='rgba(148, 163, 184, 0.08)', 
            tickprefix='$', 
            color='#64748b', 
            tickfont=dict(size=10),
            showspikes=True,
            spikecolor='#8b5cf6',
            spikethickness=1,
            spikedash='solid',
            spikemode='across',
            spikesnap='cursor'
        ),
        hovermode='x unified',
        spikedistance=-1,
    )
    fig.update_layout(**layout)

    return fig, {
        'start_value': start_value,
        'end_value': end_value,
        'period_change': period_change,
        'period_change_pct': period_change_pct,
        'is_positive': is_positive,
        'has_history': has_history
    }


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
        textfont=dict(color=bar_color, size=10, family='JetBrains Mono')
    ))

    layout = get_chart_layout(height=180)
    layout.update(
        margin=dict(l=5, r=5, t=25, b=30),
        yaxis=dict(showgrid=False, showticklabels=False),
        xaxis=dict(tickfont=dict(size=10)),
        bargap=0.3
    )
    fig.update_layout(**layout)

    return fig


def create_allocation_donut(holdings: list, total_value: float):
    """Create a donut chart showing portfolio allocation by asset.
    
    Features:
    - Vibrant color palette that matches Alpine Dusk theme
    - Center hole with total value display
    - Hover shows value and percentage
    - Top 8 holdings + "Others" for clarity
    """
    if not holdings or total_value <= 0:
        return None
    
    # Sort by value and take top 8, group rest as "Others"
    sorted_holdings = sorted(holdings, key=lambda x: x['current_value'], reverse=True)
    
    if len(sorted_holdings) > 8:
        top_holdings = sorted_holdings[:8]
        others_value = sum(h['current_value'] for h in sorted_holdings[8:])
        labels = [h['ticker'] for h in top_holdings] + ['Others']
        values = [h['current_value'] for h in top_holdings] + [others_value]
    else:
        labels = [h['ticker'] for h in sorted_holdings]
        values = [h['current_value'] for h in sorted_holdings]
    
    # Alpine Dusk inspired color palette - vibrant and modern
    colors = [
        '#8b5cf6',  # Purple (primary accent)
        '#06b6d4',  # Cyan
        '#10b981',  # Emerald/Green
        '#f59e0b',  # Amber
        '#ef4444',  # Red
        '#ec4899',  # Pink
        '#6366f1',  # Indigo
        '#14b8a6',  # Teal
        '#64748b',  # Slate (for "Others")
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        hole=0.65,  # Donut hole size
        marker=dict(
            colors=colors[:len(labels)],
            line=dict(color='#0a0a12', width=2)  # Dark border between segments
        ),
        textinfo='percent',
        textposition='outside',
        textfont=dict(
            size=11,
            color='#94a3b8',
            family='JetBrains Mono'
        ),
        hovertemplate='<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>',
        showlegend=True,
        direction='clockwise',
        sort=False  # Keep our sorted order
    ))
    
    # Layout with center annotation showing total
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=280,
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.15,
            xanchor='center',
            x=0.5,
            font=dict(size=10, color='#94a3b8'),
            bgcolor='rgba(0,0,0,0)'
        ),
        annotations=[
            dict(
                text=f'<b>${total_value:,.0f}</b>',
                x=0.5, y=0.55,
                font=dict(size=18, color='#f8fafc', family='Plus Jakarta Sans'),
                showarrow=False
            ),
            dict(
                text='Total Value',
                x=0.5, y=0.42,
                font=dict(size=11, color='#64748b', family='Plus Jakarta Sans'),
                showarrow=False
            )
        ]
    )
    
    return fig


def render_holding_row(h: dict):
    """Render a single holding row with mobile-friendly layout and logo."""
    is_positive = h['pnl_pct'] >= 0
    pnl_class = "gain" if is_positive else "loss"
    sign = "+" if is_positive else ""
    initials = h['ticker'][:2].upper()
    logo_url = get_logo_url(h['ticker'], h['type'])

    # Mobile-friendly stacked layout with logo
    st.markdown(f"""
    <div class="data-row-mobile">
        <div class="row-header">
            <div class="row-left">
                <div style="
                    width: 36px;
                    height: 36px;
                    border-radius: 10px;
                    background: var(--bg-card);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin-right: 10px;
                    overflow: hidden;
                    flex-shrink: 0;
                ">
                    <img src="{logo_url}"
                         alt="{h['ticker']}"
                         style="width: 28px; height: 28px; object-fit: contain;"
                         onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                    <span style="
                        display: none;
                        width: 100%;
                        height: 100%;
                        align-items: center;
                        justify-content: center;
                        background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
                        color: white;
                        font-size: 12px;
                        font-weight: 600;
                    ">{initials}</span>
                </div>
                <div>
                    <div class="ticker-name">{h['ticker']}</div>
                    <div class="ticker-details">{h['shares']:.2f} shares</div>
                </div>
            </div>
            <span class="pnl-badge {pnl_class}">{sign}{h['pnl_pct']:.1f}%</span>
        </div>
        <div class="row-details">
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
    data = get_portfolio_data()

    # Page header - now "Home" instead of "Dashboard"
    daruma_header = get_daruma_logo(32)
    st.markdown(f"""
    <div class="page-title">
        <span class="daruma-logo">{daruma_header}</span>
        Home
    </div>
    <p class="page-subtitle">Track your portfolio performance</p>
    """, unsafe_allow_html=True)

    if not data['connected']:
        st.warning("⚠️ Not connected to database. Please check your Supabase credentials.")

    # Main metrics - 2x2 grid for mobile compatibility
    pnl_class = "gain" if data['total_pnl'] >= 0 else "loss"
    sign = "+" if data['total_pnl'] >= 0 else ""
    asset_count = len(data['holdings'])

    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Value</div>
            <div class="metric-value-large">${data['total_value']:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    with row1_col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total P&L</div>
            <div class="metric-value" style="color: var(--{pnl_class});">{sign}${data['total_pnl']:,.0f}</div>
            <span class="metric-change {pnl_class}">{sign}{data['total_pnl_pct']:.1f}%</span>
        </div>
        """, unsafe_allow_html=True)

    row2_col1, row2_col2 = st.columns(2)
    with row2_col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Invested</div>
            <div class="metric-value">${data['total_invested']:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    with row2_col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Assets</div>
            <div class="metric-value">{asset_count}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Period selector - use 4 columns for better mobile display
    section_label("Portfolio Performance")

    periods = ['1D', '1W', '1M', '3M', 'YTD', '1Y', 'ALL']

    # Period selector using Streamlit columns with custom styling
    cols = st.columns(7)
    for i, period in enumerate(periods):
        with cols[i]:
            btn_type = "primary" if st.session_state.selected_period == period else "secondary"
            if st.button(period, key=f"period_{period}", type=btn_type, use_container_width=True):
                st.session_state.selected_period = period
                st.rerun()

    # Portfolio chart with dynamic value display
    # Pass both current_value and total_cost so chart can properly display
    chart, chart_data = create_portfolio_chart(
        st.session_state.selected_period, 
        current_value=data['total_value'],
        total_cost=data['total_invested']
    )
    
    # Dynamic Value Display Header
    period_labels = {
        '1D': 'Today', '1W': 'This Week', '1M': 'This Month', 
        '3M': 'Last 3 Months', 'YTD': 'Year to Date', '1Y': 'Last Year', 'ALL': 'All Time'
    }
    current_period = period_labels.get(st.session_state.selected_period, 'Selected Period')
    
    change_class = "gain" if chart_data['is_positive'] else "loss"
    change_sign = "+" if chart_data['is_positive'] else ""
    
    st.markdown(f"""
    <div class="chart-value-header">
        <div class="chart-main-value">${chart_data['end_value']:,.0f}</div>
        <div class="chart-value-change {change_class}">
            <span class="amount">{change_sign}${abs(chart_data['period_change']):,.0f}</span>
            <span>({change_sign}{chart_data['period_change_pct']:.1f}%)</span>
        </div>
        <div class="chart-period-label">{current_period}</div>
        <div class="chart-hint">Hover chart for details</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.plotly_chart(chart, use_container_width=True, config={'displayModeBar': False})
    
    # Show notice if no historical data
    if not chart_data.get('has_history', True):
        st.caption("📊 *Limited history - chart shows growth from invested to current value*")

    st.markdown("---")
    
    # Allocation Donut Chart section
    if data['holdings']:
        section_label("Portfolio Allocation")
        
        donut_chart = create_allocation_donut(data['holdings'], data['total_value'])
        if donut_chart:
            st.plotly_chart(donut_chart, use_container_width=True, config={'displayModeBar': False})
        
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

    # Floating Action Button for quick transaction adding
    render_fab_button()
    
    # Bottom Navigation Bar
    render_bottom_nav(active_page="home")


if __name__ == "__main__":
    main()
