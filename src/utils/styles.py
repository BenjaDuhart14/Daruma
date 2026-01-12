"""
Daruma Design System - "Alpine Dusk" Theme
A luxurious fintech aesthetic inspired by twilight mountains.
"""

import streamlit as st

# Color Palette
COLORS = {
    # Backgrounds
    'bg_primary': '#0a0a12',
    'bg_secondary': '#12121c',
    'bg_card': 'rgba(20, 20, 35, 0.7)',
    'bg_card_hover': 'rgba(30, 30, 50, 0.8)',

    # Borders & Accents
    'border_glow': 'rgba(139, 92, 246, 0.3)',
    'border_subtle': 'rgba(255, 255, 255, 0.08)',
    'accent_purple': '#8b5cf6',
    'accent_cyan': '#06b6d4',
    'accent_pink': '#ec4899',

    # Text
    'text_primary': '#f8fafc',
    'text_secondary': '#94a3b8',
    'text_muted': '#64748b',

    # Semantic
    'gain': '#10b981',
    'gain_bg': 'rgba(16, 185, 129, 0.15)',
    'loss': '#ef4444',
    'loss_bg': 'rgba(239, 68, 68, 0.15)',

    # Gradients
    'gradient_purple': 'linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%)',
    'gradient_gain': 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
    'gradient_loss': 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)',
}

# Chart colors for Plotly
CHART_COLORS = {
    'bg': '#0a0a12',
    'paper': '#0a0a12',
    'grid': 'rgba(148, 163, 184, 0.1)',
    'gain': '#10b981',
    'loss': '#ef4444',
    'accent': '#8b5cf6',
    'text': '#94a3b8',
}


