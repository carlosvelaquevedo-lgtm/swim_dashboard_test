import streamlit as st
import streamlit.components.v1 as components

# =============================================
# PAGE CONFIG
# =============================================
st.set_page_config(
    page_title="SwimForm AI",
    page_icon="🏊",
    layout="centered",                      # wide is better for full background
    initial_sidebar_state="expanded"    # sidebar open by default
)

# =============================================
# CONFIG & SECRETS
# =============================================
try:
    import stripe
    # Attempt to load secrets if available, otherwise handle gracefully
    if "stripe" in st.secrets:
        stripe.api_key = st.secrets["stripe"]["secret_key"]
        APP_BASE_URL = st.secrets["stripe"].get("base_url", "http://localhost:8501")
    else:
        APP_BASE_URL = "http://localhost:8501"
except Exception:
    APP_BASE_URL = "http://localhost:8501"

# Hardcoded link for the button (Test Mode Link)
STRIPE_PAYMENT_LINK = "https://buy.stripe.com/test_8x2eVdaBSe7mf2JaIEao800"
IS_DEV = True

if "paid" not in st.session_state:
    st.session_state.paid = False

# =============================================
# BACKGROUND + MENU HIDE
# =============================================
st.markdown("""
<style>
    /* Full background */
    .stApp, [data-testid="stAppViewContainer"], .main, .block-container {
        background: #0a1628 !important;
        background-image: linear-gradient(180deg, #0a1628 0%, #0f2847 30%, #0e3d6b 60%, #0f2847 100%) !important;
        color: #f0fdff;
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

    /* Video Cards for Angles */
    .video-card {
        background: rgba(15, 40, 71, 0.4);
        border: 1px solid rgba(6, 182, 212, 0.15);
        border-radius: 16px;
        padding: 20px;
        transition: all 0.3s ease;
        height: 100%;
    }
    .video-card:hover {
        border-color: rgba(6, 182, 212, 0.4);
        transform: translateY(-4px);
    }
    .video-svg {
        width: 100%;
        height: 120px;
        display: block;
        margin-bottom: 16px;
    }
    
    /* Steps */
    .step-box {
        background: rgba(15, 40, 71, 0.4);
        border: 1px solid rgba(6, 182, 212, 0.15);
        border-radius: 16px;
        padding: 32px;
        text-align: center;
        height: 100%;
    }
    .step-num {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        background: linear-gradient(135deg, #06b6d4, #22d3ee);
        color: #0a1628;
        font-size: 1.5rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 16px;
    }

</style>

<div class="water-bg"></div>
<div class="lane-lines"></div>
""", unsafe_allow_html=True)


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

    # Features Grid (Expanded to include all 6 from App 2)
    st.markdown('<h2 class="section-title">What You Get</h2>', unsafe_allow_html=True)
    
    features = [
        ("📊", "7 Biomechanical Metrics", "Stroke rate, DPS, entry angle, elbow drop, kick depth, head position & body rotation measured frame-by-frame."),
        ("🎯", "Ranked Issues (1-3)", "We rank your 1–3 biggest issues so you know exactly what to fix first to move the needle."),
        ("🎥", "Pro Comparison", "Side-by-side view: your stroke vs. Olympic-level reference footage with overlays."),
        ("🏊", "Drill Prescription", "Exact drills with rep counts, focus cues, and when to return to full stroke. No guessing."),
        ("📈", "Progress Tracking", "Upload follow-up videos. We'll chart your improvement across all metrics session by session."),
        ("⚡", "Instant PDF Download", "Complete report with screenshots, data tables, and drill cards. Keep for your records.")
    ]
    
    # Render in 2 rows of 3
    row1_cols = st.columns(3)
    for i in range(3):
        icon, title, desc = features[i]
        with row1_cols[i]:
            st.markdown(f"""
            <div class="feature-card">
                <div style="font-size: 2.8rem; margin-bottom: 16px;">{icon}</div>
                <h3 style="color: #22d3ee; margin-bottom: 12px;">{title}</h3>
                <p style="color: rgba(240,253,255,0.8);">{desc}</p>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True) # Spacer
    
    row2_cols = st.columns(3)
    for i in range(3):
        icon, title, desc = features[i+3]
        with row2_cols[i]:
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

    # Best Camera Angles (Populated with SVGs from App 2)
    st.markdown('<h2 class="section-title">Best Camera Angles</h2>', unsafe_allow_html=True)
    
    angle_cols = st.columns(4)
    video_cards = [
        ("recommended", """
<svg viewBox="0 0 200 120" class="video-svg">
    <defs>
        <linearGradient id="poolGrad1" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="#0c2d4d"/>
            <stop offset="100%" stop-color="#0a1628"/>
        </linearGradient>
        <linearGradient id="glowGrad1" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#06b6d4" stop-opacity="0.8"/>
            <stop offset="50%" stop-color="#22d3ee"/>
            <stop offset="100%" stop-color="#06b6d4" stop-opacity="0.8"/>
        </linearGradient>
    </defs>
    <rect fill="url(#poolGrad1)" width="200" height="120" rx="8"/>
    <path d="M0 20 Q50 15 100 20 T200 20" stroke="#22d3ee" stroke-width="1.5" fill="none" opacity="0.4"/>
    <line x1="0" y1="18" x2="200" y2="18" stroke="#22d3ee" stroke-width="3" stroke-dasharray="12,6" opacity="0.3"/>
    <g transform="translate(30, 45)">
        <ellipse cx="70" cy="12" rx="55" ry="10" fill="url(#glowGrad1)" opacity="0.9"/>
        <circle cx="15" cy="8" r="9" fill="#22d3ee"/>
        <line x1="25" y1="6" x2="-5" y2="2" stroke="#22d3ee" stroke-width="6" stroke-linecap="round"/>
        <path d="M60 15 Q75 30 95 20" stroke="#06b6d4" stroke-width="5" stroke-linecap="round" fill="none"/>
        <line x1="120" y1="10" x2="145" y2="5" stroke="#06b6d4" stroke-width="5" stroke-linecap="round"/>
    </g>
    <text x="100" y="108" fill="rgba(255,255,255,0.8)" font-size="9" text-anchor="middle" font-family="system-ui">Side View • Underwater</text>
</svg>
""", "Side View + Underwater", "Streamline, pull path, elbow position, kick timing"),

        ("", """
<svg viewBox="0 0 200 120" class="video-svg">
    <rect fill="#0a1628" width="200" height="120" rx="8"/>
    <path d="M0 60 Q50 55 100 60 T200 60" stroke="#22d3ee" stroke-width="1.5" fill="none" opacity="0.4"/>
    <g transform="translate(60, 40)">
        <circle cx="40" cy="15" r="8" fill="#22d3ee"/>
        <path d="M40 25 L40 60 L20 75 M40 60 L60 75" stroke="#06b6d4" stroke-width="4" fill="none"/>
        <line x1="20" y1="35" x2="60" y2="35" stroke="#06b6d4" stroke-width="4"/>
    </g>
    <text x="100" y="108" fill="rgba(255,255,255,0.8)" font-size="9" text-anchor="middle" font-family="system-ui">Front View • Underwater</text>
</svg>
""", "Front View + Underwater", "Symmetry, crossover, catch width"),

        ("", """
<svg viewBox="0 0 200 120" class="video-svg">
    <rect fill="#0a1628" width="200" height="120" rx="8"/>
    <path d="M0 80 Q50 75 100 80 T200 80" stroke="#22d3ee" stroke-width="1.5" fill="none" opacity="0.4"/>
    <g transform="translate(40, 30)">
        <ellipse cx="60" cy="15" rx="50" ry="10" fill="#06b6d4" opacity="0.5"/>
        <circle cx="20" cy="10" r="8" fill="#22d3ee"/>
        <line x1="28" y1="10" x2="90" y2="10" stroke="#22d3ee" stroke-width="4"/>
    </g>
    <text x="100" y="108" fill="rgba(255,255,255,0.8)" font-size="9" text-anchor="middle" font-family="system-ui">Side View • Above Water</text>
</svg>
""", "Side View + Above", "Recovery, entry, head position, timing"),

        ("", """
<svg viewBox="0 0 200 120" class="video-svg">
    <rect fill="#0a1628" width="200" height="120" rx="8"/>
    <text x="100" y="60" fill="#22d3ee" font-size="24" text-anchor="middle">❌</text>
    <text x="100" y="108" fill="rgba(255,255,255,0.8)" font-size="9" text-anchor="middle" font-family="system-ui">Top Down / Drone</text>
</svg>
""", "Top Down / Drone", "Less ideal for underwater mechanics analysis.")
    ]

    for i, (class_name, svg, title, metrics) in enumerate(video_cards):
        with angle_cols[i]:
            # Apply highlighting if recommended
            border_style = "border: 2px solid #fbbf24;" if class_name == "recommended" else ""
            bg_style = "background: linear-gradient(135deg, rgba(251,191,36,0.1) 0%, rgba(15,40,71,0.4) 100%);" if class_name == "recommended" else ""
            
            st.markdown(f"""
            <div class="video-card" style="{border_style} {bg_style}">
                {svg}
                <h3 style="font-size: 1rem; font-weight: 600; color: #22d3ee; margin-bottom: 8px;">{title}</h3>
                <p style="font-size: 0.875rem; color: rgba(240, 253, 255, 0.6); line-height: 1.5;">{metrics}</p>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown('<p style="background: rgba(251, 191, 36, 0.1); border: 1px solid rgba(251, 191, 36, 0.3); border-radius: 12px; padding: 16px 20px; font-size: 0.9375rem; color: rgba(240, 253, 255, 0.9); text-align: center; margin-top: 32px;">💡 <strong>Tip:</strong> 10-15 seconds of continuous swimming works best. Our AI auto-detects your camera angle!</p>', unsafe_allow_html=True)


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
# Check query params for Stripe success/cancel
query_params = st.query_params

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
    # Check if returning from Stripe
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
        show_landing_page()
    else:
        show_landing_page()
