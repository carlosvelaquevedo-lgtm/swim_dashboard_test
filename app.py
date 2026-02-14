import streamlit as st

# =============================================
# PAGE CONFIG
# =============================================
st.set_page_config(
    page_title="SwimForm AI",
    page_icon="🏊",
    layout="centered",
    initial_sidebar_state="expanded"  # Forces sidebar open on load
)

# =============================================
# CSS STYLING (Theming & Layout)
# =============================================
st.markdown("""
<style>
    /* Main Background Theme */
    .stApp, [data-testid="stAppViewContainer"], .main, .block-container {
        background: #0a1628 !important;
        background-image: linear-gradient(180deg, #0a1628 0%, #0f2847 30%, #0e3d6b 60%, #0f2847 100%) !important;
    }

    /* Animated Water Effect */
    .water-bg {
        position: fixed; inset: 0; z-index: -999;
        background: linear-gradient(180deg, #0a1628 0%, #0f2847 30%, #0e3d6b 60%, #0f2847 100%);
    }
    .water-bg::before {
        content: ''; position: absolute; inset: 0;
        background: radial-gradient(ellipse at 20% 20%, rgba(6,182,212,0.15) 0%, transparent 50%);
        animation: waterShimmer 8s ease-in-out infinite;
    }
    @keyframes waterShimmer { 0%, 100% { opacity: 0.5; } 50% { opacity: 1; } }

    /* Component Styling */
    .section-title { text-align: center; font-size: 2.2rem; margin: 60px 0 30px; color: #f0fdff; }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(6, 182, 212, 0.1);
        border-radius: 20px;
        padding: 25px;
        height: 100%;
        transition: 0.3s;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        background: rgba(6, 182, 212, 0.08);
        border-color: #06b6d4;
    }

    .step-box { text-align: center; padding: 20px; }
    .step-num {
        width: 40px; height: 40px; background: #06b6d4; color: #0a1628;
        border-radius: 50%; display: flex; align-items: center; 
        justify-content: center; font-weight: 800; margin: 0 auto 15px;
    }

    /* Keep Sidebar visible but styled */
    [data-testid="stSidebar"] {
        background-color: #07111d !important;
        border-right: 1px solid rgba(6, 182, 212, 0.2);
    }
    
    /* Hide top toolbar only (keeps sidebar toggle visible) */
    header[data-testid="stHeader"] { background: transparent !important; }
    [data-testid="stToolbar"] { visibility: hidden !important; }
</style>
<div class="water-bg"></div>
""", unsafe_allow_html=True)

# =============================================
# SIDEBAR CONTENT
# =============================================
with st.sidebar:
    st.image("https://img.icons8.com", width=80)
    st.title("SwimForm AI")
    st.markdown("---")
    st.info("💡 **Tip:** Underwater side-view videos provide the most accurate biomechanical data.")
    st.markdown("### Settings")
    st.toggle("High-Contrast Mode")
    st.selectbox("Metric System", ["Meters/Seconds", "Yards/Seconds"])

# =============================================
# APP LOGIC
# =============================================
STRIPE_PAYMENT_LINK = "https://buy.stripe.com/test_8x2eVdaBSe7mf2JaIEao800"
IS_DEV = True

if "paid" not in st.session_state:
    st.session_state.paid = False

def show_landing_page():
    # Hero Section
    st.markdown('<div style="padding: 40px 0; text-align: center;">', unsafe_allow_html=True)
    st.markdown('<div style="background: rgba(6,182,212,0.15); border: 1px solid #06b6d4; border-radius: 50px; padding: 8px 20px; display: inline-block; margin-bottom: 20px; color: #22d3ee; font-weight: 600;">⚡ AI Video Analysis</div>', unsafe_allow_html=True)
    st.markdown('<h1 style="font-size: 3.5rem; line-height: 1.1; color: white;">Find the <span style="color: #06b6d4;">One Fix</span><br>That Makes You Faster</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 1.2rem; color: #a5b4fc; margin: 20px 0;">Upload your swim video. Get a biomechanics report in 90 seconds.</p>', unsafe_allow_html=True)
    
    # CTA Buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.link_button("🏊 Get Instant Analysis — $4.99", STRIPE_PAYMENT_LINK, use_container_width=True, type="primary")
        if IS_DEV:
            if st.button("Developer: Skip Payment", use_container_width=True):
                st.session_state.paid = True
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Features Grid
    st.markdown('<h2 class="section-title">Analysis Features</h2>', unsafe_allow_html=True)
    f_cols = st.columns(3)
    features = [
        ("📊", "7 Biometrics", "Stroke rate, DPS, and entry angles measured frame-by-frame."),
        ("🎯", "Ranked Fixes", "We rank issues 1-3 so you know what to prioritize first."),
        ("🎥", "Pro Comparison", "Your stroke vs. Olympic reference footage side-by-side.")
    ]
    for i, (icon, title, desc) in enumerate(features):
        with f_cols[i]:
            st.markdown(f"""
            <div class="feature-card">
                <div style="font-size: 2rem; margin-bottom: 10px;">{icon}</div>
                <h3 style="color: #22d3ee; margin-bottom: 10px;">{title}</h3>
                <p style="color: rgba(240, 253, 255, 0.7); font-size: 0.95rem;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

def show_dashboard():
    st.title("🏊 Analysis Dashboard")
    st.write("Ready to analyze. Drag your video file here.")
    st.file_uploader("Upload MP4/MOV clip (Max 30s)", type=['mp4', 'mov'])
    if st.button("Log Out"):
        st.session_state.paid = False
        st.rerun()

# Router
if st.session_state.paid:
    show_dashboard()
else:
    show_landing_page()
