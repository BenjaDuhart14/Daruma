"""
Import Page - Import transactions from Delta CSV
Alpine Dusk Theme
"""

import streamlit as st
import pandas as pd
from utils import supabase_client as db
from utils.delta_parser import parse_delta_csv, get_import_summary
from utils.auth import check_password
from utils.styles import apply_styles, section_label, page_header

st.set_page_config(
    page_title="Import - Daruma",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply Alpine Dusk theme
apply_styles()

# Authentication check
check_password()


def parse_delta_csv_preview(content: str):
    """Parse Delta CSV for preview."""
    try:
        transactions = parse_delta_csv(content)
        summary = get_import_summary(transactions)
        return transactions, summary, None
    except Exception as e:
        return None, None, str(e)


def import_transactions(transactions: list) -> dict:
    """Import transactions to Supabase."""
    try:
        client = db.get_client()
        imported = 0
        skipped = 0
        errors = []

        progress_bar = st.progress(0)
        status_text = st.empty()

        for i, tx in enumerate(transactions):
            progress = (i + 1) / len(transactions)
            progress_bar.progress(progress)
            status_text.text(f"Processing {i+1}/{len(transactions)}: {tx['ticker']}")

            if db.transaction_exists(client, tx['ticker'], tx['date'][:10], tx['quantity']):
                skipped += 1
                continue

            try:
                result = db.insert_transaction(client, tx)
                if result:
                    imported += 1
                else:
                    errors.append(f"{tx['ticker']}: Error inserting")
            except Exception as e:
                errors.append(f"{tx['ticker']}: {str(e)}")

        progress_bar.empty()
        status_text.empty()

        return {
            'imported': imported,
            'skipped': skipped,
            'errors': errors,
            'success': True
        }
    except Exception as e:
        return {
            'imported': 0,
            'skipped': 0,
            'errors': [str(e)],
            'success': False
        }


def main():
    page_header("Import Data", "Import your transactions from Delta app", "📥")

    # Instructions card
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(6, 182, 212, 0.1) 100%);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
    ">
        <h4 style="color: var(--text-primary); margin: 0 0 16px 0; display: flex; align-items: center; gap: 8px;">
            📱 How to Export from Delta
        </h4>
        <ol style="color: var(--text-secondary); margin: 0; padding-left: 20px; line-height: 2;">
            <li>Open the <strong>Delta</strong> app on your phone</li>
            <li>Go to <strong>Settings</strong> → <strong>Export Data</strong></li>
            <li>Select <strong>Export as CSV</strong></li>
            <li>Upload the CSV file below</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

    # File uploader with custom styling
    uploaded_file = st.file_uploader(
        "Select your Delta CSV file",
        type=['csv'],
        help="CSV file exported from Delta app"
    )

    if uploaded_file is not None:
        content = uploaded_file.read().decode('utf-8')
        transactions, summary, error = parse_delta_csv_preview(content)

        if error:
            st.error(f"❌ Error parsing file: {error}")
            return

        if not transactions:
            st.warning("⚠️ No valid transactions found in the file")
            return

        st.markdown("---")

        # Preview header
        st.markdown("""
        <h3 style="color: var(--text-primary); margin-bottom: 20px;">📋 Import Preview</h3>
        """, unsafe_allow_html=True)

        # Summary metrics - 2x2 grid for mobile
        row1_col1, row1_col2 = st.columns(2)
        with row1_col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Transactions</div>
                <div class="metric-value">{summary['total_transactions']}</div>
            </div>
            """, unsafe_allow_html=True)

        with row1_col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Tickers</div>
                <div class="metric-value">{summary['unique_tickers']}</div>
            </div>
            """, unsafe_allow_html=True)

        row2_col1, row2_col2 = st.columns(2)
        with row2_col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Buy Orders</div>
                <div class="metric-value" style="color: var(--gain);">{summary['buy_count']}</div>
            </div>
            """, unsafe_allow_html=True)

        with row2_col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Sell Orders</div>
                <div class="metric-value" style="color: var(--loss);">{summary['sell_count']}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Asset types breakdown
        if summary['asset_types']:
            section_label("Asset Types")
            cols = st.columns(len(summary['asset_types']))
            type_colors = {'STOCK': '#8b5cf6', 'FUND': '#06b6d4', 'CRYPTO': '#f59e0b'}
            for i, (asset_type, count) in enumerate(summary['asset_types'].items()):
                with cols[i]:
                    color = type_colors.get(asset_type, '#8b5cf6')
                    st.markdown(f"""
                    <div style="
                        background: var(--bg-card);
                        border: 1px solid var(--border-subtle);
                        border-left: 3px solid {color};
                        border-radius: 8px;
                        padding: 16px;
                        text-align: center;
                    ">
                        <div style="color: var(--text-secondary); font-size: 12px; text-transform: uppercase;">{asset_type}</div>
                        <div style="color: var(--text-primary); font-size: 24px; font-weight: 700;">{count}</div>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Date range
        if summary['date_range']:
            section_label("Date Range")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div style="color: var(--text-secondary);">
                    📅 From: <strong style="color: var(--text-primary);">{summary['date_range']['earliest'][:10]}</strong>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div style="color: var(--text-secondary);">
                    📅 To: <strong style="color: var(--text-primary);">{summary['date_range']['latest'][:10]}</strong>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Preview table
        section_label("First 10 Transactions")

        preview_data = []
        for tx in transactions[:10]:
            preview_data.append({
                'Date': tx['date'][:10],
                'Type': tx['type'],
                'Ticker': tx['ticker'],
                'Quantity': f"{tx['quantity']:.4f}",
                'Price': f"${tx['price']:,.2f}",
                'Total': f"${tx['total_amount']:,.2f}"
            })

        df = pd.DataFrame(preview_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Tickers list
        with st.expander("📋 View all tickers"):
            st.write(", ".join(sorted(summary['tickers'])))

        st.markdown("---")

        # Import button
        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            if st.button("🚀 Import Transactions", type="primary", use_container_width=True):
                with st.spinner("Importing transactions..."):
                    result = import_transactions(transactions)

                if result['success']:
                    st.markdown(f"""
                    <div style="
                        background: var(--gain-bg);
                        border: 1px solid var(--gain);
                        border-radius: 12px;
                        padding: 20px;
                        text-align: center;
                        margin-top: 16px;
                    ">
                        <div style="font-size: 32px; margin-bottom: 8px;">✅</div>
                        <h3 style="color: var(--gain); margin: 0 0 8px 0;">Import Complete!</h3>
                        <p style="color: var(--text-secondary); margin: 0;">
                            <strong>{result['imported']}</strong> transactions imported<br>
                            <strong>{result['skipped']}</strong> duplicates skipped
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                    if result['imported'] > 0:
                        st.balloons()

                    if result['errors']:
                        with st.expander(f"⚠️ View {len(result['errors'])} errors"):
                            for err in result['errors']:
                                st.warning(err)
                else:
                    st.error(f"❌ Import failed: {result['errors'][0] if result['errors'] else 'Unknown error'}")

        # Duplicate warning
        st.markdown("""
        <div style="
            background: rgba(139, 92, 246, 0.08);
            border-left: 3px solid var(--accent-purple);
            border-radius: 0 8px 8px 0;
            padding: 16px;
            margin-top: 24px;
        ">
            <strong style="color: var(--text-primary);">💡 About Duplicates</strong>
            <p style="color: var(--text-secondary); margin: 8px 0 0 0; font-size: 14px;">
                The system automatically checks for existing transactions with the same date, ticker, and quantity to prevent duplicates.
            </p>
        </div>
        """, unsafe_allow_html=True)

    else:
        # Empty state
        st.markdown("""
        <div style="
            text-align: center;
            padding: 80px 20px;
            background: var(--bg-card);
            border-radius: 16px;
            border: 2px dashed var(--border-subtle);
            margin-top: 20px;
        ">
            <div style="font-size: 64px; margin-bottom: 20px;">📄</div>
            <h3 style="color: var(--text-primary); margin-bottom: 8px;">No File Selected</h3>
            <p style="color: var(--text-secondary);">Upload your Delta CSV file to preview and import your transactions.</p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
