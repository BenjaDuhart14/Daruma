"""
Authentication module for Daruma.
Simple password protection with Alpine Dusk themed login page.

Secrets should contain:
    [auth]
    email = "your@email.com"
    password = "your-password"
"""

import streamlit as st


def _apply_login_styles():
    """Apply custom styles for the login page."""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

        :root {
            --bg-primary: #0a0a12;
            --bg-card: rgba(20, 20, 35, 0.8);
            --border-subtle: rgba(255, 255, 255, 0.08);
            --border-glow: rgba(139, 92, 246, 0.4);
            --accent-purple: #8b5cf6;
            --accent-cyan: #06b6d4;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
        }

        .stApp {
            background: linear-gradient(180deg, #0a0a12 0%, #0f0a1a 50%, #12121c 100%);
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        /* Mountain silhouette background */
        .stApp::before {
            content: '';
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            height: 50vh;
            background:
                linear-gradient(180deg, transparent 0%, rgba(10, 10, 18, 0.9) 100%),
                url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1440 320'%3E%3Cpath fill='%23161625' d='M0,224L48,213.3C96,203,192,181,288,181.3C384,181,480,203,576,218.7C672,235,768,245,864,234.7C960,224,1056,192,1152,181.3C1248,171,1344,181,1392,186.7L1440,192L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z'/%3E%3C/svg%3E");
            background-size: cover;
            background-position: bottom;
            pointer-events: none;
            z-index: 0;
            opacity: 0.7;
        }

        /* Aurora glow effect */
        .stApp::after {
            content: '';
            position: fixed;
            top: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 100%;
            height: 60vh;
            background: radial-gradient(ellipse at center top, rgba(139, 92, 246, 0.15) 0%, transparent 60%);
            pointer-events: none;
            z-index: 0;
        }

        header[data-testid="stHeader"] {
            background: transparent;
        }

        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        /* Hide sidebar completely on login page */
        [data-testid="stSidebar"] {
            display: none !important;
        }
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        [data-testid="collapsedControl"] {
            display: none !important;
        }
        section[data-testid="stSidebar"] {
            display: none !important;
        }

        /* Login container */
        .login-container {
            position: relative;
            z-index: 1;
            max-width: 420px;
            margin: 60px auto 0;
            padding: 48px 40px;
            background: var(--bg-card);
            backdrop-filter: blur(20px);
            border: 1px solid var(--border-subtle);
            border-radius: 24px;
            box-shadow:
                0 4px 30px rgba(0, 0, 0, 0.3),
                0 0 60px rgba(139, 92, 246, 0.1);
            animation: fadeInUp 0.6s ease forwards;
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .login-header {
            text-align: center;
            margin-bottom: 40px;
        }

        .login-logo {
            width: 80px;
            height: 80px;
            margin: 0 auto 20px;
            background: linear-gradient(135deg, var(--accent-purple) 0%, var(--accent-cyan) 100%);
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 10px 30px rgba(139, 92, 246, 0.3);
            animation: float 3s ease-in-out infinite;
            padding: 12px;
        }
        
        .login-logo svg {
            width: 100%;
            height: 100%;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-8px); }
        }

        .login-title {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 32px;
            font-weight: 800;
            color: var(--text-primary);
            margin: 0;
            letter-spacing: -0.02em;
        }

        .login-subtitle {
            font-size: 14px;
            color: var(--text-secondary);
            margin-top: 8px;
        }

        /* Form inputs */
        .stTextInput > div > div > input {
            background: rgba(15, 15, 25, 0.6) !important;
            border: 1px solid var(--border-subtle) !important;
            border-radius: 12px !important;
            color: var(--text-primary) !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-size: 15px !important;
            padding: 14px 18px !important;
            transition: all 0.2s ease !important;
        }

        .stTextInput > div > div > input:focus {
            border-color: var(--accent-purple) !important;
            box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2) !important;
        }

        .stTextInput > div > div > input::placeholder {
            color: var(--text-muted) !important;
        }

        .stTextInput > label {
            color: var(--text-secondary) !important;
            font-weight: 500 !important;
            font-size: 13px !important;
            margin-bottom: 6px !important;
        }

        /* Login button */
        .stButton > button {
            width: 100%;
            background: linear-gradient(135deg, var(--accent-purple) 0%, #6366f1 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 14px 28px !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-size: 16px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 20px rgba(139, 92, 246, 0.4) !important;
            margin-top: 8px !important;
        }

        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 30px rgba(139, 92, 246, 0.5) !important;
        }

        .stButton > button:active {
            transform: translateY(0) !important;
        }

        /* Error message */
        .stAlert {
            background: rgba(239, 68, 68, 0.1) !important;
            border: 1px solid rgba(239, 68, 68, 0.3) !important;
            border-radius: 12px !important;
            color: #fca5a5 !important;
        }

        /* Quote section */
        .login-quote {
            margin-top: 32px;
            padding: 20px;
            background: rgba(139, 92, 246, 0.08);
            border-left: 3px solid var(--accent-purple);
            border-radius: 0 12px 12px 0;
        }

        .login-quote p {
            font-size: 14px;
            color: var(--text-secondary);
            font-style: italic;
            margin: 0;
            line-height: 1.6;
        }

        .login-quote .quote-author {
            font-size: 12px;
            color: var(--text-muted);
            font-style: normal;
            margin-top: 8px;
            display: block;
        }

        /* Footer text */
        .login-footer {
            text-align: center;
            margin-top: 32px;
            font-size: 12px;
            color: var(--text-muted);
        }
    </style>
    """, unsafe_allow_html=True)


def _show_login_page(show_error: bool = False):
    """Display the styled login page."""
    _apply_login_styles()

    # Center content
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("""
        <div class="login-container">
            <div class="login-header">
                <div class="login-logo">
                    <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                        <ellipse cx="50" cy="55" rx="40" ry="42" fill="#dc2626"/>
                        <ellipse cx="50" cy="55" rx="38" ry="40" fill="#ef4444"/>
                        <ellipse cx="50" cy="48" rx="28" ry="24" fill="#fef3c7"/>
                        <circle cx="38" cy="45" r="10" fill="#1f2937"/>
                        <circle cx="36" cy="43" r="3" fill="white"/>
                        <circle cx="62" cy="45" r="10" fill="none" stroke="#1f2937" stroke-width="2"/>
                        <path d="M28 35 Q38 32 48 36" stroke="#1f2937" stroke-width="2" fill="none"/>
                        <path d="M52 36 Q62 32 72 35" stroke="#1f2937" stroke-width="2" fill="none"/>
                        <path d="M40 60 Q50 56 60 60" stroke="#1f2937" stroke-width="2" fill="none"/>
                    </svg>
                </div>
                <h1 class="login-title">Daruma</h1>
                <p class="login-subtitle">Investment Portfolio Tracker</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Form inputs (rendered by Streamlit but styled by CSS)
        st.text_input("Email", key="login_email", placeholder="your@email.com")
        st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")

        if show_error:
            st.error("Incorrect email or password")

        st.button("Sign In", on_click=_credentials_entered, use_container_width=True)

        st.markdown("""
        <div class="login-quote">
            <p>"The first $100,000 is the hardest — but after that, it gets easier."</p>
            <span class="quote-author">— Charlie Munger</span>
        </div>
        <p class="login-footer">Built with patience. One step at a time.</p>
        """, unsafe_allow_html=True)


