"""
Add Transaction Page - Manual transaction entry
Alpine Dusk Theme
"""

import streamlit as st
from datetime import datetime, date
from utils import supabase_client as db
from utils.auth import check_password
from utils.styles import apply_styles, section_label, page_header

st.set_page_config(
    page_title="Add Transaction - Daruma",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply Alpine Dusk theme
apply_styles()

# Authentication check
check_password()


@st.cache_data(ttl=60)
def get_existing_tickers():
    """Get list of existing tickers for autocomplete."""
    try:
        client = db.get_client()
        return db.get_unique_tickers(client)
    except Exception:
        return []


@st.cache_data(ttl=60)
def get_recent_transactions(limit: int = 20):
    """Get recent transactions for display."""
    try:
        client = db.get_client()
        transactions = db.get_all_transactions(client)
        return transactions[:limit]
    except Exception:
        return []


def delete_transaction_by_id(tx_id: int) -> bool:
    """Delete a transaction and clear cache."""
    try:
        client = db.get_client()
        result = db.delete_transaction(client, tx_id)
        if result:
            get_existing_tickers.clear()
            get_recent_transactions.clear()
        return result
    except Exception:
        return False


def save_transaction(transaction: dict) -> bool:
    """Save transaction to Supabase."""
    try:
        client = db.get_client()
        result = db.insert_transaction(client, transaction)
        if result:
            get_existing_tickers.clear()
            get_recent_transactions.clear()
            return True
        return False
    except Exception as e:
        st.error(f"Error saving transaction: {str(e)}")
        return False


def main():
    page_header("Add Transaction", "Record a new buy or sell transaction", "➕")

    existing_tickers = get_existing_tickers()

    # Form container
    st.markdown("""
    <div style="
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
    ">
    </div>
    """, unsafe_allow_html=True)

    with st.form("transaction_form"):
        col1, col2 = st.columns(2)

        with col1:
            section_label("Transaction Details")

            tx_date = st.date_input(
                "Date",
                value=date.today(),
                max_value=date.today()
            )

            ticker = st.text_input(
                "Ticker Symbol",
                placeholder="e.g., AAPL, VOO, BTC",
                help="Enter the stock/ETF/crypto symbol"
            ).upper()

            if ticker and len(ticker) >= 1 and existing_tickers:
                suggestions = [t for t in existing_tickers if ticker in t]
                if suggestions and ticker not in suggestions:
                    st.caption(f"💡 Suggestions: {', '.join(suggestions[:5])}")

            name = st.text_input(
                "Asset Name (optional)",
                placeholder="e.g., Apple Inc, Vanguard S&P 500"
            )

            tx_type = st.radio(
                "Transaction Type",
                ["BUY", "SELL"],
                horizontal=True
            )

        with col2:
            section_label("Pricing")

            asset_type = st.selectbox(
                "Asset Type",
                ["STOCK", "FUND", "CRYPTO"],
                index=0
            )

            quantity = st.number_input(
                "Quantity",
                min_value=0.0,
                step=0.0001,
                format="%.4f"
            )

            price_method = st.radio(
                "Enter price as",
                ["Unit Price", "Total Amount"],
                horizontal=True
            )

            if price_method == "Unit Price":
                price = st.number_input(
                    "Unit Price (USD)",
                    min_value=0.0,
                    step=0.01,
                    format="%.4f"
                )
                total_amount = price * quantity if quantity else 0
                if total_amount > 0:
                    st.markdown(f"""
                    <div style="
                        background: rgba(139, 92, 246, 0.1);
                        border: 1px solid rgba(139, 92, 246, 0.2);
                        border-radius: 8px;
                        padding: 12px;
                        margin-top: 8px;
                    ">
                        <span style="color: var(--text-secondary); font-size: 12px;">TOTAL AMOUNT</span><br>
                        <span style="color: var(--text-primary); font-size: 18px; font-weight: 600;">${total_amount:,.2f}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                total_amount = st.number_input(
                    "Total Amount (USD)",
                    min_value=0.0,
                    step=0.01,
                    format="%.2f"
                )
                price = total_amount / quantity if quantity else 0
                if price > 0:
                    st.markdown(f"""
                    <div style="
                        background: rgba(139, 92, 246, 0.1);
                        border: 1px solid rgba(139, 92, 246, 0.2);
                        border-radius: 8px;
                        padding: 12px;
                        margin-top: 8px;
                    ">
                        <span style="color: var(--text-secondary); font-size: 12px;">UNIT PRICE</span><br>
                        <span style="color: var(--text-primary); font-size: 18px; font-weight: 600;">${price:,.4f}</span>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("---")

        # Additional fields
        col1, col2 = st.columns(2)

        with col1:
            currency = st.selectbox("Currency", ["USD", "CLP"], index=0)

        with col2:
            platform = st.text_input(
                "Platform (optional)",
                placeholder="e.g., Interactive Brokers, Binance"
            )

        notes = st.text_area(
            "Notes (optional)",
            placeholder="Any additional notes about this transaction...",
            max_chars=500
        )

        # Submit button
        submitted = st.form_submit_button("💾 Save Transaction", use_container_width=True)

        if submitted:
            errors = []
            if not ticker:
                errors.append("Ticker is required")
            if quantity <= 0:
                errors.append("Quantity must be greater than 0")
            if price <= 0:
                errors.append("Price must be greater than 0")

            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
            else:
                transaction = {
                    'date': datetime.combine(tx_date, datetime.min.time()).isoformat(),
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

                if save_transaction(transaction):
                    st.success(f"✅ Transaction saved: {tx_type} {quantity:.4f} {ticker} @ ${price:,.4f}")
                    st.balloons()
                    st.rerun()

    st.markdown("---")

    # Transaction Log
    section_label("Transaction Log")

    recent = get_recent_transactions(limit=20)

    if recent:
        # Filter controls
        col_filter1, col_filter2 = st.columns([2, 1])

        with col_filter1:
            all_tickers = sorted(set(tx['ticker'] for tx in recent))
            filter_ticker = st.selectbox(
                "Filter by ticker",
                ["All"] + all_tickers,
                key="tx_filter"
            )

        with col_filter2:
            filter_type = st.selectbox(
                "Filter by type",
                ["All", "BUY", "SELL"],
                key="type_filter"
            )

        # Apply filters
        filtered = recent
        if filter_ticker != "All":
            filtered = [tx for tx in filtered if tx['ticker'] == filter_ticker]
        if filter_type != "All":
            filtered = [tx for tx in filtered if tx['type'] == filter_type]

        st.caption(f"Showing {len(filtered)} of {len(recent)} transactions")

        # Transaction list
        for tx in filtered:
            is_buy = tx['type'] == 'BUY'
            tx_color = "#10b981" if is_buy else "#ef4444"
            tx_icon = "📈" if is_buy else "📉"
            tx_id = tx.get('id')

            col_info, col_delete = st.columns([5, 1])

            with col_info:
                st.markdown(f"""
                <div class="data-row" style="margin-bottom: 8px;">
                    <div style="display: flex; align-items: center; flex: 2;">
                        <div class="ticker-badge" style="background: {tx_color};">
                            {tx['ticker'][:2]}
                        </div>
                        <div>
                            <div class="ticker-name">{tx_icon} {tx['type']} {tx['ticker']}</div>
                            <div class="ticker-details">{tx['date'][:10] if tx['date'] else ''}</div>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div class="value-display">{float(tx['quantity'] or 0):.4f} @ ${float(tx['price'] or 0):,.2f}</div>
                        <div class="ticker-details">${float(tx['total_amount'] or 0):,.2f}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col_delete:
                if tx_id and st.button("🗑️", key=f"del_{tx_id}", help="Delete transaction"):
                    if delete_transaction_by_id(tx_id):
                        st.success(f"Deleted {tx['ticker']} transaction")
                        st.rerun()
                    else:
                        st.error("Failed to delete")
    else:
        st.markdown("""
        <div style="
            text-align: center;
            padding: 40px 20px;
            background: var(--bg-card);
            border-radius: 12px;
            border: 1px dashed var(--border-subtle);
        ">
            <p style="color: var(--text-secondary);">No transactions yet. Add your first transaction above.</p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
