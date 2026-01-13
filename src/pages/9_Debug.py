"""
Debug script to test Supabase connection on Streamlit Cloud.
Add this as a temporary page to diagnose connection issues.
"""

import streamlit as st

st.set_page_config(page_title="Debug", page_icon="🔧")

st.title("🔧 Connection Debug")

# Show secrets detection
st.subheader("1. Secrets Detection")

try:
    st.write(f"st.secrets keys: {list(st.secrets.keys())}")

    if "SUPABASE_URL" in st.secrets:
        st.success("✅ SUPABASE_URL found at root level")
        url = st.secrets["SUPABASE_URL"]
        st.code(f"URL: {url[:50]}...")
    elif "auth" in st.secrets and "SUPABASE_URL" in st.secrets["auth"]:
        st.success("✅ SUPABASE_URL found under [auth]")
        url = st.secrets["auth"]["SUPABASE_URL"]
        st.code(f"URL: {url[:50]}...")
    else:
        st.error("❌ SUPABASE_URL not found!")
        st.write("Available keys:", list(st.secrets.keys()))
        if "auth" in st.secrets:
            st.write("Keys under [auth]:", list(st.secrets["auth"].keys()))
        url = None

    if "SUPABASE_KEY" in st.secrets:
        st.success("✅ SUPABASE_KEY found at root level")
    elif "auth" in st.secrets and "SUPABASE_KEY" in st.secrets["auth"]:
        st.success("✅ SUPABASE_KEY found under [auth]")
    else:
        st.error("❌ SUPABASE_KEY not found!")

except Exception as e:
    st.error(f"Error reading secrets: {e}")

# Test connection
st.subheader("2. Database Connection")

try:
    from utils import supabase_client as db
    client = db.get_client()
    st.success("✅ Supabase client created!")

    # Test queries
    st.subheader("3. Data Check")

    txns = db.get_all_transactions(client)
    st.write(f"Transactions: {len(txns)}")

    prices = db.get_current_prices(client)
    st.write(f"Current prices: {len(prices)}")

    holdings = db.get_holdings_with_value(client)
    st.write(f"Holdings: {len(holdings)}")

    if holdings:
        st.write("Sample holding:", holdings[0])

    summary = db.get_portfolio_summary(client)
    st.write("Portfolio summary:", summary)

except Exception as e:
    st.error(f"Connection error: {e}")
    import traceback
    st.code(traceback.format_exc())
