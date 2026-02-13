import streamlit as st

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="SwimFix AI",
    page_icon="🏊",
    layout="wide"
)

STRIPE_PAYMENT_LINK = "https://buy.stripe.com/test_8x2eVdaBSe7mf2JaIEao800"
IS_DEV = True  # set False in production

# =========================================================
# SESSION INIT
# =========================================================

if "paid" not in st.session_state:
    st.session_state.paid = False

# =========================================================
# STRIPE SUCCESS HANDLER
# =========================================================

params = st.query_params

if "success" in params:
    st.session_state.paid = True
    st.query_params.clear()

if IS_DEV and "demo" in params:
    st.session_state.paid = True
    st.query_params.clear()

# =========================================================
# ROUTER
# =========================================================

if st.session_state.paid:
    st.switch_page("pages/2_Ddashboard.py")

# =========================================================
# LANDING PAGE
# =========================================================

# ---------- Clean Styling ----------
st.markdown("""
<style>
.big-title {
    font-size: 52px;
    font-weight: 800;
    line-height: 1.1;
}

.subtitle {
    font-size: 22px;
    color: #666;
}

.feature-card {
    padding: 30px;
    border-radius: 20px;
    background: #f8fafc;
    border: 1px solid #e5e7eb;
    text-align: center;
}

.icon {
    font-size: 40px;
}
</style>
""", unsafe_allow_html=True)

# ---------- HERO ----------
st.markdown('<div class="big-title">AI Swim Technique Analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload a video. Get pro-level feedback in 60 seconds.</div>', unsafe_allow_html=True)

st.markdown("")

col1, col2 = st.columns(2)

with col1:
    if st.button("🏊 Get Instant Analysis – $4.99", use_container_width=True):
        st.markdown(
            f'<meta http-equiv="refresh" content="0;url={STRIPE_PAYMENT_LINK}?success=true">',
            unsafe_allow_html=True
        )

with col2:
    if IS_DEV:
        if st.button("Demo Mode (Skip Payment)", use_container_width=True):
            st.session_state.paid = True
            st.rerun()

st.markdown("---")

# ---------- FEATURES ----------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="icon">📐</div>
        <h3>Angle Detection</h3>
        <p>Shoulder, elbow & hip tracking with biomechanical scoring.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="icon">⚡</div>
        <h3>Catch Analysis</h3>
        <p>High-elbow catch detection using EVF modeling.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="icon">📊</div>
        <h3>Performance Score</h3>
        <p>Instant 0–100 technique grade with correction tips.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("### Who Is This For?")
st.markdown("""
• Competitive swimmers  
• Triathletes  
• Swim coaches  
• Parents reviewing race footage  
""")
