import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="SwimForm AI",
    page_icon="🏊",
    layout="centered",  # Centered to prevent expansion
    initial_sidebar_state="collapsed",
)

# Hide Streamlit default chrome
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {padding: 0 !important;}
    .stContainer {max-width: 1100px; margin: 0 auto; padding: 0 24px;}  /* Container max-width like original */
</style>
""", unsafe_allow_html=True)

# CONFIG & SECRETS (unchanged)
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

# Session state for payment
if "paid" not in st.session_state:
    st.session_state.paid = False


def show_landing_page():
    # Global CSS with fixes for text color, spacing, and overrides
    st.markdown("""
    <style>
        :root {
            --deep-pool: #0a1628;
            --mid-water: #0f2847;
            --surface-glow: #06b6d4;
            --lane-line: #22d3ee;
            --bubble-white: #f0fdff;
            --alert-red: #ff4757;
            --success-green: #10b981;
            --gold-medal: #fbbf24;
        }

        .stApp {
            background: var(--deep-pool) !important;
            color: var(--bubble-white) !important;
        }

        .stMarkdown div, p, h1, h2, h3, h4, blockquote {
            color: var(--bubble-white) !important;
        }

        h1, h2, h3 {
            color: var(--bubble-white) !important;
        }

        .water-bg {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            z-index: -10;
            background: linear-gradient(180deg, var(--deep-pool) 0%, var(--mid-water) 30%, #0e3d6b 60%, var(--mid-water) 100%);
        }

        .water-bg::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: 
                radial-gradient(ellipse at 20% 20%, rgba(6, 182, 212, 0.15) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 80%, rgba(6, 182, 212, 0.1) 0%, transparent 50%);
            animation: waterShimmer 8s ease-in-out infinite;
        }

        @keyframes waterShimmer {
            0%, 100% { opacity: 0.5; transform: translateY(0); }
            50% { opacity: 1; transform: translateY(-20px); }
        }

        .lane-lines {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            z-index: -9;
            opacity: 0.03;
            background: repeating-linear-gradient(90deg, var(--lane-line) 0px, var(--lane-line) 4px, transparent 4px, transparent 150px);
        }

        .bubble {
            position: fixed;
            border-radius: 50%;
            background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.4), rgba(6, 182, 212, 0.1));
            animation: float 15s infinite ease-in-out;
            z-index: -8;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0) rotate(0deg); }
            33% { transform: translateY(-30px) rotate(5deg); }
            66% { transform: translateY(20px) rotate(-5deg); }
        }

        .bubble:nth-child(1) { width: 80px; height: 80px; top: 20%; left: 10%; }
        .bubble:nth-child(2) { width: 40px; height: 40px; top: 60%; left: 85%; animation-delay: -5s; }
        .bubble:nth-child(3) { width: 60px; height: 60px; top: 80%; left: 20%; animation-delay: -10s; }
        .bubble:nth-child(4) { width: 30px; height: 30px; top: 40%; left: 70%; animation-delay: -3s; }

        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(6, 182, 212, 0.15);
            border: 1px solid rgba(6, 182, 212, 0.3);
            padding: 8px 16px;
            border-radius: 100px;
            font-size: 0.875rem;
            color: var(--lane-line);
            margin-bottom: 24px;
            animation: fadeInUp 0.6s ease-out;
        }

        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        h1 {
            font-size: clamp(2.5rem, 6vw, 4rem);
            font-weight: 700;
            line-height: 1.1;
            margin-bottom: 20px;
            animation: fadeInUp 0.6s ease-out 0.1s both;
        }

        h1 .highlight {
            background: linear-gradient(135deg, var(--surface-glow), var(--lane-line));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .hero-subtitle {
            font-size: 1.25rem;
            color: rgba(240, 253, 255, 0.7);
            max-width: 600px;
            margin: 0 auto 40px;
            line-height: 1.6;
            animation: fadeInUp 0.6s ease-out 0.2s both;
        }

        .cta-box {
            background: linear-gradient(135deg, rgba(15, 40, 71, 0.8) 0%, rgba(10, 22, 40, 0.9) 100%);
            border: 1px solid rgba(6, 182, 212, 0.2);
            border-radius: 24px;
            padding: 40px;
            max-width: 500px;
            margin: 0 auto 60px;  /* Added margin for spacing */
            position: relative;
            overflow: hidden;
            animation: fadeInUp 0.6s ease-out 0.3s both;
        }

        .price-tag {
            display: flex;
            align-items: baseline;
            justify-content: center;
            gap: 8px;
            margin-bottom: 8px;
            font-size: 3rem;
            font-weight: 700;
            color: var(--surface-glow);
        }

        .price-period {
            font-size: 1.125rem;
            color: rgba(240, 253, 255, 0.6);
        }

        .price-note {
            font-size: 0.875rem;
            color: rgba(240, 253, 255, 0.5);
            margin-bottom: 32px;
            text-align: center;
        }

        .trust-signals {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 24px;
            font-size: 0.875rem;
            color: rgba(240, 253, 255, 0.6);
        }

        .trust-signal::before {
            content: '✓';
            color: var(--success-green);
            font-weight: 700;
        }

        .section-title {
            text-align: center;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 48px;
            margin-top: 60px;  /* Added top margin for section spacing */
        }

        .feature {
            background: rgba(15, 40, 71, 0.4);
            border: 1px solid rgba(6, 182, 212, 0.15);
            border-radius: 16px;
            padding: 32px;
            transition: all 0.3s ease;
            height: 100%;  /* Equal height in columns */
        }

        .feature:hover {
            border-color: rgba(6, 182, 212, 0.4);
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(6, 182, 212, 0.15);
        }

        .feature-icon {
            width: 56px;
            height: 56px;
            border-radius: 12px;
            background: linear-gradient(135deg, rgba(6, 182, 212, 0.2), rgba(34, 211, 238, 0.1));
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.75rem;
            margin-bottom: 20px;
        }

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

        .video-card.recommended {
            border: 2px solid var(--gold-medal);
            background: linear-gradient(135deg, rgba(251, 191, 36, 0.1) 0%, rgba(15, 40, 71, 0.4) 100%);
            position: relative;
        }

        .video-card.recommended::before {
            content: '⭐ RECOMMENDED';
            position: absolute;
            top: -12px;
            left: 50%;
            transform: translateX(-50%);
            background: var(--gold-medal);
            color: var(--deep-pool);
            font-size: 0.75rem;
            font-weight: 700;
            padding: 4px 12px;
            border-radius: 100px;
            letter-spacing: 0.5px;
        }

        .video-svg {
            width: 100%;
            height: 120px;  /* Fixed height to prevent expansion */
            display: block;
            margin-bottom: 16px;
        }

        .step {
            background: rgba(15, 40, 71, 0.4);
            border: 1px solid rgba(6, 182, 212, 0.15);
            border-radius: 16px;
            padding: 32px;
            text-align: center;
            height: 100%;
        }

        .step-number {
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--surface-glow), var(--lane-line));
            color: var(--deep-pool);
            font-size: 1.5rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 16px;
        }

        .testimonial-card {
            background: rgba(15, 40, 71, 0.4);
            border: 1px solid rgba(6, 182, 212, 0.15);
            border-radius: 20px;
            padding: 40px;
            max-width: 700px;
            margin: 60px auto;  /* Centered with spacing */
        }

        .final-cta {
            text-align: center;
            margin: 80px 0;  /* Added spacing */
        }
    </style>
    <div class="water-bg"></div>
    <div class="lane-lines"></div>
    <div class="bubble"></div>
    <div class="bubble"></div>
    <div class="bubble"></div>
    <div class="bubble"></div>
    """, unsafe_allow_html=True)

    container = st.container()  # Wrap content in max-width container

    with container:
        # Header/Logo (unchanged)
        st.markdown("""
        <div style="padding: 20px 0; position: relative; z-index: 10; text-align: left;">
            <a href="#" style="font-family: 'Space Mono', monospace; font-size: 1.5rem; font-weight: 700; color: var(--surface-glow); text-decoration: none; display: inline-flex; align-items: center; gap: 10px;">
                <svg width="32" height="32" viewBox="0 0 32 32">
                    <circle cx="16" cy="16" r="14" fill="none" stroke="currentColor" stroke-width="2"/>
                    <path d="M 8 16 Q 16 12 24 16" stroke="currentColor" stroke-width="2.5" fill="none" stroke-linecap="round"/>
                    <circle cx="12" cy="14" r="1.5" fill="currentColor"/>
                    <circle cx="20" cy="14" r="1.5" fill="currentColor"/>
                </svg>
                SwimForm AI
            </a>
        </div>
        """, unsafe_allow_html=True)

        # Hero Section (with padding)
        st.markdown('<div style="padding: 60px 0 20px; text-align: center;">', unsafe_allow_html=True)
        st.markdown('<div class="hero-badge">⚡ Video analysis powered by Claude AI</div>', unsafe_allow_html=True)
        st.markdown('<h1>Find the <span class="highlight">one fix</span><br/>that makes you faster</h1>', unsafe_allow_html=True)
        st.markdown('<p class="hero-subtitle">Upload your swim video. Get a biomechanics report in 90 seconds. Fix what coaches miss.</p>', unsafe_allow_html=True)

        # CTA Box (unchanged)
        st.markdown("""
        <div class="cta-box">
            <div class="price-tag">
                $4.99 <span class="price-period">per analysis</span>
            </div>
            <p class="price-note">One video • Full PDF report • Annotated playback</p>
        """, unsafe_allow_html=True)

        if st.button("🏊 Get Instant Analysis → $4.99", key="cta1", use_container_width=True):
            st.markdown(f'<meta http-equiv="refresh" content="0;url={STRIPE_PAYMENT_LINK}">', unsafe_allow_html=True)

        if IS_DEV:
            if st.button("Skip Payment – Demo Mode (testing only)", key="demo1", use_container_width=True):
                st.session_state.paid = True
                st.rerun()

        st.markdown("""
            <div class="trust-signals">
                <span class="trust-signal">Secure checkout</span>
                <span class="trust-signal">90-sec turnaround</span>
                <span class="trust-signal">Download forever</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Features Section
        st.markdown('<h2 class="section-title">What you get</h2>', unsafe_allow_html=True)
        cols = st.columns(3, gap="medium")  # Added gap for spacing
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

        # Import the dashboard module (handles numeric prefix in filename)
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
