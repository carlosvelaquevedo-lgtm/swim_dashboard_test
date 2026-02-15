import streamlit as st
import streamlit.components.v1 as components
import base64
import os

# =============================================
# PAGE CONFIG
# =============================================
st.set_page_config(
    page_title="SwimForm AI | Elite Biomechanics",
    page_icon="🏊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =============================================
# GLOBAL CSS (Background & Theme Fixes)
# =============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Space+Mono:wght@400;700&display=swap');

    /* --- THEME ROOT --- */
    /* Force background on the entire app container */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background: #0a1628 !important;
        background: linear-gradient(180deg, #0a1628 0%, #0f2847 30%, #0e3d6b 60%, #0f2847 100%) !important;
        color: #f0fdff !important;
    }

    /* Floating Decorations */
    .water-bg {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 0;
        pointer-events: none; opacity: 0.3;
    }
    .bubble {
        position: fixed; border-radius: 50%; z-index: 0; pointer-events: none;
        background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.2), rgba(6, 182, 212, 0.05));
        animation: float 15s infinite ease-in-out;
    }
    .b1 { width: 80px; height: 80px; top: 20%; left: 10%; }
    .b2 { width: 40px; height: 40px; top: 60%; left: 85%; animation-delay: -5s; }
    @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-40px); } }

    /* CTA Box Styling */
    .cta-box {
        background: rgba(15, 40, 71, 0.6);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(6, 182, 212, 0.2);
        border-radius: 24px; padding: 40px; text-align: center;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        margin-bottom: 20px;
    }
