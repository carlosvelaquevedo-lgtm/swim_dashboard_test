import streamlit as st
import streamlit.components.v1 as components

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
# CONFIG & SECRETS
# =============================================
STRIPE_PAYMENT_LINK = "https://buy.stripe.com/test_8x2eVdaBSe7mf2JaIEao800"
IS_DEV = True

if "paid" not in st.session_state:
    st.session_state.paid = False

# =============================================
# CSS STYLING (Theming & Advanced Animations)
# =============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Space+Mono:wght@700&display=swap');

    /* Global Theme */
    .stApp, [data-testid="stAppViewContainer"], .main, .block-container {
        background: #0a1628 !important;
        color: #f0fdff;
        font-family: 'Inter', sans-serif;
    }

    /* --- Background Layers --- */
    .water-bg {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -10;
        background: linear-gradient(180deg, #0a1628 0%, #0f2847 30%, #0e3d6b 60%, #0f2847 100%);
    }
    .water-bg::before {
        content: ''; position: absolute; inset: 0;
        background: radial-gradient(ellipse at 20% 20%, rgba(6, 182, 212, 0.15) 0%, transparent 50%);
        animation: waterShimmer 8s ease-in-out infinite;
    }
    .lane-lines {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -9; opacity: 0.03;
        background: repeating-linear-gradient(90deg, #22d3ee 0px, #22d3ee 4px, transparent 4px, transparent 150px);
    }
    @keyframes waterShimmer { 0%, 100% { opacity: 0.5; transform: translateY(0); } 50% { opacity: 1; transform: translateY(-20px); } }

    /* --- Floating Bubbles --- */
    .bubble {
        position: fixed; border-radius: 50%; z-index: -8;
        background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.2), rgba(6, 182, 212, 0.05));
        animation: float 15s infinite ease-in-out;
    }
    .b1 { width: 80px; height: 80px; top: 20%; left: 10%; }
    .b2 { width: 40px; height: 40px; top: 60%; left: 85%; animation-delay: -5s; }
    @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-40px); } }

    /* --- Components --- */
    [data-testid="stToolbar"], [data-testid="stHeader"] { visibility: hidden; }

    .hero-badge {
        display: inline-flex; align-items: center; gap: 8px;
        background: rgba(6, 182, 212, 0.15); border: 1px solid rgba(6, 182, 212, 0.3);
        padding: 8px 16px; border-radius: 100px; font-size: 0.85rem; color: #22d3ee;
    }

    .cta-box {
        background: rgba(15, 40, 71, 0.6);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(6, 182, 212, 0.2);
        border-radius: 24px; padding: 40px; text-align: center;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }

    .f-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(34, 211, 238, 0.1);
        border-radius: 20px; padding: 25px; height: 100%;
        transition: all 0.3s ease;
    }
    .f-card:hover { border-color: #22d3ee; transform: translateY(-5px); background: rgba(34, 211, 238, 0.05); }

    /* --- SVG Animations --- */
    @keyframes swim-stroke { 0%, 100% { transform: translateX(0); } 50% { transform: translateX(-5px); } }
    @keyframes arm-pull { 0%, 100% { transform: rotate(0deg); } 50% { transform: rotate(-10deg); } }
    .swimmer-group { animation: swim-stroke 3s ease-in-out infinite; }
    .ai-node { fill: #22d3ee; filter: drop-shadow(0 0 3px #22d3ee); }
    .ai-line { stroke: #22d3ee; stroke-width: 0.5; opacity: 0.5; }
</style>

<div class="water-bg"></div>
<div class="lane-lines"></div>
<div class="bubble b1"></div>
<div class="bubble b2"></div>
""", unsafe_allow_html=True)

def show_landing_page():
    # --- 1. Navigation (Centered) ---
    st.markdown("""
    <div style="padding: 20px 0; display: flex; justify-content: center; align-items: center;">
        <div style="font-family: 'Space Mono', monospace; font-size: 1.5rem; font-weight: 700; color: #22d3ee; display: flex; align-items: center; gap: 12px;">
            <svg width="30" height="30" viewBox="0 0 32 32"><circle cx="16" cy="16" r="14" fill="none" stroke="currentColor" stroke-width="2"/><path d="M 8 16 Q 16 12 24 16" stroke="currentColor" stroke-width="2.5" fill="none"/></svg>
            SWIMFORM AI
        </div>
    </div>
    """, unsafe_allow_html=True)
    # --- 3. How It Works (The 3 Steps) ---
def show_landing_page():
    # ... previous code ...

    # LINE 114: Ensure 'st.markdown' starts at the same level as other lines
    st.markdown("""
    <style>
    .process-section { padding: 60px 0; text-align: center; }
    .process-title { font-size: 2.8rem; font-weight: 700; margin-bottom: 50px; color: white !important; }
    .process-grid { display: flex; justify-content: center; align-items: center; gap: 15px; flex-wrap: nowrap; margin: 0 auto; }
    .process-card { background: linear-gradient(180deg, rgba(20,50,90,0.9), rgba(15,40,71,0.9)); border-radius: 24px; padding: 30px 20px; width: 260px; border: 1px solid rgba(34,211,238,0.15); text-align: center; }
    .process-number { width: 45px; height: 45px; margin: 0 auto 15px auto; border-radius: 50%; background: #22d3ee; color: #0a1628; font-weight: 800; display: flex; align-items: center; justify-content: center; }
    .process-card h3 { color: #22d3ee !important; margin-bottom: 10px; font-size: 1.25rem; }
    .process-card p { color: #94a3b8 !important; font-size: 0.9rem; line-height: 1.5; }
    .process-arrow { font-size: 1.8rem; color: rgba(34,211,238,0.4); font-weight: bold; }
    @media (max-width: 900px) { .process-grid { flex-direction: column; } .process-arrow { transform: rotate(90deg); } }
    </style>
    
    <div class="process-section">
    <div class="process-title">How it works</div>
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
    <p>10–15s clip. Side view underwater works best.</p>
    </div>
    <div class="process-arrow">→</div>
    <div class="process-card">
    <div class="process-number">3</div>
    <h3>Get Report</h3>
    <p>AI analysis in 90s. Download PDF + video.</p>
    </div>
    </div>
    </div>
    """, unsafe_allow_html=True)

    # --- 2. Hero Section + Loom Placeholder ---
    components.html("""
    <style>
    body { margin:0; background:transparent; }
    
    /* WRAPPER */
    .hero-wrapper {
        position: relative;
        max-width: 1000px;
        margin: 0 auto 120px auto;
    }
    
    /* GLOW */
    .hero-glow {
        position: absolute;
        inset: -40px;
        background: radial-gradient(circle at center, rgba(6,182,212,0.35), transparent 60%);
        filter: blur(80px);
        animation: glowPulse 6s ease-in-out infinite;
    }
    
    @keyframes glowPulse {
        0%,100% { opacity: 0.6; }
        50% { opacity: 1; }
    }
    
    /* VIDEO CARD */
    .hero-video {
        position: relative;
        border-radius: 32px;
        overflow: hidden;
        border: 1px solid rgba(6,182,212,0.25);
        box-shadow: 0 40px 100px rgba(0,0,0,0.6);
    }
    
    /* 16:9 */
    .video-inner {
        position: relative;
        padding-bottom: 56.25%;
        height: 0;
    }
    
    .video-inner iframe {
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
    }
    
    /* SCAN LINE */
    .scan-line {
        position: absolute;
        left: 0;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, transparent, #22d3ee, transparent);
        animation: scanMove 3s linear infinite;
    }
    
    @keyframes scanMove {
        0% { top: 0%; }
        100% { top: 100%; }
    }
    
    /* METRICS */
    .metric {
        position: absolute;
        background: rgba(15,40,71,0.85);
        border: 1px solid rgba(34,211,238,0.4);
        padding: 10px 16px;
        border-radius: 14px;
        font-size: 13px;
        backdrop-filter: blur(10px);
    }
    
    .metric span {
        color: #22d3ee;
        font-weight: 700;
    }
    
    .metric-1 { top: 20px; left: 20px; }
    .metric-2 { bottom: 20px; right: 20px; }
    
    </style>
    
    <div class="hero-wrapper">
        <div class="hero-glow"></div>
    
        <div class="hero-video">
            <div class="video-inner">
                <iframe 
                    id="ytplayer"
                    src="https://www.youtube.com/embed/5HLW2AI1Ink?enablejsapi=1&mute=1&controls=0&rel=0"
                    frameborder="0"
                    allow="autoplay; encrypted-media">
                </iframe>
    
                <div class="scan-line"></div>
    
                <div class="metric metric-1">
                    Elbow Angle<br><span>118°</span>
                </div>
    
                <div class="metric metric-2">
                    Stroke Rate<br><span>32 spm</span>
                </div>
    
            </div>
        </div>
    </div>
    
    <script>
    var iframe = document.getElementById("ytplayer");
    var player;
    
    function onYouTubeIframeAPIReady() {
        player = new YT.Player('ytplayer');
    }
    
    var tag = document.createElement('script');
    tag.src = "https://www.youtube.com/iframe_api";
    document.body.appendChild(tag);
    
    document.querySelector('.hero-video').addEventListener('mouseenter', function() {
        if(player) player.playVideo();
    });
    
    document.querySelector('.hero-video').addEventListener('mouseleave', function() {
        if(player) player.pauseVideo();
    });
    </script>
    """, height=600)

    # --- Feature Grid ---
    st.markdown('<h2 style="text-align: center; font-size: 2.5rem; margin: 80px 0 50px;">The Analysis Engine</h2>', unsafe_allow_html=True)
    
    f_cols = st.columns(3)
    features = [
        ("📊", "7 Biometrics", "Stroke rate, DPS, entry angle, elbow drop, and body rotation measured frame-by-frame."),
        ("🎯", "Ranked Issues", "We rank your 1-3 biggest speed leaks so you know exactly what to fix first."),
        ("🏊", "Drill Prescription", "Personalized drills with rep counts and focus cues to correct your specific flaws."),
        ("🎥", "Pro Comparison", "Your stroke overlaid with Olympic-level reference footage for visual alignment."),
        ("📈", "Progress Charting", "Upload follow-up videos to track improvement across all metrics session-over-session."),
        ("⚡", "90-Sec Turnaround", "Proprietary AI processing delivers a deep-dive PDF report while you're still at the pool.")
    ]
    
    for i, (icon, title, desc) in enumerate(features):
        with f_cols[i % 3]:
            st.markdown(f"""
            <div class="f-card">
                <div style="font-size: 2rem; margin-bottom: 15px;">{icon}</div>
                <h3 style="color: #22d3ee; margin-bottom: 10px; font-size: 1.2rem;">{title}</h3>
                <p style="color: #94a3b8; font-size: 0.95rem; line-height: 1.5;">{desc}</p>
            </div>
            <div style="height: 25px;"></div>
            """, unsafe_allow_html=True)
    # --- 6. Final CTA / Pricing (Centered with Demo) ---
    # Pricing Box
    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        st.markdown("""
        <div class="cta-box">
            <div style="font-size: 0.9rem; color: #22d3ee; font-weight: 700; margin-bottom: 10px; letter-spacing: 1px;">INSTANT ANALYSIS</div>
            <div style="font-size: 3.5rem; font-weight: 800; color: white;">$4.99 <span style="font-size: 1rem; color: #64748b; font-weight: 400;">/ video</span></div>
            <p style="color: #94a3b8; margin: 15px 0 30px;">Full PDF Report • Side-by-Side Playback • Drill Cards</p>
        </div>
        """, unsafe_allow_html=True)
        st.link_button("🏊 Get My Biomechanics Report →", STRIPE_PAYMENT_LINK, type="primary", use_container_width=True)
        if IS_DEV:
            if st.button("Developer: Skip to Dashboard", use_container_width=True):
                st.session_state.paid = True
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    # --- Camera Angles (Animated Skeletal SVGs) ---
    st.markdown('<h2 style="text-align: center; font-size: 2.5rem; margin: 80px 0 40px;">Optimized Recording Angles</h2>', unsafe_allow_html=True)
    a_cols = st.columns(4)

    # Angle 1: Side Underwater
    with a_cols[0]:
        st.markdown("""
        <div style="background: #07111d; border-radius: 15px; padding: 15px; border: 1px solid rgba(255,255,255,0.05);">
            <svg viewBox="0 0 200 120" width="100%">
                <rect fill="#0a1628" width="200" height="120" rx="8"/>
                <g class="swimmer-group">
                    <ellipse cx="70" cy="50" rx="25" ry="10" fill="#22d3ee" opacity="0.2"/> <circle cx="45" cy="48" r="7" fill="#22d3ee" opacity="0.3"/> <line x1="45" y1="48" x2="75" y2="52" class="ai-line"/> <line x1="45" y1="48" x2="25" y2="42" class="ai-line"/> <circle cx="45" cy="48" r="2" class="ai-node"/> <circle cx="75" cy="52" r="2" class="ai-node"/> <circle cx="25" cy="42" r="2" class="ai-node"/> </g>
                <text x="100" y="110" fill="#22d3ee" font-size="8" text-anchor="middle" font-family="Space Mono">SIDE • UNDERWATER</text>
            </svg>
        </div>
        <div style="margin-top:15px; text-align:center;">
            <div style="color:#10b981; font-size:0.8rem; font-weight:700;">★ RECOMMENDED</div>
            <div style="font-weight:600; margin:5px 0;">Side View</div>
            <div style="font-size:0.8rem; color:#64748b;">Best for pull path & elbow position.</div>
        </div>
        """, unsafe_allow_html=True)

    # Angle 2: Front Underwater
    with a_cols[1]:
        st.markdown("""
        <div style="background: #07111d; border-radius: 15px; padding: 15px; border: 1px solid rgba(255,255,255,0.05);">
            <svg viewBox="0 0 200 120" width="100%">
                <rect fill="#0a1628" width="200" height="120" rx="8"/>
                <g class="swimmer-group">
                    <ellipse cx="100" cy="50" rx="15" ry="20" fill="#22d3ee" opacity="0.2"/>
                    <circle cx="100" cy="35" r="8" fill="#22d3ee" opacity="0.3"/>
                    <circle cx="100" cy="35" r="2" class="ai-node"/>
                    <line x1="85" y1="50" x2="115" y2="50" class="ai-line"/>
                    <circle cx="85" cy="50" r="2" class="ai-node"/>
                    <circle cx="115" cy="50" r="2" class="ai-node"/>
                </g>
                <text x="100" y="110" fill="#22d3ee" font-size="8" text-anchor="middle" font-family="Space Mono">FRONT • UNDERWATER</text>
            </svg>
        </div>
        <div style="margin-top:15px; text-align:center;">
            <div style="color:#94a3b8; font-size:0.8rem; font-weight:700;">SUPPORTED</div>
            <div style="font-weight:600; margin:5px 0;">Front View</div>
            <div style="font-size:0.8rem; color:#64748b;">Best for symmetry & crossover.</div>
        </div>
        """, unsafe_allow_html=True)

    # Angle 3: Side Above Water
    with a_cols[2]:
        st.markdown("""
        <div style="background: #07111d; border-radius: 15px; padding: 15px; border: 1px solid rgba(255,255,255,0.05);">
            <svg viewBox="0 0 200 120" width="100%">
                <rect fill="#0a1628" width="200" height="120" rx="8"/>
                <line x1="0" y1="60" x2="200" y2="60" stroke="#22d3ee" stroke-width="1" opacity="0.4"/>
                <g class="swimmer-group">
                    <path d="M 60 60 Q 90 30 120 50" stroke="#22d3ee" stroke-width="3" fill="none" opacity="0.4"/>
                    <circle cx="60" cy="55" r="5" fill="#22d3ee" opacity="0.3"/>
                    <circle cx="90" cy="30" r="2" class="ai-node"/>
                </g>
                <text x="100" y="110" fill="#22d3ee" font-size="8" text-anchor="middle" font-family="Space Mono">SIDE • ABOVE WATER</text>
            </svg>
        </div>
        <div style="margin-top:15px; text-align:center;">
            <div style="color:#94a3b8; font-size:0.8rem; font-weight:700;">SUPPORTED</div>
            <div style="font-weight:600; margin:5px 0;">Above Water</div>
            <div style="font-size:0.8rem; color:#64748b;">Best for recovery & head position.</div>
        </div>
        """, unsafe_allow_html=True)

    # Angle 4: Avoid (Drone/Top Down)
    with a_cols[3]:
        st.markdown("""
        <div style="background: #07111d; border-radius: 15px; padding: 15px; border: 1px solid rgba(255,255,255,0.05); opacity: 0.4;">
            <svg viewBox="0 0 200 120" width="100%">
                <rect fill="#0a1628" width="200" height="120" rx="8"/>
                <line x1="50" y1="30" x2="150" y2="90" stroke="#ef4444" stroke-width="2"/>
                <line x1="150" y1="30" x2="50" y2="90" stroke="#ef4444" stroke-width="2"/>
                <text x="100" y="110" fill="#ef4444" font-size="8" text-anchor="middle" font-family="Space Mono">DIRECT TOP-DOWN</text>
            </svg>
        </div>
        <div style="margin-top:15px; text-align:center;">
            <div style="color:#ef4444; font-size:0.8rem; font-weight:700;">AVOID</div>
            <div style="font-weight:600; margin:5px 0;">Direct Top</div>
            <div style="font-size:0.8rem; color:#64748b;">Refraction obscures AI tracking.</div>
        </div>
        """, unsafe_allow_html=True)

    # --- Footer ---
    st.markdown("""
    <div style="text-align: center; margin-top: 100px; padding: 40px 0; border-top: 1px solid rgba(6, 182, 212, 0.1); color: #64748b; font-size: 0.8rem;">
        © 2026 SwimForm AI · Professional Biomechanics for Every Lane · <a href="mailto:support@swimform.ai" style="color: #22d3ee; text-decoration: none;">Support</a>
    </div>
    """, unsafe_allow_html=True)

# =============================================
# MAIN ROUTER (Clean & Reliable)
# =============================================

# Handle Stripe success redirect
q = st.query_params
if q.get("success") == "true":
    st.session_state.paid = True
    st.query_params.clear()          # clean the URL
    st.balloons()
    st.rerun()                       # important

# ────── PAGE ROUTING ──────
if st.session_state.paid:
    st.switch_page("pages/2_Dashboard.py")   # ← This is the magic line

else:
    show_landing_page()
