import streamlit as st
import streamlit.components.v1 as components

import streamlit as st

# ─────────────────────────────────────────────
# PAGE CONFIG - Wide + Expanded
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SwimForm AI",
    page_icon="🏊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# AGGRESSIVE BACKGROUND + MENU CONTROL
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* FORCE BACKGROUND */
    .stApp, [data-testid="stAppViewContainer"], .main, .block-container {
        background: #0a1628 !important;
        background-image: linear-gradient(180deg, #0a1628 0%, #0f2847 30%, #0e3d6b 60%, #0f2847 100%) !important;
        color: white !important;
    }

    /* Background layers */
    .water-bg {
        position: fixed !important;
        top: 0 !important; left: 0 !important; right: 0 !important; bottom: 0 !important;
        z-index: -999 !important;
        background: linear-gradient(180deg, #0a1628 0%, #0f2847 30%, #0e3d6b 60%, #0f2847 100%);
        pointer-events: none;
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

    /* HIDE MENU ON LANDING PAGE */
    [data-testid="stToolbar"],
    button[kind="menu"],
    .st-emotion-cache-1cpxqw2 {
        display: none !important;
    }
</style>

<!-- Background layers -->
<div class="water-bg"></div>
<div class="lane-lines"></div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CONFIG & SECRETS
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
    # Your full content goes here (unchanged from your original)
    st.markdown("""
    <div style="padding: 20px 0; text-align: left;">
        <a href="#" style="font-family: 'Space Mono', monospace; font-size: 1.5rem; font-weight: 700; color: #06b6d4; text-decoration: none;">
            SwimForm AI
        </a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="padding: 60px 0 20px; text-align: center;">', unsafe_allow_html=True)
    st.markdown('<div class="hero-badge">⚡ Video analysis powered by Claude AI</div>', unsafe_allow_html=True)
    st.markdown('<h1>Find the <span class="highlight">one fix</span><br/>that makes you faster</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Upload your swim video. Get a biomechanics report in 90 seconds. Fix what coaches miss.</p>', unsafe_allow_html=True)

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
                    <h3 style="font-size: 1.25rem; font-weight: 600; margin-bottom: 12px; color: var(--lane-line);">{title}</h3>
                    <p style="color: rgba(240, 253, 255, 0.7); line-height: 1.6;">{desc}</p>
                </div>
                """, unsafe_allow_html=True)

        # Demo Section
        st.markdown('<h2 class="section-title">See it in action</h2>', unsafe_allow_html=True)
        st.markdown("""
        <div style="background: rgba(15, 40, 71, 0.4); border: 1px solid rgba(6, 182, 212, 0.15); border-radius: 16px; padding: 40px; text-align: center; max-width: 900px; margin: 0 auto;">
            <svg viewBox="0 0 120 120" width="100" height="100" style="margin-bottom: 24px; opacity: 0.8;">
                <circle cx="60" cy="60" r="55" fill="none" stroke="rgba(6, 182, 212, 0.4)" stroke-width="3"/>
                <circle cx="60" cy="60" r="45" fill="rgba(6, 182, 212, 0.15)"/>
                <path d="M 48 38 L 48 82 L 82 60 Z" fill="#06b6d4"/>
            </svg>
            <h3 style="font-size: 1.5rem; margin-bottom: 12px; color: #22d3ee;">Demo Video Coming Soon</h3>
            <p style="font-size: 1.1rem; max-width: 500px; line-height: 1.6; margin: 0 auto;">
                We're finalizing a full walkthrough showing the upload, AI analysis, and instant PDF report generation.
            </p>
            <p style="font-size: 0.95rem; margin-top: 20px; color: rgba(240, 253, 255, 0.6);">
                In the meantime, click "Get Instant Analysis" to try it yourself!
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Video Section
        st.markdown('<h2 class="section-title">Best camera angles</h2>', unsafe_allow_html=True)
        cols = st.columns(4, gap="medium")
        video_cards = [
            ("recommended", """
<svg viewBox="0 0 200 120" class="video-svg">
    <defs>
        <linearGradient id="poolGrad" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="#0c2d4d"/>
            <stop offset="100%" stop-color="#0a1628"/>
        </linearGradient>
        <linearGradient id="glowGrad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#06b6d4" stop-opacity="0.8"/>
            <stop offset="50%" stop-color="#22d3ee"/>
            <stop offset="100%" stop-color="#06b6d4" stop-opacity="0.8"/>
        </linearGradient>
    </defs>
    <rect fill="url(#poolGrad)" width="200" height="120" rx="8"/>
    <path d="M0 20 Q50 15 100 20 T200 20" stroke="#22d3ee" stroke-width="1.5" fill="none" opacity="0.4"/>
    <line x1="0" y1="18" x2="200" y2="18" stroke="#22d3ee" stroke-width="3" stroke-dasharray="12,6" opacity="0.3"/>
    <g transform="translate(30, 45)">
        <ellipse cx="70" cy="12" rx="55" ry="10" fill="url(#glowGrad)" opacity="0.9"/>
        <circle cx="15" cy="8" r="9" fill="#22d3ee"/>
        <line x1="25" y1="6" x2="-5" y2="2" stroke="#22d3ee" stroke-width="6" stroke-linecap="round"/>
        <path d="M60 15 Q75 30 95 20" stroke="#06b6d4" stroke-width="5" stroke-linecap="round" fill="none"/>
        <line x1="120" y1="10" x2="145" y2="5" stroke="#06b6d4" stroke-width="5" stroke-linecap="round"/>
        <line x1="120" y1="14" x2="145" y2="20" stroke="#06b6d4" stroke-width="5" stroke-linecap="round" opacity="0.8"/>
    </g>
    <line x1="45" y1="53" x2="45" y2="30" stroke="#fbbf24" stroke-width="1" stroke-dasharray="4,2" opacity="0.6"/>
    <line x1="45" y1="30" x2="55" y2="30" stroke="#fbbf24" stroke-width="1" opacity="0.6"/>
    <circle cx="50" cy="60" r="2" fill="white" opacity="0.3"/>
    <circle cx="55" cy="55" r="1.5" fill="white" opacity="0.2"/>
    <circle cx="48" cy="65" r="1" fill="white" opacity="0.25"/>
    <text x="100" y="108" fill="rgba(255,255,255,0.8)" font-size="9" text-anchor="middle" font-family="system-ui">Side View • Underwater</text>
</svg>
""", "Side View + Underwater", "Streamline, pull path, elbow position, kick timing"),
        # (other SVGs unchanged...)
        ]
        for i, (class_name, svg, title, metrics) in enumerate(video_cards):
            with cols[i]:
                st.markdown(f'<div class="video-card {class_name}">', unsafe_allow_html=True)
                st.markdown(svg, unsafe_allow_html=True)
                st.markdown(f'<h3 style="font-size: 1rem; font-weight: 600; color: var(--lane-line); margin-bottom: 8px;">{title}</h3>', unsafe_allow_html=True)
                st.markdown(f'<p style="font-size: 0.875rem; color: rgba(240, 253, 255, 0.6); line-height: 1.5;">{metrics}</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<p style="background: rgba(251, 191, 36, 0.1); border: 1px solid rgba(251, 191, 36, 0.3); border-radius: 12px; padding: 16px 20px; font-size: 0.9375rem; color: rgba(240, 253, 255, 0.9); text-align: center; margin-top: 32px;">💡 <strong>Tip:</strong> 10-15 seconds of continuous swimming works best. Our AI auto-detects your camera angle!</p>', unsafe_allow_html=True)

    # How It Works (with gap)
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
                <h3 style="color: var(--lane-line);">{title}</h3>
                <p style="color: rgba(240, 253, 255, 0.7);">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    # Testimonial
    st.markdown('<div class="testimonial-card">', unsafe_allow_html=True)
    st.markdown('<div style="font-size: 1.5rem; color: var(--gold-medal); margin-bottom: 20px;">★★★★★</div>', unsafe_allow_html=True)
    st.markdown('<blockquote style="font-size: 1.125rem; line-height: 1.7; color: rgba(240, 253, 255, 0.9); margin-bottom: 24px; font-style: italic;">"I\'ve been coaching for 18 years and this caught a dropped elbow pattern I missed. My swimmer dropped 0.4 seconds in her next 100 free after 2 weeks of targeted drills."</blockquote>', unsafe_allow_html=True)
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 16px;">
        <div style="width: 56px; height: 56px; border-radius: 50%; background: linear-gradient(135deg, var(--surface-glow), var(--lane-line)); color: var(--deep-pool); font-weight: 700; display: flex; align-items: center; justify-content: center; font-size: 1.125rem;">MK</div>
        <div>
            <h4 style="color: var(--lane-line);">Mike K.</h4>
            <p style="font-size: 0.875rem; color: rgba(240, 253, 255, 0.6);">Head Coach, Aquatic Stars SC</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Final CTA
    st.markdown('<div class="final-cta">', unsafe_allow_html=True)
    st.markdown('<h2>Ready to find your speed leak?</h2>', unsafe_allow_html=True)
    st.markdown('<p>One video. One analysis. One fix that changes everything.</p>', unsafe_allow_html=True)
    if st.button("🏊 Get Instant Analysis → $4.99", key="cta2", use_container_width=True):
        st.markdown(f'<meta http-equiv="refresh" content="0;url={STRIPE_PAYMENT_LINK}">', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div style="padding: 40px 0; border-top: 1px solid rgba(6, 182, 212, 0.1); text-align: center; color: rgba(240, 253, 255, 0.5); font-size: 0.875rem;">
        © 2026 SwimForm AI · <a href="#" style="color: var(--surface-glow); text-decoration: none;">Privacy</a> · <a href="#" style="color: var(--surface-glow); text-decoration: none;">Terms</a> · <a href="mailto:support@swimform.ai" style="color: var(--surface-glow); text-decoration: none;">support@swimform.ai</a>
    </div>
    """, unsafe_allow_html=True)

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

    if success:
        st.session_state.paid = True
        st.success("Payment successful! Loading dashboard...")
        st.balloons()
        st.query_params.clear()
        st.rerun()
    elif demo:
        st.session_state.paid = True
        st.info("Demo mode activated — full access granted for testing!")
        st.query_params.clear()
        st.rerun()
    elif cancel:
        st.warning("Payment cancelled. You can try again.")
        st.query_params.clear()
    else:
        show_landing_page()


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
