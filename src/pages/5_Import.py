"""
Import Page - Import transactions from Delta CSV
"""

import streamlit as st
import pandas as pd
import sys
import os

# Add utils to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

st.set_page_config(
    page_title="Import - Daruma",
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


def parse_delta_csv_preview(content: str):
    """Parse Delta CSV for preview."""
    try:
        from utils.delta_parser import parse_delta_csv, get_import_summary
        transactions = parse_delta_csv(content)
        summary = get_import_summary(transactions)
        return transactions, summary, None
    except Exception as e:
        return None, None, str(e)


def main():
    st.markdown("### Importar desde Delta")

    st.info("""
    **Instrucciones:**
    1. Abre la app Delta en tu telefono
    2. Ve a Settings > Export Data > Export as CSV
    3. Sube el archivo CSV aqui
    """)

    # File uploader
    uploaded_file = st.file_uploader(
        "Selecciona el archivo CSV de Delta",
        type=['csv'],
        help="Archivo CSV exportado desde Delta app"
    )

    if uploaded_file is not None:
        # Read file content
        content = uploaded_file.read().decode('utf-8')

        # Parse CSV
        transactions, summary, error = parse_delta_csv_preview(content)

        if error:
            st.error(f"Error al parsear el archivo: {error}")
            return

        if not transactions:
            st.warning("No se encontraron transacciones validas en el archivo")
            return

        # Show summary
        st.markdown("---")
        st.markdown("### Vista Previa")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Transacciones", summary['total_transactions'])

        with col2:
            st.metric("Tickers Unicos", summary['unique_tickers'])

        with col3:
            st.metric("Compras", summary['buy_count'])

        with col4:
            st.metric("Ventas", summary['sell_count'])

        # Asset types breakdown
        st.markdown("#### Tipos de Activos")
        cols = st.columns(len(summary['asset_types']))
        for i, (asset_type, count) in enumerate(summary['asset_types'].items()):
            with cols[i]:
                st.metric(asset_type, count)

        # Date range
        if summary['date_range']:
            st.markdown("#### Rango de Fechas")
            col1, col2 = st.columns(2)
            with col1:
                st.caption(f"Desde: {summary['date_range']['earliest'][:10]}")
            with col2:
                st.caption(f"Hasta: {summary['date_range']['latest'][:10]}")

        # Preview table
        st.markdown("#### Primeras 10 Transacciones")

        preview_data = []
        for tx in transactions[:10]:
            preview_data.append({
                'Fecha': tx['date'][:10],
                'Tipo': tx['type'],
                'Ticker': tx['ticker'],
                'Cantidad': f"{tx['quantity']:.4f}",
                'Precio': f"${tx['price']:,.2f}",
                'Total': f"${tx['total_amount']:,.2f}"
            })

        df = pd.DataFrame(preview_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Tickers list
        with st.expander("Ver todos los tickers"):
            st.write(", ".join(sorted(summary['tickers'])))

        st.markdown("---")

        # Import button
        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            if st.button("Importar Transacciones", type="primary", use_container_width=True):
                # TODO: Replace with actual Supabase import
                with st.spinner("Importando transacciones..."):
                    import time
                    time.sleep(2)  # Simulated delay

                    # Show success (mock)
                    st.success(f"""
                    Importacion completada:
                    - {summary['total_transactions']} transacciones importadas
                    - {summary['unique_tickers']} tickers diferentes
                    """)

                    st.balloons()

        # Warning about duplicates
        st.markdown("---")
        st.warning("""
        **Nota sobre duplicados:**
        El sistema verificara automaticamente si ya existen transacciones
        con la misma fecha, ticker y cantidad para evitar duplicados.
        """)


if __name__ == "__main__":
    main()