def get_base_styles():
    """Return the base CSS styles for the Alpine Dusk theme."""
    return """
    <style>
        /* ==================== FONTS ==================== */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

        /* ==================== ROOT VARIABLES ==================== */
        :root {
            --bg-primary: #0a0a12;
            --bg-secondary: #12121c;
            --bg-card: rgba(20, 20, 35, 0.7);
            --bg-card-hover: rgba(30, 30, 50, 0.8);
            --border-glow: rgba(139, 92, 246, 0.3);
            --border-subtle: rgba(255, 255, 255, 0.08);
            --accent-purple: #8b5cf6;
            --accent-cyan: #06b6d4;
            --accent-pink: #ec4899;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --gain: #10b981;
            --gain-bg: rgba(16, 185, 129, 0.15);
            --loss: #ef4444;
            --loss-bg: rgba(239, 68, 68, 0.15);
        }

        /* ==================== GLOBAL STYLES ==================== */
        .stApp {
            background: linear-gradient(180deg, #0a0a12 0%, #0f0a1a 50%, #12121c 100%);
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Mountain silhouette background */
        .stApp::before {
            content: '';
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            height: 40vh;
            background:
                linear-gradient(180deg, transparent 0%, rgba(10, 10, 18, 0.8) 100%),
                url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1440 320'%3E%3Cpath fill='%23161625' d='M0,224L48,213.3C96,203,192,181,288,181.3C384,181,480,203,576,218.7C672,235,768,245,864,234.7C960,224,1056,192,1152,181.3C1248,171,1344,181,1392,186.7L1440,192L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z'/%3E%3C/svg%3E");
            background-size: cover;
            background-position: bottom;
            pointer-events: none;
            z-index: 0;
            opacity: 0.6;
        }

        /* Header styling */
        header[data-testid="stHeader"] {
            background: linear-gradient(180deg, #0a0a12 0%, transparent 100%);
            backdrop-filter: blur(10px);
        }

        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        /* ==================== TYPOGRAPHY ==================== */
        h1, h2, h3, h4, h5, h6, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 700 !important;
            color: var(--text-primary) !important;
            letter-spacing: -0.02em;
        }

        p, span, div, label {
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        /* Page titles */
        .page-title {
            font-size: 28px;
            font-weight: 800;
            color: var(--text-primary);
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .page-subtitle {
            font-size: 14px;
            color: var(--text-secondary);
            margin-bottom: 24px;
        }

        /* Section headers */
        .section-label {
            font-size: 11px;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 12px;
        }

        /* ==================== METRIC CARDS ==================== */
        .metric-card {
            background: var(--bg-card);
            backdrop-filter: blur(20px);
            border: 1px solid var(--border-subtle);
            border-radius: 16px;
            padding: 20px 24px;
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
        }

        .metric-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, var(--accent-purple), var(--accent-cyan));
            opacity: 0.6;
        }

        .metric-card:hover {
            background: var(--bg-card-hover);
            border-color: var(--border-glow);
            transform: translateY(-2px);
        }

        .metric-label {
            font-size: 12px;
            font-weight: 500;
            color: var(--text-secondary);
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .metric-value {
            font-family: 'JetBrains Mono', monospace;
            font-size: 32px;
            font-weight: 700;
            color: var(--text-primary);
            line-height: 1.1;
        }

        .metric-value-large {
            font-family: 'JetBrains Mono', monospace;
            font-size: 48px;
            font-weight: 700;
            color: var(--text-primary);
            line-height: 1.1;
        }

        .metric-currency {
            font-size: 18px;
            color: var(--text-muted);
            font-weight: 500;
            margin-left: 6px;
        }

        .metric-change {
            font-size: 14px;
            font-weight: 600;
            margin-top: 8px;
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 4px 10px;
            border-radius: 20px;
        }

        .metric-change.gain {
            color: var(--gain);
            background: var(--gain-bg);
        }

        .metric-change.loss {
            color: var(--loss);
            background: var(--loss-bg);
        }

        /* Mini sparkline container */
        .sparkline-container {
            position: absolute;
            bottom: 12px;
            right: 16px;
            width: 80px;
            height: 40px;
            opacity: 0.6;
        }

        /* ==================== DATA TABLE ==================== */
        .data-row {
            background: var(--bg-card);
            backdrop-filter: blur(10px);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            transition: all 0.2s ease;
        }

        .data-row:hover {
            background: var(--bg-card-hover);
            border-color: var(--border-glow);
            transform: translateX(4px);
        }

        .ticker-badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, var(--accent-purple) 0%, var(--accent-pink) 100%);
            border-radius: 10px;
            font-weight: 700;
            font-size: 12px;
            color: white;
            margin-right: 12px;
        }

        .ticker-name {
            font-weight: 600;
            font-size: 15px;
            color: var(--text-primary);
        }

        .ticker-details {
            font-size: 12px;
            color: var(--text-muted);
            margin-top: 2px;
        }

        .value-display {
            font-family: 'JetBrains Mono', monospace;
            font-weight: 600;
            font-size: 15px;
            color: var(--text-primary);
        }

        .pnl-badge {
            font-family: 'JetBrains Mono', monospace;
            font-size: 13px;
            font-weight: 600;
            padding: 6px 12px;
            border-radius: 8px;
        }

        .pnl-badge.gain {
            color: var(--gain);
            background: var(--gain-bg);
        }

        .pnl-badge.loss {
            color: var(--loss);
            background: var(--loss-bg);
        }

        /* ==================== BUTTONS ==================== */
        .stButton > button {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 600 !important;
            border-radius: 10px !important;
            padding: 10px 20px !important;
            transition: all 0.2s ease !important;
            border: none !important;
        }

        .stButton > button[data-testid="baseButton-primary"] {
            background: linear-gradient(135deg, var(--accent-purple) 0%, #6366f1 100%) !important;
            color: white !important;
            box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3) !important;
        }

        .stButton > button[data-testid="baseButton-primary"]:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(139, 92, 246, 0.4) !important;
        }

        .stButton > button[data-testid="baseButton-secondary"] {
            background: var(--bg-card) !important;
            color: var(--text-secondary) !important;
            border: 1px solid var(--border-subtle) !important;
        }

        .stButton > button[data-testid="baseButton-secondary"]:hover {
            background: var(--bg-card-hover) !important;
            color: var(--text-primary) !important;
            border-color: var(--border-glow) !important;
        }

        /* Period selector buttons */
        .period-btn {
            background: var(--bg-card) !important;
            border: 1px solid var(--border-subtle) !important;
            color: var(--text-secondary) !important;
            font-size: 13px !important;
            font-weight: 600 !important;
            padding: 8px 16px !important;
            border-radius: 8px !important;
            transition: all 0.2s ease !important;
        }

        .period-btn:hover {
            background: var(--bg-card-hover) !important;
            color: var(--text-primary) !important;
        }

        .period-btn.active {
            background: var(--accent-purple) !important;
            color: white !important;
            border-color: var(--accent-purple) !important;
        }

        /* ==================== INPUTS ==================== */
        .stTextInput > div > div > input,
        .stSelectbox > div > div > div,
        .stNumberInput > div > div > input,
        .stDateInput > div > div > input,
        .stTextArea > div > div > textarea {
            background: var(--bg-card) !important;
            border: 1px solid var(--border-subtle) !important;
            border-radius: 10px !important;
            color: var(--text-primary) !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            padding: 12px 16px !important;
        }

        .stTextInput > div > div > input:focus,
        .stSelectbox > div > div > div:focus,
        .stNumberInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: var(--accent-purple) !important;
            box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.2) !important;
        }

        .stTextInput > label,
        .stSelectbox > label,
        .stNumberInput > label,
        .stDateInput > label,
        .stTextArea > label {
            color: var(--text-secondary) !important;
            font-weight: 500 !important;
            font-size: 13px !important;
        }

        /* Fix dropdown z-index - ensure dropdowns appear above other content */
        .stSelectbox > div {
            position: relative;
            z-index: 1000 !important;
        }

        .stSelectbox [data-baseweb="select"] {
            position: relative;
            z-index: 1000 !important;
        }

        .stSelectbox [data-baseweb="popover"] {
            z-index: 9999 !important;
        }

        div[data-baseweb="popover"] {
            z-index: 9999 !important;
        }

        div[data-baseweb="select"] > div {
            z-index: 1000 !important;
        }

        /* ==================== CHECKBOX & RADIO ==================== */
        .stCheckbox > label > div[data-testid="stMarkdownContainer"] > p,
        .stRadio > label > div[data-testid="stMarkdownContainer"] > p {
            color: var(--text-secondary) !important;
            font-size: 14px !important;
        }

        /* ==================== SIDEBAR ==================== */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f0a1a 0%, #12121c 100%) !important;
            border-right: 1px solid var(--border-subtle) !important;
        }

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
            color: var(--text-secondary) !important;
        }

        /* Sidebar navigation styling */
        [data-testid="stSidebarNav"] {
            padding-top: 20px;
        }

        [data-testid="stSidebarNav"] li {
            margin-bottom: 4px;
        }

        [data-testid="stSidebarNav"] a {
            background: transparent !important;
            border-radius: 10px !important;
            padding: 12px 16px !important;
            color: var(--text-secondary) !important;
            font-weight: 500 !important;
            transition: all 0.2s ease !important;
        }

        [data-testid="stSidebarNav"] a:hover {
            background: var(--bg-card) !important;
            color: var(--text-primary) !important;
        }

        [data-testid="stSidebarNav"] a[aria-selected="true"] {
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(99, 102, 241, 0.2) 100%) !important;
            color: var(--accent-purple) !important;
            border-left: 3px solid var(--accent-purple) !important;
        }

        /* ==================== METRICS ==================== */
        [data-testid="stMetric"] {
            background: var(--bg-card);
            backdrop-filter: blur(20px);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            padding: 16px 20px;
        }

        [data-testid="stMetricLabel"] {
            color: var(--text-secondary) !important;
            font-size: 12px !important;
            font-weight: 500 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
        }

        [data-testid="stMetricValue"] {
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 24px !important;
            font-weight: 700 !important;
            color: var(--text-primary) !important;
        }

        [data-testid="stMetricDelta"] {
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 13px !important;
            font-weight: 600 !important;
        }

        [data-testid="stMetricDelta"] svg {
            display: none;
        }

        /* ==================== DIVIDERS ==================== */
        hr {
            border: none !important;
            border-top: 1px solid var(--border-subtle) !important;
            margin: 24px 0 !important;
        }

        /* ==================== INFO/WARNING/ERROR BOXES ==================== */
        .stAlert {
            background: var(--bg-card) !important;
            border: 1px solid var(--border-subtle) !important;
            border-radius: 12px !important;
            color: var(--text-secondary) !important;
        }

        .stAlert [data-testid="stMarkdownContainer"] {
            color: var(--text-secondary) !important;
        }

        /* Success state */
        .element-container:has(.stSuccess) .stAlert {
            border-color: var(--gain) !important;
            background: var(--gain-bg) !important;
        }

        /* Error state */
        .element-container:has(.stError) .stAlert {
            border-color: var(--loss) !important;
            background: var(--loss-bg) !important;
        }

        /* ==================== EXPANDER ==================== */
        .streamlit-expanderHeader {
            background: var(--bg-card) !important;
            border: 1px solid var(--border-subtle) !important;
            border-radius: 10px !important;
            color: var(--text-secondary) !important;
            font-weight: 500 !important;
        }

        .streamlit-expanderHeader:hover {
            color: var(--text-primary) !important;
            border-color: var(--border-glow) !important;
        }

        .streamlit-expanderContent {
            background: var(--bg-secondary) !important;
            border: 1px solid var(--border-subtle) !important;
            border-top: none !important;
            border-radius: 0 0 10px 10px !important;
        }

        /* ==================== DATAFRAME ==================== */
        .stDataFrame {
            border-radius: 12px !important;
            overflow: hidden !important;
        }

        .stDataFrame [data-testid="stDataFrameResizable"] {
            background: var(--bg-card) !important;
            border: 1px solid var(--border-subtle) !important;
            border-radius: 12px !important;
        }

        /* ==================== FILE UPLOADER ==================== */
        [data-testid="stFileUploader"] {
            background: var(--bg-card) !important;
            border: 2px dashed var(--border-subtle) !important;
            border-radius: 12px !important;
            padding: 24px !important;
        }

        [data-testid="stFileUploader"]:hover {
            border-color: var(--accent-purple) !important;
        }

        /* ==================== PROGRESS BAR ==================== */
        .stProgress > div > div > div {
            background: linear-gradient(90deg, var(--accent-purple), var(--accent-cyan)) !important;
            border-radius: 10px !important;
        }

        /* ==================== ANIMATIONS ==================== */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes glow {
            0%, 100% {
                box-shadow: 0 0 5px rgba(139, 92, 246, 0.3);
            }
            50% {
                box-shadow: 0 0 20px rgba(139, 92, 246, 0.5);
            }
        }

        .animate-in {
            animation: fadeInUp 0.5s ease forwards;
        }

        /* ==================== CUSTOM SCROLLBAR ==================== */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: var(--bg-secondary);
        }

        ::-webkit-scrollbar-thumb {
            background: var(--border-glow);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: var(--accent-purple);
        }

        /* ==================== RESPONSIVE ==================== */

        /* Tablet breakpoint */
        @media (max-width: 768px) {
            .metric-value-large {
                font-size: 28px;
            }

            .metric-value {
                font-size: 20px;
            }

            .page-title {
                font-size: 22px;
            }

            .page-subtitle {
                font-size: 13px;
            }

            .metric-card {
                padding: 14px 16px;
                border-radius: 12px;
            }

            .metric-label {
                font-size: 10px;
            }

            .metric-change {
                font-size: 12px;
                padding: 3px 8px;
            }

            .data-row {
                padding: 12px 14px;
                border-radius: 10px;
            }

            .ticker-badge {
                width: 36px;
                height: 36px;
                font-size: 11px;
                border-radius: 8px;
                margin-right: 10px;
            }

            .ticker-name {
                font-size: 14px;
            }

            .ticker-details {
                font-size: 11px;
            }

            .value-display {
                font-size: 13px;
            }

            .pnl-badge {
                font-size: 12px;
                padding: 5px 10px;
            }

            .section-label {
                font-size: 10px;
                margin-bottom: 10px;
            }

            /* Chart margins */
            [data-testid="stPlotlyChart"] {
                margin-left: -10px;
                margin-right: -10px;
            }
        }

        /* Mobile breakpoint */
        @media (max-width: 480px) {
            .metric-value-large {
                font-size: 24px;
            }

            .metric-value {
                font-size: 18px;
            }

            .metric-currency {
                font-size: 14px;
            }

            .page-title {
                font-size: 20px;
                gap: 8px;
            }

            .page-title span {
                font-size: 24px !important;
            }

            .page-subtitle {
                font-size: 12px;
                margin-bottom: 16px;
            }

            .metric-card {
                padding: 12px 14px;
                border-radius: 10px;
            }

            .metric-label {
                font-size: 9px;
                letter-spacing: 0.3px;
                margin-bottom: 4px;
            }

            .metric-change {
                font-size: 11px;
                padding: 2px 6px;
                margin-top: 6px;
            }

            .data-row {
                padding: 12px;
                border-radius: 10px;
                margin-bottom: 6px;
            }

            .ticker-badge {
                width: 32px;
                height: 32px;
                font-size: 10px;
                border-radius: 8px;
                margin-right: 8px;
            }

            .ticker-name {
                font-size: 13px;
            }

            .ticker-details {
                font-size: 10px;
            }

            .value-display {
                font-size: 12px;
            }

            .pnl-badge {
                font-size: 11px;
                padding: 4px 8px;
                border-radius: 6px;
            }

            .section-label {
                font-size: 9px;
                letter-spacing: 1px;
                margin-bottom: 8px;
            }

            /* Sidebar collapsed on mobile */
            [data-testid="stSidebar"] {
                min-width: 0 !important;
            }

            /* Compact period selector buttons on mobile */
            .stButton > button {
                min-height: 38px !important;
                padding: 8px 10px !important;
                font-size: 12px !important;
            }

            /* Primary button (selected period) */
            .stButton > button[data-testid="baseButton-primary"] {
                background: var(--accent-purple) !important;
            }

            /* Secondary button (unselected period) */
            .stButton > button[data-testid="baseButton-secondary"] {
                background: rgba(20, 20, 35, 0.6) !important;
            }

            /* Input fields */
            .stTextInput > div > div > input,
            .stSelectbox > div > div > div,
            .stNumberInput > div > div > input {
                padding: 10px 12px !important;
                font-size: 16px !important; /* Prevents zoom on iOS */
            }
        }

        /* Small mobile breakpoint */
        @media (max-width: 375px) {
            .metric-value-large {
                font-size: 22px;
            }

            .metric-value {
                font-size: 16px;
            }

            .page-title {
                font-size: 18px;
            }

            .metric-card {
                padding: 10px 12px;
            }

            .data-row {
                padding: 10px;
            }

            .ticker-badge {
                width: 28px;
                height: 28px;
                font-size: 9px;
            }

            /* Even more compact buttons on small phones */
            .stButton > button {
                min-height: 36px !important;
                padding: 6px 8px !important;
                font-size: 11px !important;
            }
        }

        /* ==================== MOBILE LAYOUT HELPERS ==================== */

        /* Mobile-friendly data row (stacks content) */
        .data-row-mobile {
            background: var(--bg-card);
            backdrop-filter: blur(10px);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            padding: 14px;
            margin-bottom: 8px;
            transition: all 0.2s ease;
        }

        .data-row-mobile .row-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 10px;
        }

        .data-row-mobile .row-left {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .data-row-mobile .row-details {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 6px;
        }

        .data-row-mobile .detail-item {
            text-align: center;
            padding: 6px;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 6px;
        }

        .data-row-mobile .detail-label {
            font-size: 8px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.3px;
            margin-bottom: 2px;
        }

        .data-row-mobile .detail-value {
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
            font-weight: 600;
            color: var(--text-primary);
        }

        /* Small phone optimizations for data rows */
        @media (max-width: 375px) {
            .data-row-mobile {
                padding: 10px;
            }

            .data-row-mobile .row-details {
                gap: 4px;
            }

            .data-row-mobile .detail-item {
                padding: 5px;
            }

            .data-row-mobile .detail-value {
                font-size: 11px;
            }
        }

        /* Period buttons container - horizontal scroll on mobile */
        .period-buttons {
            display: flex;
            gap: 6px;
            overflow-x: auto;
            padding-bottom: 8px;
            -webkit-overflow-scrolling: touch;
            scrollbar-width: none;
        }

        .period-buttons::-webkit-scrollbar {
            display: none;
        }

        .period-buttons .period-btn {
            flex-shrink: 0;
            min-width: 44px;
            padding: 10px 14px;
            font-size: 13px;
            font-weight: 600;
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: 8px;
            color: var(--text-secondary);
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .period-buttons .period-btn:active {
            background: var(--bg-card-hover);
            transform: scale(0.96);
        }

        .period-buttons .period-btn.active {
            background: var(--accent-purple);
            color: white;
            border-color: var(--accent-purple);
        }

        /* Touch-friendly active states */
        @media (hover: none) {
            .metric-card:active {
                background: var(--bg-card-hover);
                transform: scale(0.98);
            }

            .data-row:active,
            .data-row-mobile:active {
                background: var(--bg-card-hover);
                transform: scale(0.99);
            }

            /* Remove hover effects on touch devices */
            .metric-card:hover,
            .data-row:hover {
                transform: none;
            }
        }
    </style>
    """


