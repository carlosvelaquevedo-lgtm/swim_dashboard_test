import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="SwimForm AI",
    page_icon="🏊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Hide Streamlit default chrome for a clean landing page
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {padding: 0 !important; max-width: 100% !important;}
    iframe {border: none !important;}
</style>
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

# Session state for payment
if "paid" not in st.session_state:
    st.session_state.paid = False


def show_landing_page():
    # ─────────────────────────────────────────────
    # FULL LANDING PAGE HTML WITH WORKING BUTTONS
    # ─────────────────────────────────────────────
    landing_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SwimForm AI - Instant Technique Analysis</title>
        <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Space+Mono:wght@700&display=swap" rel="stylesheet">
        <style>
            :root {{
                --deep-pool: #0a1628;
                --mid-water: #0f2847;
                --surface-glow: #06b6d4;
                --lane-line: #22d3ee;
                --bubble-white: #f0fdff;
                --alert-red: #ff4757;
                --success-green: #10b981;
                --gold-medal: #fbbf24;
            }}

            * {{ margin: 0; padding: 0; box-sizing: border-box; }}

            body {{
                font-family: 'DM Sans', -apple-system, sans-serif;
                background: var(--deep-pool);
                color: var(--bubble-white);
                min-height: 100vh;
                overflow-x: hidden;
            }}

            .water-bg {{
                position: fixed;
                top: 0; left: 0;
                width: 100%; height: 100%;
                z-index: -1;
                background: linear-gradient(180deg, var(--deep-pool) 0%, var(--mid-water) 30%, #0e3d6b 60%, var(--mid-water) 100%);
            }}

            .water-bg::before {{
                content: '';
                position: absolute;
                top: 0; left: 0; right: 0; bottom: 0;
                background: 
                    radial-gradient(ellipse at 20% 20%, rgba(6, 182, 212, 0.15) 0%, transparent 50%),
                    radial-gradient(ellipse at 80% 80%, rgba(6, 182, 212, 0.1) 0%, transparent 50%);
                animation: waterShimmer 8s ease-in-out infinite;
            }}

            @keyframes waterShimmer {{
                0%, 100% {{ opacity: 0.5; transform: translateY(0); }}
                50% {{ opacity: 1; transform: translateY(-20px); }}
            }}

            .lane-lines {{
                position: fixed;
                top: 0; left: 0;
                width: 100%; height: 100%;
                z-index: -1;
                opacity: 0.03;
                background: repeating-linear-gradient(90deg, var(--lane-line) 0px, var(--lane-line) 4px, transparent 4px, transparent 150px);
            }}

            .bubble {{
                position: fixed;
                border-radius: 50%;
                background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.4), rgba(6, 182, 212, 0.1));
                animation: float 15s infinite ease-in-out;
                z-index: -1;
            }}

            @keyframes float {{
                0%, 100% {{ transform: translateY(0) rotate(0deg); }}
                33% {{ transform: translateY(-30px) rotate(5deg); }}
                66% {{ transform: translateY(20px) rotate(-5deg); }}
            }}

            .bubble:nth-child(1) {{ width: 80px; height: 80px; top: 20%; left: 10%; }}
            .bubble:nth-child(2) {{ width: 40px; height: 40px; top: 60%; left: 85%; animation-delay: -5s; }}
            .bubble:nth-child(3) {{ width: 60px; height: 60px; top: 80%; left: 20%; animation-delay: -10s; }}
            .bubble:nth-child(4) {{ width: 30px; height: 30px; top: 40%; left: 70%; animation-delay: -3s; }}

            .container {{ max-width: 1100px; margin: 0 auto; padding: 0 24px; }}

            header {{ padding: 20px 0; position: relative; z-index: 10; }}

            .logo {{
                font-family: 'Space Mono', monospace;
                font-size: 1.5rem;
                font-weight: 700;
                color: var(--surface-glow);
                text-decoration: none;
                display: inline-flex;
                align-items: center;
                gap: 10px;
            }}

            .hero {{ padding: 60px 0 20px; text-align: center; }}

            .hero-badge {{
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
            }}

            .hero-badge::before {{ content: '⚡'; }}

            @keyframes fadeInUp {{
                from {{ opacity: 0; transform: translateY(20px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}

            h1 {{
                font-size: clamp(2.5rem, 6vw, 4rem);
                font-weight: 700;
                line-height: 1.1;
                margin-bottom: 20px;
                animation: fadeInUp 0.6s ease-out 0.1s both;
            }}

            h1 .highlight {{
                background: linear-gradient(135deg, var(--surface-glow), var(--lane-line));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }}

            .hero-subtitle {{
                font-size: 1.25rem;
                color: rgba(240, 253, 255, 0.7);
                max-width: 600px;
                margin: 0 auto 40px;
                line-height: 1.6;
                animation: fadeInUp 0.6s ease-out 0.2s both;
            }}

            .cta-box {{
                background: linear-gradient(135deg, rgba(15, 40, 71, 0.8) 0%, rgba(10, 22, 40, 0.9) 100%);
                border: 1px solid rgba(6, 182, 212, 0.2);
                border-radius: 24px;
                padding: 40px;
                max-width: 500px;
                margin: 0 auto;
                position: relative;
                overflow: hidden;
                animation: fadeInUp 0.6s ease-out 0.3s both;
            }}

            .cta-box::before {{
                content: '';
                position: absolute;
                top: 0; left: 0; right: 0;
                height: 1px;
                background: linear-gradient(90deg, transparent, var(--surface-glow), transparent);
            }}

            .price-tag {{
                display: flex;
                align-items: baseline;
                justify-content: center;
                gap: 8px;
                margin-bottom: 8px;
            }}

            .price-amount {{
                font-size: 3rem;
                font-weight: 700;
                color: var(--surface-glow);
            }}

            .price-period {{
                font-size: 1.125rem;
                color: rgba(240, 253, 255, 0.6);
            }}

            .price-note {{
                font-size: 0.875rem;
                color: rgba(240, 253, 255, 0.5);
                margin-bottom: 32px;
            }}

            /* Working button styles */
            .cta-button {{
                display: block;
                width: 100%;
                padding: 18px 32px;
                font-size: 1.125rem;
                font-weight: 600;
                color: #0a1628;
                background: linear-gradient(135deg, #06b6d4, #22d3ee);
                border: none;
                border-radius: 12px;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 4px 20px rgba(6, 182, 212, 0.3);
                text-decoration: none;
                text-align: center;
                font-family: inherit;
            }}
            
            .cta-button:hover {{
                box-shadow: 0 6px 30px rgba(6, 182, 212, 0.5);
                transform: translateY(-2px);
            }}
            
            .demo-button {{
                display: block;
                width: 100%;
                margin-top: 16px;
                padding: 14px 24px;
                font-size: 0.95rem;
                font-weight: 500;
                color: rgba(240, 253, 255, 0.7);
                background: transparent;
                border: 1px solid rgba(240, 253, 255, 0.3);
                border-radius: 12px;
                cursor: pointer;
                transition: all 0.3s ease;
                text-decoration: none;
                text-align: center;
                font-family: inherit;
            }}
            
            .demo-button:hover {{
                border-color: rgba(6, 182, 212, 0.5);
                color: #06b6d4;
            }}

            .trust-signals {{
                display: flex;
                justify-content: center;
                gap: 20px;
                margin-top: 24px;
                font-size: 0.875rem;
                color: rgba(240, 253, 255, 0.6);
            }}

            .trust-signal {{
                display: flex;
                align-items: center;
                gap: 6px;
            }}

            .trust-signal::before {{
                content: '✓';
                color: var(--success-green);
                font-weight: 700;
            }}

            .features-section {{
                padding: 60px 0;
                background: linear-gradient(180deg, transparent 0%, rgba(6, 182, 212, 0.02) 100%);
            }}

            .section-title {{
                text-align: center;
                font-size: 2.5rem;
                font-weight: 700;
                margin-bottom: 48px;
            }}

            .features {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 24px;
            }}

            .feature {{
                background: rgba(15, 40, 71, 0.4);
                border: 1px solid rgba(6, 182, 212, 0.15);
                border-radius: 16px;
                padding: 32px;
                transition: all 0.3s ease;
            }}

            .feature:hover {{
                border-color: rgba(6, 182, 212, 0.4);
                transform: translateY(-4px);
                box-shadow: 0 8px 24px rgba(6, 182, 212, 0.15);
            }}

            .feature-icon {{
                width: 56px;
                height: 56px;
                border-radius: 12px;
                background: linear-gradient(135deg, rgba(6, 182, 212, 0.2), rgba(34, 211, 238, 0.1));
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.75rem;
                margin-bottom: 20px;
            }}

            .feature h3 {{
                font-size: 1.25rem;
                font-weight: 600;
                margin-bottom: 12px;
                color: var(--lane-line);
            }}

            .feature p {{
                color: rgba(240, 253, 255, 0.7);
                line-height: 1.6;
            }}

            .demo-section {{
                padding: 60px 0;
                background: linear-gradient(180deg, rgba(6, 182, 212, 0.02) 0%, transparent 100%);
            }}

            .demo-video-container {{
                max-width: 900px;
                margin: 0 auto;
            }}

            .demo-video-wrapper {{
                background: rgba(15, 40, 71, 0.4);
                border: 1px solid rgba(6, 182, 212, 0.15);
                border-radius: 16px;
                padding: 8px;
                min-height: 400px;
                display: flex;
                align-items: center;
                justify-content: center;
            }}

            .video-section {{
                padding: 60px 0;
            }}

            .video-cards {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
                gap: 24px;
                margin-bottom: 32px;
            }}

            .video-card {{
                background: rgba(15, 40, 71, 0.4);
                border: 1px solid rgba(6, 182, 212, 0.15);
                border-radius: 16px;
                padding: 20px;
                transition: all 0.3s ease;
            }}

            .video-card:hover {{
                border-color: rgba(6, 182, 212, 0.4);
                transform: translateY(-4px);
            }}

            .video-card.recommended {{
                border: 2px solid var(--gold-medal);
                background: linear-gradient(135deg, rgba(251, 191, 36, 0.1) 0%, rgba(15, 40, 71, 0.4) 100%);
                position: relative;
            }}

            .video-card.recommended::before {{
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
            }}

            .video-preview {{
                border-radius: 12px;
                overflow: hidden;
                margin-bottom: 16px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            }}

            .video-svg {{
                width: 100%;
                height: auto;
                display: block;
            }}

            .video-card h3 {{
                font-size: 1rem;
                font-weight: 600;
                color: var(--lane-line);
                margin-bottom: 8px;
            }}

            .video-metrics {{
                font-size: 0.875rem;
                color: rgba(240, 253, 255, 0.6);
                line-height: 1.5;
            }}

            .video-tip {{
                background: rgba(251, 191, 36, 0.1);
                border: 1px solid rgba(251, 191, 36, 0.3);
                border-radius: 12px;
                padding: 16px 20px;
                font-size: 0.9375rem;
                color: rgba(240, 253, 255, 0.9);
                text-align: center;
            }}

            .how-section {{
                padding: 60px 0;
                background: linear-gradient(180deg, transparent 0%, rgba(6, 182, 212, 0.02) 100%);
            }}

            .steps {{
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                align-items: center;
                gap: 24px;
            }}

            .step {{
                flex: 0 1 280px;
                background: rgba(15, 40, 71, 0.4);
                border: 1px solid rgba(6, 182, 212, 0.15);
                border-radius: 16px;
                padding: 32px;
                text-align: center;
            }}

            .step-number {{
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
            }}

            .step h3 {{
                font-size: 1.25rem;
                font-weight: 600;
                margin-bottom: 12px;
                color: var(--lane-line);
            }}

            .step p {{
                color: rgba(240, 253, 255, 0.7);
                line-height: 1.6;
            }}

            .step-arrow {{
                font-size: 1.5rem;
                color: var(--surface-glow);
                flex: 0 0 auto;
            }}

            .testimonial-section {{
                padding: 60px 0;
            }}

            .testimonial-card {{
                background: rgba(15, 40, 71, 0.4);
                border: 1px solid rgba(6, 182, 212, 0.15);
                border-radius: 20px;
                padding: 40px;
                max-width: 700px;
                margin: 0 auto;
            }}

            .testimonial-stars {{
                font-size: 1.5rem;
                color: var(--gold-medal);
                margin-bottom: 20px;
            }}

            .testimonial-quote {{
                font-size: 1.125rem;
                line-height: 1.7;
                color: rgba(240, 253, 255, 0.9);
                margin-bottom: 24px;
                font-style: italic;
            }}

            .testimonial-author {{
                display: flex;
                align-items: center;
                gap: 16px;
            }}

            .testimonial-avatar {{
                width: 56px;
                height: 56px;
                border-radius: 50%;
                background: linear-gradient(135deg, var(--surface-glow), var(--lane-line));
                color: var(--deep-pool);
                font-weight: 700;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.125rem;
            }}

            .testimonial-info h4 {{
                font-weight: 600;
                color: var(--lane-line);
                margin-bottom: 4px;
            }}

            .testimonial-info p {{
                font-size: 0.875rem;
                color: rgba(240, 253, 255, 0.6);
            }}

            .final-cta {{
                padding: 80px 0;
                text-align: center;
            }}

            .final-cta h2 {{
                font-size: 2.5rem;
                font-weight: 700;
                margin-bottom: 16px;
            }}

            .final-cta p {{
                font-size: 1.25rem;
                color: rgba(240, 253, 255, 0.7);
                margin-bottom: 32px;
            }}
            
            .final-cta .cta-button {{
                max-width: 400px;
                margin: 0 auto;
            }}

            footer {{
                padding: 40px 0;
                border-top: 1px solid rgba(6, 182, 212, 0.1);
                text-align: center;
            }}

            footer p {{
                color: rgba(240, 253, 255, 0.5);
                font-size: 0.875rem;
            }}

            footer a {{
                color: var(--surface-glow);
                text-decoration: none;
            }}

            footer a:hover {{
                text-decoration: underline;
            }}

            @media (max-width: 768px) {{
                .steps {{ flex-direction: column; }}
                .step-arrow {{ transform: rotate(90deg); }}
                .trust-signals {{ flex-direction: column; gap: 12px; }}
            }}
        </style>
    </head>
    <body>
        <div class="water-bg"></div>
        <div class="lane-lines"></div>
        <div class="bubble"></div>
        <div class="bubble"></div>
        <div class="bubble"></div>
        <div class="bubble"></div>

        <div id="main-content">
            <header>
                <div class="container">
                    <a href="#" class="logo">
                        <svg width="32" height="32" viewBox="0 0 32 32">
                            <circle cx="16" cy="16" r="14" fill="none" stroke="currentColor" stroke-width="2"/>
                            <path d="M 8 16 Q 16 12 24 16" stroke="currentColor" stroke-width="2.5" fill="none" stroke-linecap="round"/>
                            <circle cx="12" cy="14" r="1.5" fill="currentColor"/>
                            <circle cx="20" cy="14" r="1.5" fill="currentColor"/>
                        </svg>
                        SwimForm AI
                    </a>
                </div>
            </header>

            <main>
                <section class="hero">
                    <div class="container">
                        <div class="hero-badge">Video analysis powered by Claude AI</div>
                        <h1>Find the <span class="highlight">one fix</span><br/>that makes you faster</h1>
                        <p class="hero-subtitle">Upload your swim video. Get a biomechanics report in 90 seconds. Fix what coaches miss.</p>
                        
                        <div class="cta-box">
                            <div class="price-tag">
                                <span class="price-amount">$4.99</span>
                                <span class="price-period">per analysis</span>
                            </div>
                            <p class="price-note">One video • Full PDF report • Annotated playback</p>
                            
                            <!-- Working buttons using standard anchor tags -->
                            <a href="{STRIPE_PAYMENT_LINK}" class="cta-button" target="_top">
                                🏊 Get Instant Analysis → $4.99
                            </a>
                            
                            {f'<a href="{APP_BASE_URL}?demo=true" class="demo-button" target="_top">Skip Payment – Demo Mode (testing only)</a>' if IS_DEV else ''}
                            
                            <div class="trust-signals">
                                <span class="trust-signal">Secure checkout</span>
                                <span class="trust-signal">90-sec turnaround</span>
                                <span class="trust-signal">Download forever</span>
                            </div>
                        </div>
                    </div>
                </section>

                <section class="features-section">
                    <div class="container">
                        <h2 class="section-title">What you get</h2>
                        <div class="features">
                            <div class="feature">
                                <div class="feature-icon">📊</div>
                                <h3>7 Biomechanical Metrics</h3>
                                <p>Stroke rate, DPS, entry angle, elbow drop, kick depth, head position, body rotation—all measured frame-by-frame.</p>
                            </div>
                            <div class="feature">
                                <div class="feature-icon">🎯</div>
                                <h3>Ranked Issues (1-3)</h3>
                                <p>Not just a list. We tell you which fix will move the needle most based on your specific technique patterns.</p>
                            </div>
                            <div class="feature">
                                <div class="feature-icon">🏊</div>
                                <h3>Drill Prescription</h3>
                                <p>Exact drills with rep counts, focus cues, and when to return to full stroke. No guessing.</p>
                            </div>
                            <div class="feature">
                                <div class="feature-icon">🎥</div>
                                <h3>Side-by-Side Comparison</h3>
                                <p>Your stroke vs. Olympic reference footage with synchronized playback and annotation overlays.</p>
                            </div>
                            <div class="feature">
                                <div class="feature-icon">📈</div>
                                <h3>Progress Tracking</h3>
                                <p>Upload follow-up videos. We'll chart your improvement across all metrics session by session.</p>
                            </div>
                            <div class="feature">
                                <div class="feature-icon">⚡</div>
                                <h3>Instant PDF Download</h3>
                                <p>Complete report with screenshots, data tables, and drill cards. Share with coaches or keep for your records.</p>
                            </div>
                        </div>
                    </div>
                </section>

                <section class="demo-section">
                    <div class="container">
                        <h2 class="section-title">See it in action</h2>
                        <div class="demo-video-container">
                            <div class="demo-video-wrapper">
                                <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; color: rgba(240, 253, 255, 0.8); text-align: center; padding: 40px;">
                                    <svg viewBox="0 0 120 120" width="100" height="100" style="margin-bottom: 24px; opacity: 0.8;">
                                        <circle cx="60" cy="60" r="55" fill="none" stroke="rgba(6, 182, 212, 0.4)" stroke-width="3"/>
                                        <circle cx="60" cy="60" r="45" fill="rgba(6, 182, 212, 0.15)"/>
                                        <path d="M 48 38 L 48 82 L 82 60 Z" fill="#06b6d4"/>
                                    </svg>
                                    <h3 style="font-size: 1.5rem; margin-bottom: 12px; color: #22d3ee;">Demo Video Coming Soon</h3>
                                    <p style="font-size: 1.1rem; max-width: 500px; line-height: 1.6;">
                                        We're finalizing a full walkthrough showing the upload, AI analysis, and instant PDF report generation.
                                    </p>
                                    <p style="font-size: 0.95rem; margin-top: 20px; color: rgba(240, 253, 255, 0.6);">
                                        In the meantime, click "Get Instant Analysis" to try it yourself!
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>    

                <section class="video-section">
                    <div class="container">
                        <h2 class="section-title">Best camera angles</h2>

                        <div class="video-cards">
                            <!-- RECOMMENDED: Side View Underwater -->
                            <div class="video-card recommended">
                                <div class="video-preview">
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
                                        <!-- Pool background -->
                                        <rect fill="url(#poolGrad)" width="200" height="120" rx="8"/>
                                        <!-- Water surface line -->
                                        <path d="M0 20 Q50 15 100 20 T200 20" stroke="#22d3ee" stroke-width="1.5" fill="none" opacity="0.4"/>
                                        <!-- Lane line -->
                                        <line x1="0" y1="18" x2="200" y2="18" stroke="#22d3ee" stroke-width="3" stroke-dasharray="12,6" opacity="0.3"/>
                                        <!-- Swimmer silhouette - clean geometric style -->
                                        <g transform="translate(30, 45)">
                                            <!-- Body core -->
                                            <ellipse cx="70" cy="12" rx="55" ry="10" fill="url(#glowGrad)" opacity="0.9"/>
                                            <!-- Head -->
                                            <circle cx="15" cy="8" r="9" fill="#22d3ee"/>
                                            <!-- Extended arm (front) -->
                                            <line x1="25" y1="6" x2="-5" y2="2" stroke="#22d3ee" stroke-width="6" stroke-linecap="round"/>
                                            <!-- Pull arm (underneath) -->
                                            <path d="M60 15 Q75 30 95 20" stroke="#06b6d4" stroke-width="5" stroke-linecap="round" fill="none"/>
                                            <!-- Legs -->
                                            <line x1="120" y1="10" x2="145" y2="5" stroke="#06b6d4" stroke-width="5" stroke-linecap="round"/>
                                            <line x1="120" y1="14" x2="145" y2="20" stroke="#06b6d4" stroke-width="5" stroke-linecap="round" opacity="0.8"/>
                                        </g>
                                        <!-- Analysis overlay lines -->
                                        <line x1="45" y1="53" x2="45" y2="30" stroke="#fbbf24" stroke-width="1" stroke-dasharray="4,2" opacity="0.6"/>
                                        <line x1="45" y1="30" x2="55" y2="30" stroke="#fbbf24" stroke-width="1" opacity="0.6"/>
                                        <!-- Bubbles -->
                                        <circle cx="50" cy="60" r="2" fill="white" opacity="0.3"/>
                                        <circle cx="55" cy="55" r="1.5" fill="white" opacity="0.2"/>
                                        <circle cx="48" cy="65" r="1" fill="white" opacity="0.25"/>
                                        <!-- Label -->
                                        <text x="100" y="108" fill="rgba(255,255,255,0.8)" font-size="9" text-anchor="middle" font-family="system-ui">Side View • Underwater</text>
                                    </svg>
                                </div>
                                <h3>Side View + Underwater</h3>
                                <p class="video-metrics">Streamline, pull path, elbow position, kick timing</p>
                            </div>
                        
                            <!-- Side View Above Water -->
                            <div class="video-card">
                                <div class="video-preview">
                                    <svg viewBox="0 0 200 120" class="video-svg">
                                        <defs>
                                            <linearGradient id="skyGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                                                <stop offset="0%" stop-color="#1e3a5f"/>
                                                <stop offset="100%" stop-color="#0f2847"/>
                                            </linearGradient>
                                        </defs>
                                        <!-- Sky/indoor background -->
                                        <rect fill="url(#skyGrad)" width="200" height="120" rx="8"/>
                                        <!-- Water surface -->
                                        <rect x="0" y="55" width="200" height="65" fill="#0a1628" rx="0 0 8 8"/>
                                        <path d="M0 55 Q50 52 100 55 T200 55" stroke="#22d3ee" stroke-width="2" fill="none" opacity="0.5"/>
                                        <!-- Swimmer at surface -->
                                        <g transform="translate(25, 40)">
                                            <!-- Body breaking surface -->
                                            <ellipse cx="70" cy="18" rx="50" ry="8" fill="#06b6d4" opacity="0.6"/>
                                            <!-- Head (above water) -->
                                            <circle cx="20" cy="12" r="10" fill="#22d3ee"/>
                                            <!-- Recovery arm (above water) -->
                                            <path d="M35 8 Q70 -15 110 5" stroke="#22d3ee" stroke-width="5" stroke-linecap="round" fill="none"/>
                                            <!-- Catch arm entering -->
                                            <line x1="30" y1="15" x2="5" y2="20" stroke="#06b6d4" stroke-width="5" stroke-linecap="round"/>
                                        </g>
                                        <!-- Splash effect -->
                                        <circle cx="30" cy="55" r="3" fill="white" opacity="0.4"/>
                                        <circle cx="35" cy="52" r="2" fill="white" opacity="0.3"/>
                                        <circle cx="140" cy="53" r="2.5" fill="white" opacity="0.35"/>
                                        <!-- Label -->
                                        <text x="100" y="108" fill="rgba(255,255,255,0.8)" font-size="9" text-anchor="middle" font-family="system-ui">Side View • Above Water</text>
                                    </svg>
                                </div>
                                <h3>Side View + Above Water</h3>
                                <p class="video-metrics">Recovery arm, head position, breathing timing</p>
                            </div>
                        
                            <!-- Front View Underwater -->
                            <div class="video-card">
                                <div class="video-preview">
                                    <svg viewBox="0 0 200 120" class="video-svg">
                                        <!-- Pool background -->
                                        <rect fill="url(#poolGrad)" width="200" height="120" rx="8"/>
                                        <!-- Lane lines (perspective) -->
                                        <line x1="50" y1="0" x2="70" y2="120" stroke="#22d3ee" stroke-width="2" stroke-dasharray="8,4" opacity="0.2"/>
                                        <line x1="150" y1="0" x2="130" y2="120" stroke="#22d3ee" stroke-width="2" stroke-dasharray="8,4" opacity="0.2"/>
                                        <!-- Swimmer facing camera -->
                                        <g transform="translate(100, 55)">
                                            <!-- Body (torpedo shape from front) -->
                                            <ellipse cx="0" cy="0" rx="18" ry="35" fill="#06b6d4" opacity="0.8"/>
                                            <!-- Head -->
                                            <circle cx="0" cy="-28" r="12" fill="#22d3ee"/>
                                            <!-- Arms spread for catch -->
                                            <line x1="-15" y1="-10" x2="-50" y2="5" stroke="#22d3ee" stroke-width="6" stroke-linecap="round"/>
                                            <line x1="15" y1="-10" x2="50" y2="5" stroke="#22d3ee" stroke-width="6" stroke-linecap="round"/>
                                            <!-- Hands -->
                                            <circle cx="-50" cy="5" r="5" fill="#22d3ee"/>
                                            <circle cx="50" cy="5" r="5" fill="#22d3ee"/>
                                        </g>
                                        <!-- Body roll indicator -->
                                        <path d="M60 55 A40 20 0 0 1 140 55" stroke="#fbbf24" stroke-width="1.5" fill="none" stroke-dasharray="4,3" opacity="0.5"/>
                                        <!-- Bubbles -->
                                        <circle cx="90" cy="35" r="1.5" fill="white" opacity="0.3"/>
                                        <circle cx="110" cy="38" r="2" fill="white" opacity="0.25"/>
                                        <!-- Label -->
                                        <text x="100" y="108" fill="rgba(255,255,255,0.8)" font-size="9" text-anchor="middle" font-family="system-ui">Front View • Underwater</text>
                                    </svg>
                                </div>
                                <h3>Front View + Underwater</h3>
                                <p class="video-metrics">Body roll, hand entry width, kick symmetry</p>
                            </div>
                        
                            <!-- Front View Above Water -->
                            <div class="video-card">
                                <div class="video-preview">
                                    <svg viewBox="0 0 200 120" class="video-svg">
                                        <!-- Background -->
                                        <rect fill="url(#skyGrad)" width="200" height="120" rx="8"/>
                                        <rect x="0" y="60" width="200" height="60" fill="#0a1628"/>
                                        <!-- Water surface with ripples -->
                                        <ellipse cx="100" cy="60" rx="90" ry="8" fill="#0f2847"/>
                                        <ellipse cx="100" cy="60" rx="70" ry="5" fill="none" stroke="#22d3ee" stroke-width="1" opacity="0.3"/>
                                        <ellipse cx="100" cy="60" rx="50" ry="3" fill="none" stroke="#22d3ee" stroke-width="1" opacity="0.2"/>
                                        <!-- Swimmer head and shoulders from front -->
                                        <g transform="translate(100, 50)">
                                            <!-- Shoulders at surface -->
                                            <ellipse cx="0" cy="12" rx="30" ry="8" fill="#06b6d4" opacity="0.5"/>
                                            <!-- Head -->
                                            <circle cx="0" cy="-5" r="14" fill="#22d3ee"/>
                                            <!-- Entry arm -->
                                            <line x1="-25" y1="8" x2="-55" y2="-15" stroke="#22d3ee" stroke-width="5" stroke-linecap="round"/>
                                            <circle cx="-55" cy="-15" r="5" fill="#22d3ee"/>
                                            <!-- Other arm recovering -->
                                            <path d="M25 8 Q45 -20 55 -5" stroke="#06b6d4" stroke-width="4" stroke-linecap="round" fill="none" opacity="0.7"/>
                                        </g>
                                        <!-- Entry angle indicator -->
                                        <line x1="45" y1="35" x2="45" y2="60" stroke="#fbbf24" stroke-width="1" stroke-dasharray="3,2" opacity="0.6"/>
                                        <!-- Splash -->
                                        <circle cx="45" cy="58" r="4" fill="white" opacity="0.4"/>
                                        <circle cx="50" cy="55" r="2" fill="white" opacity="0.3"/>
                                        <!-- Label -->
                                        <text x="100" y="108" fill="rgba(255,255,255,0.8)" font-size="9" text-anchor="middle" font-family="system-ui">Front View • Above Water</text>
                                    </svg>
                                </div>
                                <h3>Front View + Above Water</h3>
                                <p class="video-metrics">Entry angle, breathing side</p>
                            </div>
                        </div>


                        <p class="video-tip">💡 <strong>Tip:</strong> 10-15 seconds of continuous swimming works best. Our AI auto-detects your camera angle!</p>
                    </div>
                </section>

                <section class="how-section">
                    <div class="container">
                        <h2 class="section-title">How it works</h2>
                        <div class="steps">
                             <div class="step">
                                 <div class="step-number">1</div>
                                 <h3>Pay $4.99</h3>
                                 <p>Secure checkout via Stripe. Instant access.</p>
                             </div>
                             <span class="step-arrow">→</span>
                             <div class="step">
                                 <div class="step-number">2</div>
                                 <h3>Upload Video</h3>
                                 <p>10-15 sec clip. Side view underwater works best.</p>
                             </div>
                             <span class="step-arrow">→</span>
                             <div class="step">
                                 <div class="step-number">3</div>
                                 <h3>Get Report</h3>
                                 <p>AI analyzes in 90 sec. Download PDF + annotated video.</p>
                             </div>
                        </div>
                    </div>
                </section>

                <section class="testimonial-section">
                    <div class="container">
                         <div class="testimonial-card">
                             <div class="testimonial-stars">★★★★★</div>
                             <blockquote class="testimonial-quote">
                                 "I've been coaching for 18 years and this caught a dropped elbow pattern I missed. My swimmer dropped 0.4 seconds in her next 100 free after 2 weeks of targeted drills."
                             </blockquote>
                             <div class="testimonial-author">
                                 <div class="testimonial-avatar">MK</div>
                                 <div class="testimonial-info">
                                     <h4>Mike K.</h4>
                                     <p>Head Coach, Aquatic Stars SC</p>
                                 </div>
                             </div>
                         </div>
                    </div>
                </section>

                <section class="final-cta">
                    <div class="container">
                        <h2>Ready to find your speed leak?</h2>
                        <p>One video. One analysis. One fix that changes everything.</p>
                        <a href="{STRIPE_PAYMENT_LINK}" class="cta-button" target="_top">
                            🏊 Get Instant Analysis → $4.99
                        </a>
                    </div>
                </section>
            </main>

            <footer>
                <div class="container">
                    <p>© 2026 SwimForm AI · <a href="#">Privacy</a> · <a href="#">Terms</a> · <a href="mailto:support@swimform.ai">support@swimform.ai</a></p>
                </div>
            </footer>
        </div>
    </body>
    </html>
    """

    # Render HTML landing page with working buttons
    components.html(landing_html, height=4500, scrolling=True)


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
    success = query_params.get("success", [None])[0] == "true"  # Use get with default to handle missing key
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
