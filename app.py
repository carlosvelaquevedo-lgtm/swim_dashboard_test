import streamlit as st

# ─────────────────────────────────────────────
# LANDING PAGE
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="Freestyle Swim Analyzer Pro",
    page_icon="🏊",
    layout="wide"
)

# Custom CSS for landing page
LANDING_CSS = """
<style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #0f172a 100%);
    }
    .hero-section {
        text-align: center;
        padding: 60px 20px;
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 24px;
        border: 1px solid rgba(100, 116, 139, 0.3);
        margin: 40px auto;
        max-width: 900px;
    }
    .hero-title {
        font-size: 3.5em;
        font-weight: 800;
        background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
    }
    .hero-subtitle {
        font-size: 1.5em;
        color: #cbd5e1;
        margin-bottom: 40px;
    }
    .feature-card {
        background: rgba(30, 41, 59, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 30px;
        border: 1px solid rgba(100, 116, 139, 0.3);
        margin: 20px;
        text-align: center;
        transition: transform 0.3s ease;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        border-color: #06b6d4;
    }
    .feature-icon {
        font-size: 3em;
        margin-bottom: 15px;
    }
    .feature-title {
        font-size: 1.3em;
        font-weight: 600;
        color: #f8fafc;
        margin-bottom: 10px;
    }
    .feature-description {
        color: #cbd5e1;
        font-size: 1em;
    }
    .cta-button {
        background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 16px 48px;
        font-size: 1.2em;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
        display: inline-block;
    }
    .cta-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(6, 182, 212, 0.4);
    }
    h1, h2, h3 { color: #f8fafc !important; }
    p, span, label { color: #cbd5e1; }
</style>
"""

st.markdown(LANDING_CSS, unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-section">
    <div class="hero-title">🏊 Freestyle Swim Analyzer Pro</div>
    <div class="hero-subtitle">
        AI-powered biomechanical analysis for elite swimming performance
    </div>
</div>
""", unsafe_allow_html=True)

# Features Section
st.markdown("## ✨ What You'll Get")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🎯</div>
        <div class="feature-title">Precise Biomechanics</div>
        <div class="feature-description">
            Advanced MediaPipe AI analyzes body alignment, stroke efficiency, and technique flaws
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Detailed Metrics</div>
        <div class="feature-description">
            Track EVF angle, body roll, kick depth, breathing timing, and more
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📹</div>
        <div class="feature-title">Video Analysis</div>
        <div class="feature-description">
            Upload your swim video and get annotated feedback with visual overlays
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🏅</div>
        <div class="feature-title">Multi-Discipline</div>
        <div class="feature-description">
            Optimized for pool swimming, triathlon, and open water
        </div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📈</div>
        <div class="feature-title">Performance Reports</div>
        <div class="feature-description">
            Export comprehensive PDF reports with charts and recommendations
        </div>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">⚡</div>
        <div class="feature-title">Instant Feedback</div>
        <div class="feature-description">
            Real-time processing with detailed stroke-by-stroke analysis
        </div>
    </div>
    """, unsafe_allow_html=True)

# How It Works
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("## 🚀 How It Works")

st.markdown("""
<div style="background: rgba(30, 41, 59, 0.7); border-radius: 16px; padding: 30px; margin: 20px auto; max-width: 800px;">
    <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <div style="background: #06b6d4; border-radius: 50%; width: 50px; height: 50px; display: flex; align-items: center; justify-content: center; font-size: 1.5em; font-weight: bold; margin-right: 20px;">1</div>
        <div>
            <div style="font-weight: 600; font-size: 1.2em; color: #f8fafc;">Get Access</div>
            <div style="color: #cbd5e1;">Complete a one-time payment to unlock the analyzer</div>
        </div>
    </div>
    <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <div style="background: #3b82f6; border-radius: 50%; width: 50px; height: 50px; display: flex; align-items: center; justify-content: center; font-size: 1.5em; font-weight: bold; margin-right: 20px;">2</div>
        <div>
            <div style="font-weight: 600; font-size: 1.2em; color: #f8fafc;">Upload Your Video</div>
            <div style="color: #cbd5e1;">Upload a freestyle swim video (underwater or above water)</div>
        </div>
    </div>
    <div style="display: flex; align-items: center;">
        <div style="background: #8b5cf6; border-radius: 50%; width: 50px; height: 50px; display: flex; align-items: center; justify-content: center; font-size: 1.5em; font-weight: bold; margin-right: 20px;">3</div>
        <div>
            <div style="font-weight: 600; font-size: 1.2em; color: #f8fafc;">Get Analysis</div>
            <div style="color: #cbd5e1;">Receive detailed metrics, annotated video, and PDF report</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Call to Action
st.markdown("<br><br>", unsafe_allow_html=True)

col_spacer1, col_cta, col_spacer2 = st.columns([1, 2, 1])

with col_cta:
    st.markdown("""
    <div style="text-align: center; background: rgba(30, 41, 59, 0.8); border-radius: 16px; padding: 40px; border: 2px solid #06b6d4;">
        <div style="font-size: 1.8em; font-weight: 700; color: #f8fafc; margin-bottom: 10px;">
            Ready to Improve Your Technique?
        </div>
        <div style="font-size: 1.1em; color: #cbd5e1; margin-bottom: 30px;">
            Get instant access to professional-grade swim analysis
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Button to payment page
    if st.button("🚀 Get Started Now", type="primary", use_container_width=True):
        st.switch_page("pages/1_Payment.py")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; padding: 20px; color: #64748b; border-top: 1px solid rgba(100, 116, 139, 0.3); margin-top: 40px;">
    <p>🏊 Powered by MediaPipe AI • Trusted by swimmers and coaches worldwide</p>
    <p style="font-size: 0.9em;">Full body visibility required for accurate analysis • Supports MP4, MOV, AVI formats</p>
</div>
""", unsafe_allow_html=True)