def _credentials_entered():
    """Validate the entered credentials.
    
    Secrets should contain:
        [auth]
        email = "user@example.com"
        password = "your-password"  # Plain text password
    """
    try:
        entered_email = st.session_state.get("login_email", "").strip()
        entered_password = st.session_state.get("login_password", "")
        
        stored_email = st.secrets["auth"]["email"].strip()
        stored_password = st.secrets["auth"].get("password", "")
        
        # Simple password check
        if entered_email == stored_email and entered_password == stored_password:
            st.session_state["authenticated"] = True
            # Clear password from session for security
            if "login_password" in st.session_state:
                del st.session_state["login_password"]
        else:
            st.session_state["authenticated"] = False
    except Exception:
        st.session_state["authenticated"] = False


def check_password():
    """Returns True if user entered correct email and password."""
    if st.session_state.get("authenticated"):
        return True

    if "authenticated" not in st.session_state:
        _show_login_page(show_error=False)
        st.stop()

    if not st.session_state.get("authenticated"):
        _show_login_page(show_error=True)
        st.stop()

    return True


def logout():
    """Logout the current user."""
    st.session_state["authenticated"] = False
    if "login_email" in st.session_state:
        del st.session_state["login_email"]
    st.rerun()


def is_authenticated():
    """Check if user is currently authenticated."""
    return st.session_state.get("authenticated", False)