def apply_styles():
    """Apply the Alpine Dusk theme styles to the current page."""
    st.markdown(get_base_styles(), unsafe_allow_html=True)


def metric_card(label: str, value: str, change: str = None, change_type: str = "gain"):
    """Render a styled metric card."""
    change_html = ""
    if change:
        change_class = "gain" if change_type == "gain" else "loss"
        arrow = "+" if change_type == "gain" else ""
        change_html = f'<span class="metric-change {change_class}">{arrow}{change}</span>'

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {change_html}
    </div>
    """, unsafe_allow_html=True)


def page_header(title: str, subtitle: str = "", icon: str = ""):
    """Render a styled page header."""
    icon_html = f'<span style="font-size: 32px;">{icon}</span>' if icon else ""
    subtitle_html = f'<p class="page-subtitle">{subtitle}</p>' if subtitle else ""

    st.markdown(f"""
    <div class="page-title">{icon_html}{title}</div>
    {subtitle_html}
    """, unsafe_allow_html=True)


def section_label(text: str):
    """Render a styled section label."""
    st.markdown(f'<div class="section-label">{text}</div>', unsafe_allow_html=True)


def get_chart_layout(height: int = 300):
    """Return common Plotly chart layout settings for the theme."""
    return dict(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=10, b=40),
        height=height,
        font=dict(
            family='Plus Jakarta Sans, sans-serif',
            color='#94a3b8'
        ),
        xaxis=dict(
            showgrid=False,
            color='#64748b',
            tickfont=dict(size=11)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(148, 163, 184, 0.1)',
            color='#64748b',
            tickfont=dict(size=11)
        ),
        showlegend=False,
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='#1e1e2e',
            bordercolor='#8b5cf6',
            font=dict(family='JetBrains Mono', size=12, color='#f8fafc')
        )
    )
