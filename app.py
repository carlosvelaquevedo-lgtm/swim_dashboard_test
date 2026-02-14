import streamlit as st

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SwimForm AI",
    page_icon="🏊",
    layout="centered",
)

# ─────────────────────────────────────────────
# AGGRESSIVE BACKGROUND + MENU HIDE
# ─────────────────────────────────────────────
st.markdown("""
<style>
    .stApp, [data-testid="stAppViewContainer"], .main, .block-container {
        background: #0a1628 !important;
        background-image: linear-gradient(180deg, #0a1628 0%, #0f2847 30%, #0e3d6b 60%, #0f2847 100%) !important;
    }
    
    [data-testid="stAppViewContainer"],
    .main,
    .block-container {
        background: transparent !important;
    }

    .water-bg {
        position: fixed !important;
        inset: 0 !important;
        z-index: -999 !important;
        background: linear-gradient(180deg, #0a1628 0%, #0f2847 30%, #0e3d6b 60%, #0f2847 100%);
    }

    .water-bg::before {
        content: '';
        position: absolute;
        inset: 0;
        background: radial-gradient(ellipse at 20% 20%, rgba(6,182,212,0.15) 0%, transparent 50%),
                    radial-gradient(ellipse at 80% 80%, rgba(6,182,212,0.1) 0%, transparent 50%);
        animation: waterShimmer 8s ease-in-out infinite;
    }

    @keyframes waterShimmer {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 1; }
    }

    .lane-lines {
        position: fixed;
        inset: 0;
        z-index: -998;
        opacity: 0.03;
        background: repeating-linear-gradient(90deg, #22d3ee 0px, #22d3ee 4px, transparent 4px, transparent 150px);
    }

    /* Hide menu on landing */
    [data-testid="stToolbar"],
    button[kind="menu"],
    .st-emotion-cache-1cpxqw2 {
        display: none !important;
    }
</style>

<div class="water-bg"></div>
<div class="lane-lines"></div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
try:
    import stripe
    stripe.api_key = st.secrets["stripe"]["secret_key"]
    APP_BASE_URL = st.secrets["stripe"].get("base_url", "http://localhost:8501")
    STRIPE_CONFIGURED = True
except Exception:
    APP_BASE_URL = "http://localhost:8501"
    STRIPE_CONFIGURED = False

STRIPE_PAYMENT_LINK = "https://buy.stripe.com/test_8x2eVdaBSe7mf2JaIEao800"
IS_DEV = True

if "paid" not in st.session_state:
    st.session_state.paid = False


def show_landing_page():
    container = st.container()
    with container:
        # Header
        st.markdown("""
        <div style="padding: 20px 0; text-align: left;">
            <a href="#" style="font-family: 'Space Mono', monospace; font-size: 1.5rem; font-weight: 700; color: #06b6d4; text-decoration: none;">
                SwimForm AI
            </a>
        </div>
        """, unsafe_allow_html=True)

        # Hero
        st.markdown('<div style="padding: 60px 0 20px; text-align: center;">', unsafe_allow_html=True)
        st.markdown('<div class="hero-badge">⚡ Video analysis powered by Claude AI</div>', unsafe_allow_html=True)
        st.markdown('<h1>Find the <span class="highlight">one fix</span><br/>that makes you faster</h1>', unsafe_allow_html=True)
        st.markdown('<p class="hero-subtitle">Upload your swim video. Get a biomechanics report in 90 seconds. Fix what coaches miss.</p>', unsafe_allow_html=True)

        # CTA
        st.markdown("""
        <div class="cta-box">
            <div class="price-tag">$4.99 <span class="price-period">per analysis</span></div>
            <p class="price-note">One video • Full PDF report • Annotated playback</p>
        """, unsafe_allow_html=True)

        if st.button("🏊 Get Instant Analysis → $4.99", key="cta1", use_container_width=True):
            st.markdown(f'<meta http-equiv="refresh" content="0;url={STRIPE_PAYMENT_LINK}">', unsafe_allow_html=True)

        if IS_DEV:
            if st.button("Skip Payment – Demo Mode (testing only)", key="demo1", use_container_width=True):
                st.session_state.paid = True
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

        # Features Section
        st.markdown('<h2 class="section-title">What you get</h2>', unsafe_allow_html=True)
        cols = st.columns(3, gap="medium")
        features = [
            ("📊", "7 Biomechanical Metrics", "Stroke rate, DPS, entry angle, elbow drop, kick depth, head position, body rotation—all measured frame-by-frame."),
            ("🎯", "Ranked Issues (1-3)", "Not just a list. We tell you which fix will move the needle most based on your specific technique patterns."),
            ("🏊", "Drill Prescription", "Exact drills with rep counts, focus cues, and when to return to full stroke. No guessing."),
            ("🎥", "Side-by-Side Comparison", "Your stroke vs. Olympic reference footage with synchronized playback and annotation overlays."),
            ("📈", "Progress Tracking", "Upload follow-up videos. We'll chart your improvement across all metrics session by session."),
            ("⚡", "Instant PDF Download", "Complete report with screenshots, data tables, and drill cards. Share with coaches or keep for your records."),
        ]
        for i, (icon, title, desc) in enumerate(features):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="feature">
                    <div class="feature-icon">{icon}</div>
                    <h3 style="font-size: 1.25rem; font-weight: 600; margin-bottom: 12px; color: #22d3ee;">{title}</h3>
                    <p style="color: rgba(240, 253, 255, 0.7); line-height: 1.6;">{desc}</p>
                </div>
                """, unsafe_allow_html=True)

        # Demo Section
        st.markdown('<h2 class="section-title">See it in action</h2>', unsafe_allow_html=True)
        st.markdown("""
        <div style="background: rgba(15, 40, 71, 0.4); border: 1px solid rgba(6, 182, 212, 0.15); border-radius: 16px; padding: 40px; text-align: center; max-width: 900px; margin: 0 auto;">
            <h3 style="font-size: 1.5rem; margin-bottom: 12px; color: #22d3ee;">Demo Video Coming Soon</h3>
            <p style="font-size: 1.1rem; max-width: 500px; line-height: 1.6; margin: 0 auto;">
                We're finalizing a full walkthrough showing the upload, AI analysis, and instant PDF report generation.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Video Section
        st.markdown('<h2 class="section-title">Best camera angles</h2>', unsafe_allow_html=True)
        cols = st.columns(4, gap="medium")
        # Add your video cards here (you had only one in the paste)
        st.info("Video cards go here...")

        # How It Works
        st.markdown('<h2 class="section-title">How it works</h2>', unsafe_allow_html=True)
        cols = st.columns(3, gap="medium")
        steps = [
            ("1", "Pay $4.99", "Secure checkout via Stripe. Instant access."),
            ("2", "Upload Video", "10-15 sec clip. Side view underwater works best."),
            ("3", "Get Report", "AI analyzes in 90 sec. Download PDF + annotated video."),
        ]
        for i, (num, title, desc) in enumerate(steps):
            with cols[i]:
                st.markdown(f"""
                <div class="step">
                    <div class="step-number">{num}</div>
                    <h3 style="color: #22d3ee;">{title}</h3>
                    <p style="color: rgba(240, 253, 255, 0.7);">{desc}</p>
                </div>
                """, unsafe_allow_html=True)

        # Testimonial, Final CTA, Footer — add them here if you want

# ─────────────────────────────────────────────
# MAIN ROUTER
# ─────────────────────────────────────────────
query_params = st.query_params

if st.session_state.paid:
    try:
        import importlib.util
        import sys
        spec = importlib.util.spec_from_file_location("dashboard", "pages/2_Dashboard.py")
        dashboard_module = importlib.util.module_from_spec(spec)
        sys.modules["dashboard"] = dashboard_module
        spec.loader.exec_module(dashboard_module)
        dashboard_module.main()
    except Exception as e:
        st.error(f"Error loading dashboard: {e}")
else:
    success = query_params.get("success", [None])[0] == "true"
    demo = query_params.get("demo", [None])[0] == "true"
    cancel = query_params.get("payment", [None])[0] == "cancel"

    if success or demo:
        st.session_state.paid = True
        st.rerun()
    elif cancel:
        st.warning("Payment cancelled.")
        st.query_params.clear()
    else:
        show_landing_page()
