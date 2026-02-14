import streamlit as st

# =============================================
# PAGE CONFIG
# =============================================
st.set_page_config(
    page_title="SwimForm AI",
    page_icon="🏊",
    layout="wide",                      # wide is better for full background
    initial_sidebar_state="expanded"    # sidebar open by default
)

# =============================================
# BACKGROUND + MENU HIDE
# =============================================
st.markdown("""
<style>
    /* Full background */
    .stApp, [data-testid="stAppViewContainer"], .main, .block-container {
        background: #0a1628 !important;
        background-image: linear-gradient(180deg, #0a1628 0%, #0f2847 30%, #0e3d6b 60%, #0f2847 100%) !important;
    }

    /* Water effect layers */
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
        background: 
            radial-gradient(ellipse at 20% 20%, rgba(6,182,212,0.15) 0%, transparent 50%),
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

    /* Hide top toolbar / menu on landing */
    header button[aria-label="View more options"],
    [data-testid="stToolbar"],
    button[kind="menu"],
    .st-emotion-cache-1cpxqw2 {
        display: none !important;
    }

    /* Section titles */
    .section-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 60px 0 40px;
        color: #f0fdff;
    }

    /* Feature cards */
    .feature-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(6,182,212,0.2);
        border-radius: 16px;
        padding: 24px;
        height: 100%;
        transition: all 0.3s;
    }
    .feature-card:hover {
        transform: translateY(-6px);
        background: rgba(6,182,212,0.08);
        border-color: #06b6d4;
    }
</style>

<div class="water-bg"></div>
<div class="lane-lines"></div>
""", unsafe_allow_html=True)

# =============================================
# CONFIG
# =============================================
STRIPE_PAYMENT_LINK = "https://buy.stripe.com/test_8x2eVdaBSe7mf2JaIEao800"
IS_DEV = True

if "paid" not in st.session_state:
    st.session_state.paid = False


