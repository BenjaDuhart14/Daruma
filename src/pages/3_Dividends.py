"""
Dividends Page - Dividend income tracking
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
from utils import supabase_client as db

st.set_page_config(
    page_title="Dividends - Daruma",
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
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=300)
def get_dividend_data():
    """Fetch dividend data from Supabase."""
    try:
        client = db.get_client()

        # Get all dividends for recent list
        all_dividends = db.get_dividends(client)

        # Get dividends by year
        by_year_raw = db.get_dividends_by_year(client)

        # Get dividend summary by ticker
        by_ticker_raw = db.get_dividend_summary(client)

        # Process by year (aggregate all tickers per year)
        year_totals = {}
        for d in by_year_raw:
            year = d['year']
            if year not in year_totals:
                year_totals[year] = 0
            year_totals[year] += float(d['total_received'] or 0)

        by_year = [{'year': y, 'amount': a} for y, a in sorted(year_totals.items(), reverse=True)]

        # Process by ticker
        by_ticker = []
        for d in by_ticker_raw:
            by_ticker.append({
                'ticker': d['ticker'],
                'amount': float(d['total_dividends'] or 0),
                'payments': d['dividend_count'] or 0
            })

        # Calculate totals
        total = sum(d['amount'] for d in by_ticker)
        current_year = datetime.now().year
        this_year = year_totals.get(current_year, 0)

        # Recent dividends (last 10)
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
        marker_color='#4CAF50',
        text=[f"${y['amount']:,.2f}" for y in by_year],
        textposition='outside',
        textfont=dict(color='#4CAF50', size=12)
    ))

    fig.update_layout(
        plot_bgcolor='#1A1A1A',
        paper_bgcolor='#1A1A1A',
        margin=dict(l=10, r=10, t=30, b=40),
        height=250,
        xaxis=dict(showgrid=False, color='#888'),
        yaxis=dict(showgrid=True, gridcolor='#262730', color='#888', tickprefix='$'),
        showlegend=False
    )

    return fig


def create_ticker_chart(by_ticker: list):
    """Create horizontal bar chart for dividends by ticker."""
    if not by_ticker:
        return None

    # Sort by amount
    by_ticker = sorted(by_ticker, key=lambda x: x['amount'], reverse=True)[:10]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=[t['ticker'] for t in by_ticker],
        x=[t['amount'] for t in by_ticker],
        orientation='h',
        marker_color='#4CAF50',
        text=[f"${t['amount']:,.2f}" for t in by_ticker],
        textposition='outside',
        textfont=dict(size=11)
    ))

    fig.update_layout(
        plot_bgcolor='#1A1A1A',
        paper_bgcolor='#1A1A1A',
        margin=dict(l=60, r=60, t=10, b=10),
        height=300,
        xaxis=dict(showgrid=True, gridcolor='#262730', color='#888', tickprefix='$'),
        yaxis=dict(showgrid=False, color='#FAFAFA', autorange='reversed'),
        showlegend=False
    )

    return fig


def main():
    st.markdown("### Dividendos")

    data = get_dividend_data()

    if not data['connected']:
        st.warning("Not connected to database.")

    # Summary metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Recibido", f"${data['total']:,.2f}")

    with col2:
        st.metric("Este Ano", f"${data['this_year']:,.2f}")

    with col3:
        avg_monthly = data['this_year'] / 12 if data['this_year'] > 0 else 0
        st.metric("Promedio Mensual", f"${avg_monthly:,.2f}")

    st.markdown("---")

    if not data['by_year'] and not data['by_ticker']:
        st.info("No dividend data yet. Dividends will be calculated automatically once you have holdings with dividend-paying stocks.")
        return

    # Charts side by side
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Por Ano")
        yearly_chart = create_yearly_chart(data['by_year'])
        if yearly_chart:
            st.plotly_chart(yearly_chart, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("No yearly data")

    with col2:
        st.markdown("#### Por Activo")
        ticker_chart = create_ticker_chart(data['by_ticker'])
        if ticker_chart:
            st.plotly_chart(ticker_chart, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("No ticker data")

    st.markdown("---")

    # Recent dividends
    if data['recent']:
        st.markdown("#### Pagos Recientes")

        for div in data['recent']:
            col1, col2, col3 = st.columns([2, 2, 2])

            with col1:
                st.markdown(f"**{div['ticker']}**")

            with col2:
                st.caption(div['date'])

            with col3:
                st.markdown(f":green[+${div['amount']:,.2f}]")

            st.markdown("---")

    # Full table
    if data['by_ticker']:
        with st.expander("Ver todos los dividendos por activo"):
            df = pd.DataFrame(data['by_ticker'])
            df['amount'] = df['amount'].apply(lambda x: f"${x:,.2f}")
            df.columns = ['Ticker', 'Total Recibido', 'Pagos']
            st.dataframe(df, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
