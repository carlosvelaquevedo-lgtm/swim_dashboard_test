import streamlit as st

# =============================================
# PAGE CONFIG
# =============================================
st.set_page_config(
    page_title="SwimForm AI | Elite Biomechanics",
    page_icon="🏊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

STRIPE_PAYMENT_LINK = "https://buy.stripe.com/test_8x2eVdaBSe7mf2JaIEao800"
IS_DEV = True

if "paid" not in st.session_state:
    st.session_state.paid = False


# =============================================
# GLOBAL STYLING
# =============================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Space+Mono:wght@600&display=swap');

/* ============================= */
/* GLOBAL */
/* ============================= */
.stApp, .main, .block-container {
    background: linear-gradient(180deg, #0a1628 0%, #0f2847 40%, #0a1628 100%);
    color: #f0fdff;
    font-family: 'Inter', sans-serif;
}

[data-testid="stToolbar"], [data-testid="stHeader"] {
    visibility: hidden;
}

.block-container {
    padding-top: 2rem;
}

/* ============================= */
/* BACKGROUND EFFECTS */
/* ============================= */
.water-bg {
    position: fixed;
    inset: 0;
    z-index: -10;
    background:
        radial-gradient(circle at 20% 20%, rgba(6,182,212,0.12), transparent 50%),
        radial-gradient(circle at 80% 70%, rgba(14,165,233,0.08), transparent 50%);
    animation: floatBg 12s ease-in-out infinite;
}

@keyframes floatBg {
    0%,100% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
}

/* ============================= */
/* CTA BOX */
/* ============================= */
.cta-box {
    background: rgba(15, 40, 71, 0.6);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(34,211,238,0.25);
    border-radius: 28px;
    padding: 50px;
    text-align: center;
    box-shadow: 0 30px 80px rgba(0,0,0,0.6);
}

/* ============================= */
/* FEATURE CARDS */
/* ============================= */
.f-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(34,211,238,0.1);
    border-radius: 22px;
    padding: 30px;
    transition: all 0.4s ease;
    height: 100%;
}

.f-card:hover {
    transform: translateY(-6px);
    border-color: rgba(34,211,238,0.6);
    background: rgba(34,211,238,0.06);
}

/* ============================= */
/* PREMIUM SVG SYSTEM */
/* ============================= */
.angle-card {
    background: linear-gradient(145deg, rgba(10,22,40,0.9), rgba(8,18,32,0.8));
    border: 1px solid rgba(34,211,238,0.15);
    border-radius: 20px;
    padding: 18px;
    backdrop-filter: blur(20px);
    transition: all 0.4s ease;
    box-shadow: 0 10px 40px rgba(0,0,0,0.5);
}

.angle-card:hover {
    transform: translateY(-8px) scale(1.02);
    border-color: rgba(34,211,238,0.6);
}

@keyframes gradientShift {
    0% { stroke-dashoffset: 0; }
    100% { stroke-dashoffset: 1000; }
}

.skeleton-line {
    stroke: url(#aiGradient);
    stroke-width: 3;
    stroke-linecap: round;
    fill: none;
    stroke-dasharray: 8 6;
    animation: gradientShift 30s linear infinite;
}

.ai-node {
    fill: #22d3ee;
    filter: drop-shadow(0 0 6px #22d3ee);
    animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
    0%,100% { r: 3; opacity: 0.7; }
    50% { r: 4.5; opacity: 1; }
}

.swimmer-group {
    animation: floatSwimmer 6s ease-in-out infinite;
}

@keyframes floatSwimmer {
    0%,100% { transform: translateX(0px); }
    50% { transform: translateX(-8px); }
}

footer {
    visibility: hidden;
}
</style>

<div class="water-bg"></div>
""", unsafe_allow_html=True)


# =============================================
# LANDING PAGE
# =============================================
def show_landing_page():

    # Header
    st.markdown("""
    <div style="display:flex;justify-content:space-between;align-items:center;">
        <div style="font-family:'Space Mono';font-size:1.6rem;font-weight:700;color:#22d3ee;">
            SWIMFORM AI
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Hero
    st.markdown("""
    <div style="text-align:center;padding:80px 0;">
        <div style="color:#22d3ee;font-weight:600;letter-spacing:1px;">
            ⚡ Pose-Estimation Powered Analysis
        </div>
        <h1 style="font-size:4rem;font-weight:800;margin:25px 0;">
            Find the <span style="
                background:linear-gradient(90deg,#22d3ee,#06b6d4);
                -webkit-background-clip:text;
                -webkit-text-fill-color:transparent;">
                one fix
            </span><br>
            that makes you faster
        </h1>
        <p style="color:#94a3b8;font-size:1.2rem;max-width:750px;margin:0 auto 60px;">
            Upload your swim video. Get a full biomechanics report in 90 seconds.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # CTA
    col1, col2, col3 = st.columns([1,1.8,1])
    with col2:
        st.markdown("""
        <div class="cta-box">
            <div style="color:#22d3ee;font-weight:700;letter-spacing:1px;">
                INSTANT ANALYSIS
            </div>
            <div style="font-size:3.8rem;font-weight:800;margin:15px 0;">
                $4.99
                <span style="font-size:1rem;color:#64748b;font-weight:400;">
                    / video
                </span>
            </div>
            <div style="color:#94a3b8;">
                Full PDF Report • Drill Cards • Stroke Metrics
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.link_button("🏊 Get My Biomechanics Report →",
                       STRIPE_PAYMENT_LINK,
                       use_container_width=True)

        if IS_DEV:
            if st.button("Developer: Skip to Dashboard", use_container_width=True):
                st.session_state.paid = True
                st.rerun()

    # Camera Angles Section
    st.markdown("""
    <h2 style="text-align:center;font-size:2.5rem;margin:100px 0 50px;">
        Optimized Recording Angle
    </h2>
    """, unsafe_allow_html=True)

    cols = st.columns(3)

    with cols[1]:
        st.markdown("""
        <div class="angle-card">
            <svg viewBox="0 0 260 150" width="100%">

                <defs>
                    <linearGradient id="aiGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stop-color="#22d3ee"/>
                        <stop offset="50%" stop-color="#06b6d4"/>
                        <stop offset="100%" stop-color="#0ea5e9"/>
                    </linearGradient>
                </defs>

                <rect width="260" height="150" rx="16" fill="#07111d"/>

                <line x1="0" y1="110" x2="260" y2="110"
                      stroke="#22d3ee"
                      stroke-width="1"
                      opacity="0.3"/>

                <g class="swimmer-group">

                    <line x1="90" y1="75" x2="140" y2="80"
                          class="skeleton-line"/>

                    <line x1="140" y1="80" x2="175" y2="60"
                          class="skeleton-line"/>

                    <line x1="90" y1="75" x2="60" y2="55"
                          class="skeleton-line"/>

                    <circle cx="75" cy="70" r="8"
                            fill="none"
                            stroke="url(#aiGradient)"
                            stroke-width="3"/>

                    <circle cx="90" cy="75" r="3" class="ai-node"/>
                    <circle cx="140" cy="80" r="3" class="ai-node"/>
                    <circle cx="175" cy="60" r="3" class="ai-node"/>
                    <circle cx="60" cy="55" r="3" class="ai-node"/>

                </g>

                <text x="130" y="140"
                      fill="#22d3ee"
                      font-size="10"
                      text-anchor="middle"
                      font-family="Space Mono"
                      letter-spacing="2">
                      SIDE • UNDERWATER
                </text>

            </svg>
        </div>

        <div style="text-align:center;margin-top:20px;">
            <div style="color:#10b981;font-weight:700;font-size:0.8rem;">
                ★ RECOMMENDED
            </div>
            <div style="font-weight:600;margin:5px 0;">
                Side View
            </div>
            <div style="font-size:0.85rem;color:#64748b;">
                Best for EVF angle, pull depth & propulsion vector.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div style="text-align:center;margin-top:120px;
                padding:40px 0;
                border-top:1px solid rgba(34,211,238,0.1);
                color:#64748b;font-size:0.8rem;">
        © 2026 SwimForm AI · Professional Biomechanics for Every Lane
    </div>
    """, unsafe_allow_html=True)


# =============================================
# ROUTER
# =============================================
if st.session_state.paid:
    st.title("🏊 AI Analysis Dashboard")
    st.success("Analysis Credit Active.")
    st.file_uploader("Upload Video (Max 30s)", type=["mp4","mov"])
    if st.button("Log Out"):
        st.session_state.paid = False
        st.rerun()
else:
    q = st.query_params
    if q.get("success") == "true":
        st.session_state.paid = True
        st.balloons()
        st.rerun()
    show_landing_page()
