"""UI styling and visual design tokens for EchoMind.

Premium dark-mode "AI SaaS" aesthetic: deep navy background, indigo glass
panels, purple/blue neon accents, Inter typography, and subtle glassmorphism.
Preserves the existing class names (em-header, em-badge, em-card, em-muted,
em-diff-box) so all pages keep working, and adds a hero + glass pill system.
"""

import streamlit as st


def apply_custom_styles() -> None:
    """Inject the premium glassmorphism theme."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

        :root {
            --em-bg:#0B1020; --em-panel:#121A32; --em-panel-2:#0F1730;
            --em-border:rgba(124,92,252,0.22); --em-border-strong:rgba(139,107,255,0.45);
            --em-purple:#8B6BFF; --em-blue:#4B8CFF; --em-pink:#F472B6; --em-cyan:#22D3EE;
            --em-green:#34D399; --em-text:#FFFFFF; --em-muted:#A9B0D0;
        }

        html, body, [class*="css"], .stMarkdown, .stMetric, button, input, textarea, select {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', sans-serif;
        }

        .stApp {
            background:
                radial-gradient(900px 500px at 12% -5%, rgba(139,107,255,0.16), transparent 55%),
                radial-gradient(800px 500px at 100% 0%, rgba(75,140,255,0.12), transparent 55%),
                radial-gradient(700px 500px at 90% 100%, rgba(34,211,238,0.06), transparent 55%),
                #0B1020;
        }
        .block-container { padding-top: 2.2rem; padding-bottom: 4rem; max-width: 1200px; }

        h1, h2, h3, h4, h5, h6 { color:#fff; font-weight:800; letter-spacing:-0.02em; margin-bottom:0.5rem; }
        p, span, label, li { color:#E9EBF6; line-height:1.55; }

        /* ---------------- Sidebar: glass panel ---------------- */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(45,38,110,0.45), rgba(18,26,50,0.30));
            backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
            border-right: 1px solid var(--em-border-strong);
            box-shadow: 12px 0 40px rgba(90,70,200,0.12);
        }
        section[data-testid="stSidebar"] [role="radiogroup"] > label {
            padding:8px 12px; border-radius:12px; margin-bottom:4px; border:1px solid transparent;
        }
        section[data-testid="stSidebar"] [role="radiogroup"] > label:has(input:checked) {
            background: linear-gradient(135deg, rgba(139,107,255,0.28), rgba(75,140,255,0.18));
            border:1px solid var(--em-border-strong);
            box-shadow: 0 8px 22px rgba(124,92,252,0.25);
        }

        /* ---------------- Hero ---------------- */
        .em-hero {
            position:relative; overflow:hidden; border-radius:24px; padding:30px 34px; margin-bottom:14px;
            background: linear-gradient(120deg, #211C57 0%, #3A2A82 42%, #1E3A8A 100%);
            border:1px solid var(--em-border-strong);
            box-shadow: 0 24px 70px rgba(70,54,160,0.38), inset 0 1px 0 rgba(255,255,255,0.07);
        }
        .em-hero::before {
            content:''; position:absolute; top:-45%; right:-8%; width:560px; height:360px;
            background: radial-gradient(circle at 30% 30%, rgba(139,107,255,0.55), transparent 60%),
                        radial-gradient(circle at 75% 60%, rgba(75,140,255,0.45), transparent 60%),
                        radial-gradient(circle at 55% 90%, rgba(244,114,182,0.30), transparent 60%);
            filter: blur(48px); opacity:.75; pointer-events:none;
        }
        .em-hero-row { position:relative; display:flex; align-items:center; gap:18px; }
        .em-hero h1 { margin:0 0 6px 0; font-size:2.3rem; font-weight:900; }
        .em-hero p  { margin:0; color:rgba(233,235,246,0.86); font-size:1.05rem; max-width:780px; }
        .em-logo {
            display:inline-flex; align-items:center; justify-content:center;
            width:56px; height:56px; border-radius:16px; font-size:28px; flex:0 0 auto;
            background: linear-gradient(135deg, rgba(139,107,255,0.9), rgba(75,140,255,0.85));
            border:1px solid rgba(255,255,255,0.18);
            box-shadow: 0 10px 26px rgba(124,92,252,0.55), inset 0 1px 0 rgba(255,255,255,0.25);
        }

        /* ---------------- Page header ---------------- */
        .em-header { margin: 8px 0 18px 0; padding-bottom: 10px; border-bottom: 1px solid var(--em-border); }
        .em-header-title { font-size:1.4rem; font-weight:800; color:#fff; margin:0; letter-spacing:-0.02em; }
        .em-header-subtitle { font-size:0.85rem; color:var(--em-muted); margin-top:4px; margin-bottom:0; }
        .em-kicker { text-transform:uppercase; letter-spacing:.18em; font-size:.72rem; font-weight:700; color:#9AA2CE; }

        /* ---------------- Badges / pills ---------------- */
        .em-badge, .em-pill {
            display:inline-flex; align-items:center; gap:8px; padding:6px 14px; border-radius:999px;
            font-size:.8rem; font-weight:600; color:#D7DBF5;
            background: rgba(18,26,50,0.55); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
            border:1px solid var(--em-border); box-shadow:0 2px 12px rgba(124,92,252,0.14);
        }
        .em-badge-neutral, .em-info { border-color:rgba(139,107,255,0.45); color:#CBBEFF; }
        .em-badge-success, .em-good { border-color:rgba(52,211,153,0.45); color:#8BEFC4; }
        .em-badge-warning, .em-warn { border-color:rgba(250,204,21,0.40); color:#FDE68A; }
        .em-badge-danger, .em-bad { border-color:rgba(244,114,182,0.45); color:#FBC7E4; }
        .em-badge-info { border-color:rgba(75,140,255,0.45); color:#BBD3FF; }
        .em-badge-dot, .em-dot {
            width:9px; height:9px; border-radius:50%; background:currentColor; display:inline-block;
        }
        .em-badge-success .em-badge-dot { background:var(--em-green); box-shadow:0 0 10px rgba(52,211,153,0.9); }

        /* ---------------- Cards / panels ---------------- */
        .em-card, .em-diff-box {
            border:1px solid var(--em-border); border-radius:16px; padding:1.1rem 1.2rem; margin-bottom:1rem;
            background: linear-gradient(180deg, rgba(18,26,50,0.6), rgba(15,23,48,0.4));
            box-shadow: 0 10px 30px rgba(10,14,32,0.35);
        }
        .em-diff-box { height:100%; margin-bottom:0; }
        .em-card-title { font-size:0.8rem; font-weight:700; color:#CBBEFF; margin-bottom:0.5rem;
            text-transform:uppercase; letter-spacing:.08em; }
        .em-muted { color:var(--em-muted); font-size:0.82rem; }

        /* ---------------- Chips ---------------- */
        .em-chips { display:flex; flex-wrap:wrap; gap:8px; margin:8px 0 4px 0; }
        .em-chip {
            background: rgba(18,26,50,0.6); border:1px solid var(--em-border); color:#D7DBF5;
            padding:8px 13px; border-radius:12px; font-size:.88rem; line-height:1.4;
        }

        /* ---------------- Metrics / dataframe / expander ---------------- */
        [data-testid="stMetric"] {
            background: linear-gradient(180deg, rgba(18,26,50,0.75), rgba(15,23,48,0.55));
            border:1px solid var(--em-border); border-radius:16px; padding:16px 18px;
            box-shadow: 0 8px 26px rgba(10,14,32,0.45);
        }
        [data-testid="stMetricValue"] { font-weight:800; }
        [data-testid="stMetricLabel"] { color:var(--em-muted) !important; }
        [data-testid="stDataFrame"] { border:1px solid var(--em-border); border-radius:12px; }
        div[data-testid="stExpander"] { border-radius:16px; border:1px solid var(--em-border); background: rgba(18,26,50,0.4); }
        [data-testid="stVerticalBlockBorderWrapper"] {
            border-radius:18px !important; border:1px solid var(--em-border) !important;
            background: linear-gradient(180deg, rgba(18,26,50,0.55), rgba(15,23,48,0.35)) !important;
        }
        hr { border-color: rgba(124,92,252,0.15); }

        /* ---------------- Buttons ---------------- */
        .stButton > button {
            border-radius:12px; font-weight:600; color:#E9EBF6; font-size:0.9rem;
            border:1px solid var(--em-border); background: rgba(18,26,50,0.6); padding:.55rem 1.1rem;
            transition: all .15s ease;
        }
        .stButton > button:hover {
            border-color:var(--em-border-strong); box-shadow:0 6px 18px rgba(124,92,252,0.22); transform:translateY(-1px);
        }
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #8B6BFF 0%, #5B7CFF 55%, #4B8CFF 100%); border:none; color:#fff;
            box-shadow: 0 10px 26px rgba(124,92,252,0.45);
        }

        /* ---------------- Inputs / selects ---------------- */
        [data-baseweb="input"], [data-baseweb="textarea"], [data-baseweb="select"] > div,
        .stTextInput input, .stTextArea textarea {
            background: rgba(18,26,50,0.6) !important; border:1px solid var(--em-border) !important;
            border-radius:12px !important; color:#fff !important;
        }
        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color:var(--em-border-strong) !important; box-shadow:0 0 0 3px rgba(139,107,255,0.20) !important;
        }

        /* ---------------- Tabs ---------------- */
        [data-baseweb="tab-list"] { gap:10px; border-bottom:1px solid rgba(124,92,252,0.14); }
        [data-baseweb="tab"] { font-weight:600; color:var(--em-muted); padding:8px 6px; }
        [data-baseweb="tab"][aria-selected="true"] { color:#fff; }
        [data-baseweb="tab-highlight"] {
            background: linear-gradient(90deg, #8B6BFF, #4B8CFF) !important; height:3px !important;
            border-radius:3px; box-shadow: 0 0 12px rgba(139,107,255,0.85);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    """Render the premium EchoMind hero card (shown once at the top of the app)."""
    st.markdown(
        """
        <div class="em-hero">
          <div class="em-hero-row">
            <span class="em-logo">🧠</span>
            <div>
              <h1>EchoMind</h1>
              <p>The content strategist that remembers what worked, learns your brand voice, and never repeats a losing idea.</p>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_header(title: str, subtitle: str = "") -> None:
    """Render a page header with a bold title and muted subtitle."""
    subtitle_html = f'<p class="em-header-subtitle">{subtitle}</p>' if subtitle else ""
    st.markdown(
        f"""
        <div class="em-header">
            <h1 class="em-header-title">{title}</h1>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def badge_html(text: str, variant: str = "neutral", dot: bool = False) -> str:
    """Return an HTML glass badge string with consistent styling."""
    dot_html = '<span class="em-badge-dot"></span>' if dot else ""
    return f'<span class="em-badge em-badge-{variant}">{dot_html}{text}</span>'
