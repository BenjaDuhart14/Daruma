"""
Dividends Page - Dividend income tracking
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

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


def get_mock_dividends():
    """Mock dividend data - replace with Supabase calls."""
    return {
        'total': 1245.67,
        'this_year': 425.30,
        'by_year': [
            {'year': 2024, 'amount': 425.30},
            {'year': 2023, 'amount': 520.37},
            {'year': 2022, 'amount': 300.00},
        ],
        'by_ticker': [
            {'ticker': 'VOO', 'amount': 456.20, 'payments': 8},
            {'ticker': 'QQQM', 'amount': 234.50, 'payments': 4},
            {'ticker': 'AAPL', 'amount': 189.30, 'payments': 4},
            {'ticker': 'COST', 'amount': 145.67, 'payments': 4},
            {'ticker': 'GOOGL', 'amount': 120.00, 'payments': 2},
            {'ticker': 'AMZN', 'amount': 100.00, 'payments': 2},
        ],
        'recent': [
            {'date': '2024-12-15', 'ticker': 'VOO', 'amount': 58.40},
            {'date': '2024-12-10', 'ticker': 'AAPL', 'amount': 12.35},
            {'date': '2024-11-15', 'ticker': 'QQQM', 'amount': 45.20},
            {'date': '2024-11-01', 'ticker': 'COST', 'amount': 38.50},
            {'date': '2024-10-15', 'ticker': 'VOO', 'amount': 55.80},
        ]
    }


def create_yearly_chart(by_year: list):
    """Create bar chart for dividends by year."""
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
    # Sort by amount
    by_ticker = sorted(by_ticker, key=lambda x: x['amount'], reverse=True)

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

    data = get_mock_dividends()

    # Summary metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Recibido", f"${data['total']:,.2f}")

    with col2:
        st.metric("Este Ano", f"${data['this_year']:,.2f}")

    with col3:
        avg_monthly = data['this_year'] / 12
        st.metric("Promedio Mensual", f"${avg_monthly:,.2f}")

    st.markdown("---")

    # Charts side by side
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Por Ano")
        yearly_chart = create_yearly_chart(data['by_year'])
        st.plotly_chart(yearly_chart, use_container_width=True, config={'displayModeBar': False})

    with col2:
        st.markdown("#### Por Activo")
        ticker_chart = create_ticker_chart(data['by_ticker'])
        st.plotly_chart(ticker_chart, use_container_width=True, config={'displayModeBar': False})

    st.markdown("---")

    # Recent dividends
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
    with st.expander("Ver todos los dividendos por activo"):
        df = pd.DataFrame(data['by_ticker'])
        df['amount'] = df['amount'].apply(lambda x: f"${x:,.2f}")
        df.columns = ['Ticker', 'Total Recibido', 'Pagos']
        st.dataframe(df, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