</style>
<div class="water-bg"></div>
<div class="bubble b1"></div>
<div class="bubble b2"></div>
""", unsafe_allow_html=True)

# =============================================
# CONFIG & SECRETS
# =============================================
STRIPE_PAYMENT_LINK = "https://buy.stripe.com/test_8x2eVdaBSe7mf2JaIEao800"
IS_DEV = True

if "paid" not in st.session_state:
    st.session_state.paid = False

def get_video_base64(video_path):
    if not os.path.exists(video_path):
        return None
    with open(video_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# =============================================
# LANDING PAGE RENDERING
# =============================================
def show_landing_page():
    # 1. Header Section
    st.markdown("""
    <div style="padding: 20px 0; text-align: center; position: relative; z-index: 1;">
        <div style="font-family: 'Space Mono', monospace; font-size: 3rem; font-weight: 700; color: #22d3ee; letter-spacing: -1px;">
            SWIMFORM AI
        </div>
        <p style="color: #94a3b8; font-size: 1.2rem; margin-top: -10px;">Elite Biomechanics. Zero Hardware. 90 Seconds.</p>
    </div>
    """, unsafe_allow_html=True)

    # 2. How It Works (FIXED: One Block)
    st.markdown("""
    <style>
    .process-section { padding: 40px 0; text-align: center; position: relative; z-index: 1; }
    .process-grid { display: flex; justify-content: center; align-items: stretch; gap: 15px; flex-wrap: wrap; margin-top: 30px; }
    .process-card { 
        background: rgba(20,50,90,0.9); border-radius: 24px; padding: 25px 15px; 
        width: 190px; border: 1px solid rgba(34,211,238,0.15); text-align: center; 
        display: flex; flex-direction: column; align-items: center;
    }
    .process-number { width: 35px; height: 35px; margin-bottom: 15px; border-radius: 50%; background: #22d3ee; color: #0a1628; font-weight: 800; display: flex; align-items: center; justify-content: center; }
    .process-card h3 { color: #22d3ee !important; font-size: 1.1rem; margin-bottom: 8px; }
    .process-card p { color: #94a3b8 !important; font-size: 0.85rem; line-height: 1.4; margin: 0; }
    .process-arrow { font-size: 1.5rem; color: #22d3ee; opacity: 0.4; align-self: center; }
    .angle-list { text-align: left; font-size: 0.75rem; color: #cbd5e1; margin-top: 10px; width: 100%; }
    .highlight { color: #10b981; font-weight: 700; }
    </style>
    
    <div class="process-section">
        <h2 style="font-size: 2.5rem; color: white;">How it works</h2>
        <div class="process-grid">
            <div class="process-card">
                <div class="process-number">1</div>
                <h3>Pay $4.99</h3>
                <p>Secure checkout via Stripe. Instant access.</p>
            </div>
            <div class="process-arrow">→</div>
            <div class="process-card">
                <div class="process-number">2</div>
                <h3>Upload Video</h3>
                <p>10–15s clip. Ensure good lighting.</p>
            </div>
            <div class="process-arrow">→</div>
            <div class="process-card">
                <div class="process-number">3</div>
                <h3>Select View</h3>
                <div class="angle-list">
                    <span>• Side | Under <span class="highlight">(Best)</span></span>
                    <span>• Side | Above</span>
                    <span>• Front | Under</span>
                    <span>• Front | Above</span>
                </div>
            </div>
            <div class="process-arrow">→</div>
            <div class="process-card">
                <div class="process-number">4</div>
                <h3>Get Report</h3>
                <p>AI analysis in 90s. Download PDF + video.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 3. Video HUD (FIXED: 25% Larger - 750px width)
    video_b64 = get_video_base64("hero_demo.mp4")
    if not video_b64:
        st.info("ℹ️ Video 'hero_demo.mp4' not found. Please place it in the root directory.")
    else:
        html_code = f"""
        <div style="display: flex; justify-content: center; margin: 50px 0; font-family: 'Space Mono', monospace;">
            <div style="position: relative; width: 750px; border-radius: 24px; overflow: hidden; border: 1px solid rgba(34, 211, 238, 0.4); box-shadow: 0 30px 60px rgba(0,0,0,0.6);">
                <video autoplay muted loop playsinline style="width: 100%; display: block;">
                    <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
                </video>
                
                <div style="position: absolute; top: 10%; left: 5%; background: rgba(10,22,40,0.85); backdrop-filter: blur(8px); padding: 15px; border-radius: 12px; border-left: 4px solid #ff4757; min-width: 140px;">
                    <div style="color: #94a3b8; font-size: 10px; text-transform: uppercase;">Elbow Angle</div>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: white; font-size: 24px; font-weight: 700;">142°</span>
                        <span style="background: rgba(255,71,87,0.2); color: #ff4757; font-size: 10px; padding: 2px 6px; border-radius: 4px; border: 1px solid #ff4757;">FIX</span>
                    </div>
                </div>

                <div style="position: absolute; bottom: 10%; right: 5%; background: rgba(10,22,40,0.85); backdrop-filter: blur(8px); padding: 15px; border-radius: 12px; border-left: 4px solid #10b981; min-width: 140px;">
                    <div style="color: #94a3b8; font-size: 10px; text-transform: uppercase;">Body Roll</div>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: white; font-size: 24px; font-weight: 700;">65°</span>
                        <span style="background: rgba(16,185,129,0.2); color: #10b981; font-size: 10px; padding: 2px 6px; border-radius: 4px; border: 1px solid #10b981;">OK</span>
                    </div>
                </div>
            </div>
        </div>
        """
        components.html(html_code, height=580)

    # 4. CTA / Pricing
    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        st.markdown("""
        <div class="cta-box">
            <div style="font-size: 0.9rem; color: #22d3ee; font-weight: 700; margin-bottom: 8px; letter-spacing: 2px;">START YOUR IMPROVEMENT</div>
            <div style="font-size: 3.5rem; font-weight: 800; color: white;">$4.99 <span style="font-size: 1rem; color: #64748b; font-weight: 400;">/ report</span></div>
            <p style="color: #cbd5e1; margin: 15px 0 30px;">Includes PDF Report, Video Overlay, and Targeted Drills.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.link_button("🏊 Analyze My Stroke Now →", STRIPE_PAYMENT_LINK, type="primary", use_container_width=True)
        
        if IS_DEV:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Dev: Skip to Dashboard", use_container_width=True):
                st.session_state.paid = True
                st.rerun()

    # 5. Feature Engine Section
    st.markdown('<h2 style="text-align:center; font-size:2.5rem; margin:80px 0 40px; color: white;">The Analysis Engine</h2>', unsafe_allow_html=True)
    
    features = [
        ("📊", "7 Biometrics", "Stroke rate, DPS, entry angle, elbow drop, and body rotation measured frame-by-frame."),
        ("🎯", "Ranked Issues", "We rank your 1-3 biggest speed leaks so you know exactly what to fix first."),
        ("🏊", "Drill Prescription", "Personalized drills with rep counts and focus cues to correct your specific flaws."),
        ("🎥", "Pro Comparison", "Your stroke overlaid with Olympic-level reference footage for visual alignment."),
        ("📈", "Progress Tracking", "Upload follow-up videos to track improvement across all metrics over time."),
        ("⚡", "90-Sec Turnaround", "Proprietary AI processing delivers a deep-dive PDF report almost instantly.")
    ]

    # Render Features in a 3-column grid
    feat_cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(features):
        with feat_cols[i % 3]:
            st.markdown(f"""
            <div style="background: rgba(15, 23, 42, 0.5); border: 1px solid rgba(148, 163, 184, 0.1); border-radius: 20px; padding: 30px 20px; text-align: center; height: 100%; margin-bottom: 20px;">
                <div style="font-size: 2.5rem; margin-bottom: 15px;">{icon}</div>
                <h3 style="color: #22d3ee; font-size: 1.2rem; margin-bottom: 10px;">{title}</h3>
                <p style="color: #94a3b8; font-size: 0.9rem; line-height: 1.5;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    # 6. Footer
    st.markdown("""
    <div style="text-align: center; margin-top: 100px; padding: 40px 0; border-top: 1px solid rgba(6, 182, 212, 0.1); color: #64748b; font-size: 0.8rem;">
        © 2026 SwimForm AI · Built for the Competitive Lane · <a href="#" style="color: #22d3ee; text-decoration: none;">Privacy Policy</a>
    </div>
    """, unsafe_allow_html=True)

# =============================================
# MAIN ROUTING LOGIC
# =============================================
# Stripe success detection
if st.query_params.get("success") == "true":
    st.session_state.paid = True
    st.query_params.clear()
    st.balloons()
    st.rerun()

if st.session_state.paid:
    # If using separate files, this would be st.switch_page("pages/Dashboard.py")
    st.title("🏊 Your Analysis Dashboard")
    st.write("Welcome! Please upload your video below.")
    uploaded_file = st.file_uploader("Upload Swim Video", type=["mp4", "mov", "avi"])
    if uploaded_file:
        st.success("Video received! Processing...")
else:
    show_landing_page()
