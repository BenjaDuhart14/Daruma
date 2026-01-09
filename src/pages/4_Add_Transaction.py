"""
Add Transaction Page - Manual transaction entry
"""

import streamlit as st
from datetime import datetime, date

st.set_page_config(
    page_title="Add Transaction - Daruma",
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


def get_existing_tickers():
    """Get list of existing tickers for autocomplete - replace with Supabase call."""
    return ['VOO', 'AMZN', 'QQQM', 'TSLA', 'ARKK', 'ETH', 'BTC', 'COST', 'AAPL', 'GOOGL']


def save_transaction(transaction: dict) -> bool:
    """Save transaction to database - replace with Supabase call."""
    # Mock save - replace with actual Supabase insert
    st.session_state['last_transaction'] = transaction
    return True


def main():
    st.markdown("### Agregar Transaccion")

    # Get existing tickers for suggestions
    existing_tickers = get_existing_tickers()

    with st.form("transaction_form"):
        col1, col2 = st.columns(2)

        with col1:
            # Date
            tx_date = st.date_input(
                "Fecha",
                value=date.today(),
                max_value=date.today()
            )

            # Ticker
            ticker = st.text_input(
                "Ticker",
                placeholder="Ej: AAPL, VOO, BTC",
                help="Simbolo del activo"
            ).upper()

            # Show suggestions if partial match
            if ticker and len(ticker) >= 1:
                suggestions = [t for t in existing_tickers if ticker in t]
                if suggestions and ticker not in suggestions:
                    st.caption(f"Sugerencias: {', '.join(suggestions)}")

            # Asset name (optional)
            name = st.text_input(
                "Nombre (opcional)",
                placeholder="Ej: Apple Inc, Vanguard S&P 500"
            )

            # Type
            tx_type = st.radio(
                "Tipo",
                ["BUY", "SELL"],
                horizontal=True
            )

        with col2:
            # Asset type
            asset_type = st.selectbox(
                "Tipo de Activo",
                ["STOCK", "FUND", "CRYPTO"],
                index=0
            )

            # Quantity
            quantity = st.number_input(
                "Cantidad",
                min_value=0.0,
                step=0.0001,
                format="%.4f"
            )

            # Price input method
            price_method = st.radio(
                "Ingresar precio como",
                ["Precio unitario", "Monto total"],
                horizontal=True
            )

            if price_method == "Precio unitario":
                price = st.number_input(
                    "Precio unitario (USD)",
                    min_value=0.0,
                    step=0.01,
                    format="%.4f"
                )
                total_amount = price * quantity if quantity else 0
                if total_amount > 0:
                    st.caption(f"Monto total: ${total_amount:,.2f}")
            else:
                total_amount = st.number_input(
                    "Monto total (USD)",
                    min_value=0.0,
                    step=0.01,
                    format="%.2f"
                )
                price = total_amount / quantity if quantity else 0
                if price > 0:
                    st.caption(f"Precio unitario: ${price:,.4f}")

        st.markdown("---")

        # Additional fields
        col1, col2 = st.columns(2)

        with col1:
            currency = st.selectbox(
                "Moneda",
                ["USD", "CLP"],
                index=0
            )

        with col2:
            platform = st.text_input(
                "Plataforma (opcional)",
                placeholder="Ej: Interactive Brokers, Binance"
            )

        # Notes
        notes = st.text_area(
            "Notas (opcional)",
            placeholder="Cualquier nota adicional sobre esta transaccion",
            max_chars=500
        )

        # Submit button
        submitted = st.form_submit_button("Guardar Transaccion", use_container_width=True)

        if submitted:
            # Validation
            errors = []

            if not ticker:
                errors.append("Ticker es requerido")
            if quantity <= 0:
                errors.append("Cantidad debe ser mayor a 0")
            if price <= 0:
                errors.append("Precio debe ser mayor a 0")

            if errors:
                for error in errors:
                    st.error(error)
            else:
                # Create transaction dict
                transaction = {
                    'date': tx_date.isoformat(),
                    'ticker': ticker,
                    'name': name if name else None,
                    'type': tx_type,
                    'asset_type': asset_type,
                    'quantity': quantity,
                    'price': price,
                    'total_amount': total_amount,
                    'currency': currency,
                    'platform': platform if platform else None,
                    'notes': notes if notes else None
                }

                # Save
                if save_transaction(transaction):
                    st.success(f"Transaccion guardada: {tx_type} {quantity:.4f} {ticker} @ ${price:,.4f}")

                    # Show summary
                    st.markdown("---")
                    st.markdown("#### Resumen")
                    st.json(transaction)
                else:
                    st.error("Error al guardar la transaccion")

    # Recent transactions preview
    st.markdown("---")
    st.markdown("#### Transacciones Recientes")
    st.info("Las transacciones recientes se mostraran aqui una vez conectado a la base de datos.")


if __name__ == "__main__":
    main()
