"""
Dividends Page - Dividend income tracking
Alpine Dusk Theme
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from utils import supabase_client as db
from utils.auth import check_password
from utils.styles import apply_styles, section_label, page_header, get_chart_layout, CHART_COLORS

st.set_page_config(
    page_title="Dividends - Daruma",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply Alpine Dusk theme
apply_styles()

# Authentication check
check_password()


@st.cache_data(ttl=300)
def get_dividend_data():
    """Fetch dividend data from Supabase."""
    try:
        client = db.get_client()

        all_dividends = db.get_dividends(client)
        by_year_raw = db.get_dividends_by_year(client)
        by_ticker_raw = db.get_dividend_summary(client)

        year_totals = {}
        for d in by_year_raw:
            year = d['year']
            if year not in year_totals:
                year_totals[year] = 0
            year_totals[year] += float(d['total_received'] or 0)

        by_year = [{'year': y, 'amount': a} for y, a in sorted(year_totals.items(), reverse=True)]

        by_ticker = []
        for d in by_ticker_raw:
            by_ticker.append({
                'ticker': d['ticker'],
                'amount': float(d['total_dividends'] or 0),
                'payments': d['dividend_count'] or 0
            })

        total = sum(d['amount'] for d in by_ticker)
        current_year = datetime.now().year
        this_year = year_totals.get(current_year, 0)

        recent = []
        for d in all_dividends[:10]:
            recent.append({
                'date': d['payment_date'],
                'ticker': d['ticker'],
                'amount': float(d['total_received'] or 0)
            })

        return {
            'total': total,
            'this_year': this_year,
            'by_year': by_year,
            'by_ticker': by_ticker,
            'recent': recent,
            'connected': True
        }
    except Exception as e:
        st.error(f"Error loading dividends: {str(e)}")
        return {
            'total': 0,
            'this_year': 0,
            'by_year': [],
            'by_ticker': [],
            'recent': [],
            'connected': False
        }


def create_yearly_chart(by_year: list):
    """Create bar chart for dividends by year."""
    if not by_year:
        return None

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=[str(y['year']) for y in by_year],
        y=[y['amount'] for y in by_year],
        marker=dict(
            color=CHART_COLORS['gain'],
            cornerradius=6
        ),
        text=[f"${y['amount']:,.0f}" for y in by_year],
        textposition='outside',
        textfont=dict(color=CHART_COLORS['gain'], size=12, family='JetBrains Mono')
    ))

    layout = get_chart_layout(height=280)
    layout.update(
        yaxis=dict(showgrid=True, gridcolor='rgba(148, 163, 184, 0.08)', tickprefix='$'),
    )
    fig.update_layout(**layout)

    return fig


def create_ticker_chart(by_ticker: list):
    """Create horizontal bar chart for dividends by ticker."""
    if not by_ticker:
        return None

    by_ticker = sorted(by_ticker, key=lambda x: x['amount'], reverse=True)[:10]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=[t['ticker'] for t in by_ticker],
        x=[t['amount'] for t in by_ticker],
        orientation='h',
        marker=dict(
            color='#8b5cf6',
            cornerradius=4
        ),
        text=[f"${t['amount']:,.0f}" for t in by_ticker],
        textposition='outside',
        textfont=dict(size=11, family='JetBrains Mono')
    ))

    layout = get_chart_layout(height=320)
    layout.update(
        margin=dict(l=70, r=70, t=10, b=10),
        xaxis=dict(showgrid=True, gridcolor='rgba(148, 163, 184, 0.08)', tickprefix='$'),
        yaxis=dict(showgrid=False, autorange='reversed'),
    )
    fig.update_layout(**layout)

    return fig


def main():
    page_header("Dividends", "Track your passive income from dividends", "💰")

    data = get_dividend_data()

    if not data['connected']:
        st.warning("⚠️ Not connected to database.")

    # Summary metrics - single column on mobile for better readability
    avg_monthly = data['this_year'] / 12 if data['this_year'] > 0 else 0

    st.markdown(f"""
    <div class="metric-card" style="margin-bottom: 12px;">
        <div class="metric-label">Total Received</div>
        <div class="metric-value-large" style="color: var(--gain);">${data['total']:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">This Year</div>
            <div class="metric-value">${data['this_year']:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    with row1_col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Monthly Avg</div>
            <div class="metric-value">${avg_monthly:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if not data['by_year'] and not data['by_ticker']:
        st.markdown("""
        <div style="
            text-align: center;
            padding: 60px 20px;
            background: var(--bg-card);
            border-radius: 16px;
            border: 1px dashed var(--border-subtle);
        ">
            <div style="font-size: 48px; margin-bottom: 16px;">💰</div>
            <h3 style="color: var(--text-primary); margin-bottom: 8px;">No Dividends Yet</h3>
            <p style="color: var(--text-secondary);">Dividends will appear here once you have holdings with dividend-paying stocks.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        section_label("By Year")
        yearly_chart = create_yearly_chart(data['by_year'])
        if yearly_chart:
            st.plotly_chart(yearly_chart, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("No yearly data available")

    with col2:
        section_label("By Asset")
        ticker_chart = create_ticker_chart(data['by_ticker'])
        if ticker_chart:
            st.plotly_chart(ticker_chart, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("No ticker data available")

    st.markdown("---")

    # Recent dividends
    if data['recent']:
        section_label("Recent Payments")

        for div in data['recent']:
            st.markdown(f"""
            <div class="data-row">
                <div style="display: flex; align-items: center; flex: 1;">
                    <div class="ticker-badge" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);">
                        {div['ticker'][:2]}
                    </div>
                    <div>
                        <div class="ticker-name">{div['ticker']}</div>
                        <div class="ticker-details">{div['date']}</div>
                    </div>
                </div>
                <div style="text-align: right;">
                    <span class="pnl-badge gain">+${div['amount']:,.2f}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Full table
    if data['by_ticker']:
        with st.expander("📊 View all dividends by asset"):
            df = pd.DataFrame(data['by_ticker'])
            df['amount'] = df['amount'].apply(lambda x: f"${x:,.2f}")
            df.columns = ['Ticker', 'Total Received', 'Payments']
            st.dataframe(df, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
