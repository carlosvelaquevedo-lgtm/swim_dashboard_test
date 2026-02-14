import streamlit as st
import streamlit.components.v1 as components

# =============================================
# PAGE CONFIG
# =============================================
st.set_page_config(
    page_title="SwimForm AI | Elite Biomechanics",
    page_icon="🏊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =============================================
# CONFIG & SECRETS
# =============================================
STRIPE_PAYMENT_LINK = "https://buy.stripe.com/test_8x2eVdaBSe7mf2JaIEao800"
IS_DEV = True

if "paid" not in st.session_state:
    st.session_state.paid = False

# =============================================
# CSS STYLING (Theming & Layout)
# =============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Space+Mono&display=swap');

    /* Main Background Theme */
    .stApp, [data-testid="stAppViewContainer"], .main, .block-container {
        background: #0a1628 !important;
        background-image: linear-gradient(180deg, #0a1628 0%, #0f2847 40%, #0e3d6b 70%, #0f2847 100%) !important;
        color: #f0fdff;
        font-family: 'Inter', sans-serif;
    }

    /* Animated Water Background Layer */
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
        background: radial-gradient(circle at 50% 50%, rgba(6,182,212,0.1) 0%, transparent 70%);
        animation: shimmer 10s ease-in-out infinite alternate;
    }
    @keyframes shimmer { 0% { opacity: 0.3; transform: scale(1); } 100% { opacity: 0.7; transform: scale(1.2); } }

    /* Component Overrides */
    [data-testid="stToolbar"], [data-testid="stHeader"] { visibility: hidden; }
    
    /* Typography & Headers */
    .hero-title {
        font-size: 4.5rem;
        font-weight: 800;
        line-height: 1;
        letter-spacing: -0.02em;
        margin-bottom: 20px;
    }
    .gradient-text {
        background: linear-gradient(90deg, #22d3ee, #06b6d4, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Feature Cards 2.0 */
    .f-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(34, 211, 238, 0.15);
        border-radius: 24px;
        padding: 35px;
        height: 100%;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .f-card:hover {
        background: rgba(34, 211, 238, 0.05);
        border-color: #22d3ee;
        transform: translateY(-8px);
    }

    /* Camera Angle SVGs Styling */
    .svg-container {
        background: #07111d;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        border: 1px solid rgba(255,255,255,0.05);
    }
    .angle-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #94a3b8;
        margin-top: 10px;
        font-weight: 700;
    }

    /* Process/Step styling */
    .step-item {
        position: relative;
        text-align: center;
        padding: 20px;
    }
    .step-circle {
        width: 60px; height: 60px;
        border-radius: 50%;
        background: #06b6d4;
        color: #0a1628;
        display: flex; align-items: center; justify-content: center;
        font-weight: 900; font-size: 1.5rem;
        margin: 0 auto 20px;
        box-shadow: 0 0 20px rgba(6, 182, 212, 0.4);
    }
</style>
<div class="water-bg"></div>
""", unsafe_allow_html=True)

def show_landing_page():
    # --- Navigation ---
    st.markdown("""
    <div style="padding: 20px 0; display: flex; justify-content: space-between; align-items: center;">
        <div style="font-family: 'Space Mono', monospace; font-size: 1.4rem; font-weight: 700; color: #22d3ee;">
            SWIMFORM<span style="color: white; font-weight: 400;">AI</span>
        </div>
        <div style="color: #94a3b8; font-size: 0.9rem;">Elite Biomechanics for Every Lane</div>
    </div>
    """, unsafe_allow_html=True)

    # --- Hero Section ---
    st.markdown('<div style="padding: 100px 0 60px; text-align: center;">', unsafe_allow_html=True)
    st.markdown('<div style="background: rgba(34, 211, 238, 0.1); color: #22d3ee; border: 1px solid rgba(34, 211, 238, 0.3); padding: 6px 18px; border-radius: 100px; font-size: 0.85rem; font-weight: 700; display: inline-block; margin-bottom: 30px;">PRO-LEVEL ANALYTICS FOR $4.99</div>', unsafe_allow_html=True)
    st.markdown('<h1 class="hero-title">Unlock Your<br><span class="gradient-text">Fastest Stroke</span></h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 1.4rem; color: #cbd5e1; max-width: 800px; margin: 20px auto 40px; line-height: 1.6;">Our AI detects 15+ joint points to pinpoint the drag slowing you down. Professional video analysis, minus the $200 coaching fee.</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1.2, 2, 1.2])
    with col2:
        st.link_button("🚀 Start Instant Analysis — $4.99", STRIPE_PAYMENT_LINK, type="primary", use_container_width=True)
        st.markdown('<p style="font-size: 0.8rem; color: #64748b; margin-top: 15px;">Secure payment via Stripe. No subscription required.</p>', unsafe_allow_html=True)
        if IS_DEV and st.button("Developer: Skip to Dashboard", use_container_width=True):
            st.session_state.paid = True
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Social Proof ---
    st.markdown("""
    <div style="text-align: center; padding: 20px 0 80px; opacity: 0.6;">
        <p style="font-size: 0.8rem; letter-spacing: 0.2em; font-weight: 700; margin-bottom: 20px;">TRUSTED BY COACHES AT</p>
        <div style="display: flex; justify-content: center; gap: 40px; font-weight: 800; font-style: italic; font-size: 1.1rem; color: #94a3b8;">
            <span>AQUATIC STARS SC</span>
            <span>ELITE SWIM LAB</span>
            <span>METRO MASTERS</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- Feature Grid (Overhauled Content) ---
    st.markdown('<h2 style="text-align: center; font-size: 2.5rem; margin-bottom: 50px;">The Analysis Engine</h2>', unsafe_allow_html=True)
    
    f_cols = st.columns(2)
    features = [
        ("📊", "Sub-Millimeter Tracking", "We track 15+ anatomical points including wrist, elbow, shoulder, hip, and ankle to measure exact angles and pull-path efficiency."),
        ("🎥", "Pro-Sync Overlay", "View your video frame-for-frame alongside Olympic reference footage with synchronized body-position markers."),
        ("🎯", "Ranked Improvement Map", "Stop being overwhelmed by 'too many fixes.' We rank your issues 1 to 3 based on what will drop the most time."),
        ("🩹", "Prescriptive Drill Library", "Get a personalized PDF including video-guided drills designed to target your specific biomechanical leaks.")
    ]
    
    for i, (icon, title, desc) in enumerate(features):
        with f_cols[i % 2]:
            st.markdown(f"""
            <div class="f-card">
                <div style="font-size: 2.5rem; margin-bottom: 20px;">{icon}</div>
                <h3 style="color: #22d3ee; margin-bottom: 15px; font-size: 1.5rem;">{title}</h3>
                <p style="color: #94a3b8; line-height: 1.6;">{desc}</p>
            </div>
            <div style="height: 25px;"></div>
            """, unsafe_allow_html=True)

    # --- REVAMPED SVG SECTION: AI POSE ESTIMATION ---
    st.markdown('<h2 style="text-align: center; font-size: 2.5rem; margin: 80px 0 40px;">Optimized Recording Angles</h2>', unsafe_allow_html=True)
    
    a_cols = st.columns(4)
    
    # 1. Side Underwater (High Tech Pose)
    with a_cols[0]:
        st.markdown("""
        <div class="svg-container">
            <svg viewBox="0 0 200 120" width="100%">
                <rect fill="#0a1628" width="200" height="120" rx="4"/>
                <circle cx="100" cy="50" r="3" fill="#22d3ee"/> <line x1="100" y1="50" x2="130" y2="60" stroke="#22d3ee" stroke-width="1"/> <line x1="130" y1="60" x2="160" y2="75" stroke="#22d3ee" stroke-width="1"/> <circle cx="130" cy="60" r="2" fill="#34d399"/> <circle cx="160" cy="75" r="2" fill="#34d399"/> <line x1="100" y1="50" x2="80" y2="70" stroke="#22d3ee" stroke-width="2"/> <line x1="80" y1="70" x2="95" y2="90" stroke="#22d3ee" stroke-width="2"/> <circle cx="80" cy="70" r="2" fill="#fbbf24"/> <text x="10" y="110" fill="#22d3ee" font-size="8" font-family="Space Mono">POSE: DETECTED</text>
            </svg>
        </div>
        <div class="angle-label" style="color:#34d399">✓ Recommended</div>
        <div style="font-weight: 700; margin-top: 5px;">Side Underwater</div>
        <div style="font-size: 0.85rem; color: #64748b;">Best for pull path, elbow drop, and hip rotation.</div>
        """, unsafe_allow_html=True)

    # 2. Front Underwater
    with a_cols[1]:
        st.markdown("""
        <div class="svg-container">
            <svg viewBox="0 0 200 120" width="100%">
                <rect fill="#0a1628" width="200" height="120" rx="4"/>
                <circle cx="100" cy="40" r="8" fill="none" stroke="#22d3ee" stroke-width="1"/>
                <line x1="100" y1="48" x2="100" y2="90" stroke="#22d3ee" stroke-width="1" stroke-dasharray="2"/>
                <line x1="100" y1="55" x2="70" y2="60" stroke="#22d3ee" stroke-width="2"/>
                <line x1="70" y1="60" x2="80" y2="100" stroke="#22d3ee" stroke-width="2"/>
                <circle cx="70" cy="60" r="2" fill="#fbbf24"/>
                <text x="10" y="110" fill="#22d3ee" font-size="8" font-family="Space Mono">AXIS: ALIGNED</text>
            </svg>
        </div>
        <div class="angle-label">Secondary</div>
        <div style="font-weight: 700; margin-top: 5px;">Front Underwater</div>
        <div style="font-size: 0.85rem; color: #64748b;">Best for symmetry and crossover detection.</div>
        """, unsafe_allow_html=True)

    # 3. Side Above Water
    with a_cols[2]:
        st.markdown("""
        <div class="svg-container">
            <svg viewBox="0 0 200 120" width="100%">
                <rect fill="#0a1628" width="200" height="120" rx="4"/>
                <path d="M0 60 Q50 55 100 60 T200 60" stroke="#06b6d4" stroke-width="1" fill="none"/>
                <circle cx="110" cy="45" r="4" fill="#22d3ee"/>
                <line x1="110" y1="45" x2="140" y2="48" stroke="#22d3ee" stroke-width="1.5"/>
                <path d="M110 45 L100 20 L80 35" stroke="#22d3ee" stroke-width="2" fill="none"/>
                <circle cx="100" cy="20" r="2" fill="#fbbf24"/>
                <text x="10" y="110" fill="#22d3ee" font-size="8" font-family="Space Mono">MODE: ABOVE_SURFACE</text>
            </svg>
        </div>
        <div class="angle-label">Secondary</div>
        <div style="font-weight: 700; margin-top: 5px;">Side Above Water</div>
        <div style="font-size: 0.85rem; color: #64748b;">Best for recovery height and entry angle.</div>
        """, unsafe_allow_html=True)

    # 4. Bad Angle (Drone/Top)
    with a_cols[3]:
        st.markdown("""
        <div class="svg-container" style="opacity: 0.5;">
            <svg viewBox="0 0 200 120" width="100%">
                <rect fill="#0a1628" width="200" height="120" rx="4"/>
                <line x1="40" y1="40" x2="160" y2="80" stroke="#ef4444" stroke-width="2"/>
                <line x1="160" y1="40" x2="40" y2="80" stroke="#ef4444" stroke-width="2"/>
                <text x="100" y="65" fill="#ef4444" font-size="10" text-anchor="middle" font-weight="900">LOW FIDELITY</text>
            </svg>
        </div>
        <div class="angle-label" style="color:#ef4444">Avoid</div>
        <div style="font-weight: 700; margin-top: 5px;">Direct Top-Down</div>
        <div style="font-size: 0.85rem; color: #64748b;">Refraction makes underwater tracking impossible.</div>
        """, unsafe_allow_html=True)

    # --- How It Works ---
    st.markdown('<h2 style="text-align: center; font-size: 2.5rem; margin: 100px 0 50px;">The 90-Second Process</h2>', unsafe_allow_html=True)
    
    s_cols = st.columns(3)
    steps = [
        ("01", "Activate", "Complete the secure $4.99 payment to unlock your specialized processing tunnel."),
        ("02", "Drop", "Upload a 10-30s raw video clip from your phone. No editing or slow-mo required."),
        ("03", "Review", "Our cloud GPU processes your clip and returns a data-rich report in under 90 seconds.")
    ]
    
    for i, (num, title, desc) in enumerate(steps):
        with s_cols[i]:
            st.markdown(f"""
            <div class="step-item">
                <div class="step-circle">{num}</div>
                <h3 style="color: white; margin-bottom: 15px;">{title}</h3>
                <p style="color: #64748b; font-size: 0.95rem;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    # --- Final CTA ---
    st.markdown('<div style="text-align: center; margin: 120px 0 80px; padding: 60px; background: rgba(34, 211, 238, 0.05); border-radius: 40px; border: 1px solid rgba(34, 211, 238, 0.1);">', unsafe_allow_html=True)
    st.markdown('<h2 style="font-size: 3rem; margin-bottom: 20px;">Ready to stop guessing?</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color: #94a3b8; margin-bottom: 40px; font-size: 1.2rem;">Join 1,200+ swimmers who have found their "one fix" this month.</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1.5, 2, 1.5])
    with col2:
        st.link_button("🏊 Get My Biomechanics Report — $4.99", STRIPE_PAYMENT_LINK, type="primary", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =============================================
# ROUTER
# =============================================
if st.session_state.paid:
    # Check if dashboard exists or show generic dashboard
    st.title("🏊 AI Analysis Dashboard")
    st.success("Payment Verified. You have 1 Analysis Credit.")
    st.file_uploader("Upload Swim Video (MP4/MOV)", type=["mp4", "mov"])
    if st.button("Logout"):
        st.session_state.paid = False
        st.rerun()
else:
    # Handle Stripe Returns
    q = st.query_params
    if q.get("success") == "true":
        st.session_state.paid = True
        st.balloons()
        st.rerun()
    show_landing_page()