def show_landing_page():
    # Header / Logo
    st.markdown("""
    <div style="padding: 20px 0; text-align: left;">
        <a href="#" style="font-family: 'Space Mono', monospace; font-size: 1.8rem; font-weight: 700; color: #06b6d4; text-decoration: none; display: inline-flex; align-items: center; gap: 12px;">
            <svg width="36" height="36" viewBox="0 0 36 36">
                <circle cx="18" cy="18" r="16" fill="none" stroke="#06b6d4" stroke-width="3"/>
                <path d="M10 18 Q18 13 26 18" stroke="#22d3ee" stroke-width="4" fill="none"/>
            </svg>
            SwimForm AI
        </a>
    </div>
    """, unsafe_allow_html=True)

    # Hero Section
    st.markdown('<div style="padding: 80px 0 40px; text-align: center;">', unsafe_allow_html=True)
    st.markdown('<div style="background: rgba(6,182,212,0.15); border: 1px solid #06b6d4; border-radius: 50px; padding: 10px 24px; display: inline-block; margin-bottom: 24px; color: #22d3ee; font-weight: 600;">⚡ AI-Powered Video Analysis</div>', unsafe_allow_html=True)
    st.markdown('<h1 style="font-size: 3.8rem; line-height: 1.1; color: white;">Find the <span style="background: linear-gradient(90deg, #06b6d4, #22d3ee); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">One Fix</span><br>That Makes You Faster</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 1.4rem; color: #d1d5db; max-width: 760px; margin: 24px auto;">Upload your swim video. Get a full biomechanics report in under 90 seconds.</p>', unsafe_allow_html=True)

    # CTA Buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🏊 Get Instant Analysis — $4.99", key="cta_main", use_container_width=True, type="primary"):
            st.markdown(f'<meta http-equiv="refresh" content="0;url={STRIPE_PAYMENT_LINK}">', unsafe_allow_html=True)

        if IS_DEV:
            if st.button("Developer: Skip Payment (Demo)", key="demo_skip"):
                st.session_state.paid = True
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # Features Grid
    st.markdown('<h2 class="section-title">What You Get</h2>', unsafe_allow_html=True)
    f_cols = st.columns(3)
    features = [
        ("📊", "7 Key Biometrics", "Stroke rate, DPS, entry angle, elbow position, body roll, kick depth & symmetry — all frame-by-frame."),
        ("🎯", "Prioritized Fixes", "We rank your 1–3 biggest issues so you know exactly what to fix first."),
        ("🎥", "Pro Comparison", "Side-by-side view: your stroke vs. Olympic-level reference footage.")
    ]
    for i, (icon, title, desc) in enumerate(features):
        with f_cols[i]:
            st.markdown(f"""
            <div class="feature-card">
                <div style="font-size: 2.8rem; margin-bottom: 16px;">{icon}</div>
                <h3 style="color: #22d3ee; margin-bottom: 12px;">{title}</h3>
                <p style="color: rgba(240,253,255,0.8);">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    # Demo Section
    st.markdown('<h2 class="section-title">See It in Action</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background: rgba(15,40,71,0.4); border: 1px solid rgba(6,182,212,0.2); border-radius: 16px; padding: 40px; text-align: center; max-width: 900px; margin: 0 auto;">
        <h3 style="font-size: 1.8rem; margin-bottom: 16px; color: #22d3ee;">Demo Video Coming Soon</h3>
        <p style="font-size: 1.15rem; max-width: 600px; margin: 0 auto; color: rgba(240,253,255,0.9);">
            Full walkthrough: upload → AI analysis → instant PDF report.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Best Camera Angles (placeholder)
    st.markdown('<h2 class="section-title">Best Camera Angles</h2>', unsafe_allow_html=True)
    st.info("Add your video card SVGs / descriptions here...")

    # How It Works
    st.markdown('<h2 class="section-title">How It Works</h2>', unsafe_allow_html=True)
    cols = st.columns(3)
    steps = [
        ("1", "Pay $4.99", "Secure checkout via Stripe. Instant access."),
        ("2", "Upload Video", "10–15 sec clip. Side underwater works best."),
        ("3", "Get Report", "AI analyzes in ~90 sec. Download PDF + annotated video.")
    ]
    for i, (num, title, desc) in enumerate(steps):
        with cols[i]:
            st.markdown(f"""
            <div class="step-box">
                <div class="step-num">{num}</div>
                <h3 style="color: #22d3ee;">{title}</h3>
                <p style="color: rgba(240,253,255,0.8);">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    # Testimonial + Final CTA + Footer (your original)
    st.markdown("""
    <div style="background: rgba(15,40,71,0.4); border: 1px solid rgba(6,182,212,0.2); border-radius: 20px; padding: 40px; max-width: 800px; margin: 60px auto; text-align: center;">
        <div style="font-size: 2rem; color: #fbbf24; margin-bottom: 16px;">★★★★★</div>
        <blockquote style="font-size: 1.2rem; line-height: 1.7; color: #f0fdff; font-style: italic; margin-bottom: 24px;">
            "Caught a dropped elbow I completely missed. Dropped 0.4s in her next 100 free after two weeks."
        </blockquote>
        <div style="display: flex; align-items: center; justify-content: center; gap: 16px;">
            <div style="width: 60px; height: 60px; border-radius: 50%; background: linear-gradient(135deg, #06b6d4, #22d3ee); color: #0a1628; font-weight: 700; display: flex; align-items: center; justify-content: center;">MK</div>
            <div>
                <h4 style="color: #22d3ee; margin: 0;">Mike K.</h4>
                <p style="color: #94a3b8; margin: 4px 0 0;">Head Coach, Aquatic Stars SC</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Final CTA
    st.markdown('<div style="text-align: center; margin: 80px 0;">', unsafe_allow_html=True)
    st.markdown('<h2 style="color: white;">Ready to Find Your Speed Leak?</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color: #d1d5db; margin: 16px 0;">One video. One analysis. One fix that changes everything.</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🏊 Get Instant Analysis — $4.99", key="cta_final", use_container_width=True, type="primary"):
            st.markdown(f'<meta http-equiv="refresh" content="0;url={STRIPE_PAYMENT_LINK}">', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div style="padding: 60px 0 40px; text-align: center; color: #64748b; border-top: 1px solid rgba(6,182,212,0.15);">
        © 2026 SwimForm AI · 
        <a href="#" style="color: #06b6d4; text-decoration: none;">Privacy</a> · 
        <a href="#" style="color: #06b6d4; text-decoration: none;">Terms</a> · 
        <a href="mailto:support@swimform.ai" style="color: #06b6d4; text-decoration: none;">support@swimform.ai</a>
    </div>
    """, unsafe_allow_html=True)


# =============================================
# MAIN ROUTER
# =============================================
if st.session_state.paid:
    # Load your dashboard page
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
    show_landing_page()
