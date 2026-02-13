import streamlit as st
import stripe

# ─────────────────────────────────────────────
# CONFIG & SECRETS
# ─────────────────────────────────────────────
# In your app.py / main.py — replace the direct access with:
try:
    stripe.api_key = st.secrets["stripe"]["secret_key"]
    APP_BASE_URL = st.secrets["stripe"].get("base_url", "http://localhost:8501")
except KeyError:
    st.error("Stripe secrets not found. Please add .streamlit/secrets.toml or configure secrets in Streamlit Cloud.")
    st.stop()

IS_DEV = True

# Session state for payment
if "paid" not in st.session_state:
    st.session_state.paid = False


def show_landing_page():
    # Optional demo button HTML (only shown when IS_DEV = True)
    if IS_DEV:
        demo_button_html = """
        <div style="margin-top: 24px; text-align: center;">
            <button 
                onclick="window.location.href = '?demo=true';" 
                style="
                    background: transparent;
                    border: 1px solid rgba(240,253,255,0.3);
                    color: rgba(240,253,255,0.7);
                    padding: 12px 24px;
                    border-radius: 12px;
                    font-size: 0.95rem;
                    cursor: pointer;
                    transition: all 0.2s;
                "
                onmouseover="this.style.borderColor='rgba(6,182,212,0.5)'; this.style.color='var(--surface-glow)';"
                onmouseout="this.style.borderColor='rgba(240,253,255,0.3)'; this.style.color='rgba(240,253,255,0.7)';"
            >
                Skip Payment – Enter Demo Mode (for testing only)
            </button>
        </div>
        """
    else:
        demo_button_html = ""

    # ─────────────────────────────────────────────
    # FULL LANDING PAGE HTML
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

            .hero {{ padding: 60px 0 80px; text-align: center; }}

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

            .cta-button {{
                width: 100%;
                padding: 18px 32px;
                font-size: 1.125rem;
                font-weight: 600;
                color: var(--deep-pool);
                background: linear-gradient(135deg, var(--surface-glow), var(--lane-line));
                border: none;
                border-radius: 12px;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 4px 20px rgba(6, 182, 212, 0.3);
            }}

            .cta-button:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 30px rgba(6, 182, 212, 0.5);
            }}

            .cta-button:active {{
                transform: translateY(0);
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

            .video-section {{
                padding: 60px 0;
            }}

            .demo-section {{
                padding: 60px 0;
                background: linear-gradient(180deg, rgba(6, 182, 212, 0.02) 0%, transparent 100%);
            }}

            .demo-video-container {{
                max-width: 900px;
                margin: 0 auto;
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
                gap: 24px;
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

            .demo-video-wrapper iframe {{
                width: 100%;
                height: 100%;
                min-height: 400px;
                border-radius: 12px;
            }}

            .demo-placeholder {{
                text-align: center;
                padding: 60px 40px;
                color: rgba(240, 253, 255, 0.5);
            }}

            .demo-placeholder svg {{
                margin-bottom: 20px;
                opacity: 0.6;
            }}

            .demo-placeholder p {{
                font-size: 1.125rem;
                margin-bottom: 8px;
                color: rgba(240, 253, 255, 0.7);
            }}

            .demo-instruction {{
                font-size: 0.875rem;
                color: rgba(6, 182, 212, 0.6);
                font-style: italic;
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

            .success-page {{
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 24px;
            }}

            .success-card {{
                background: linear-gradient(135deg, rgba(15, 40, 71, 0.8) 0%, rgba(10, 22, 40, 0.9) 100%);
                border: 1px solid rgba(6, 182, 212, 0.2);
                border-radius: 24px;
                padding: 60px 40px;
                max-width: 500px;
                text-align: center;
            }}

            .success-icon {{
                font-size: 4rem;
                margin-bottom: 24px;
            }}

            .success-card h1 {{
                font-size: 2rem;
                margin-bottom: 16px;
            }}

            .success-card p {{
                color: rgba(240, 253, 255, 0.7);
                margin-bottom: 32px;
            }}

            .success-note {{
                font-size: 0.875rem;
                color: rgba(240, 253, 255, 0.5);
                margin-top: 24px !important;
            }}

            /* Enhanced SVG Animations */
            @keyframes swim-stroke {{
                0%, 100% {{ transform: translateX(0) rotate(0deg); }}
                50% {{ transform: translateX(-8px) rotate(-3deg); }}
            }}

            @keyframes arm-pull {{
                0%, 100% {{ transform: rotate(0deg); }}
                50% {{ transform: rotate(-15deg); }}
            }}

            @keyframes bubble-rise {{
                0% {{ transform: translateY(0) scale(1); opacity: 0.6; }}
                100% {{ transform: translateY(-30px) scale(0.5); opacity: 0; }}
            }}

            @media (max-width: 768px) {{
                .steps {{ flex-direction: column; }}
                .step-arrow {{ transform: rotate(90deg); }}
                .trust-signals {{ flex-direction: column; gap: 12px; }}
                .demo-video-container {{ grid-template-columns: 1fr; }}
                .demo-video-wrapper {{ min-height: 300px; }}
                .demo-video-wrapper iframe {{ min-height: 300px; }}
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
                            <button id="checkout-button" class="cta-button">Get Instant Analysis →</button>
                            <div class="trust-signals">
                                <span class="trust-signal">Secure checkout</span>
                                <span class="trust-signal">90-sec turnaround</span>
                                <span class="trust-signal">Download forever</span>
                            </div>
                            {demo_button_html}
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
                                    <h3 style="font-size: 1.5rem; margin-bottom: 12px; color: var(--lane-line);">Demo Video Coming Soon</h3>
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
                            <div class="video-card recommended">
                                <div class="video-preview">
                                    <svg viewBox="0 0 200 120" class="video-svg">
                                        <defs>
                                            <linearGradient id="waterGrad1" x1="0%" y1="0%" x2="0%" y2="100%">
                                                <stop offset="0%" style="stop-color:#0a1628;stop-opacity:1" />
                                                <stop offset="50%" style="stop-color:#0f2847;stop-opacity:1" />
                                                <stop offset="100%" style="stop-color:#0a1628;stop-opacity:1" />
                                            </linearGradient>
                                            <linearGradient id="swimmerGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                                                <stop offset="0%" style="stop-color:#06b6d4;stop-opacity:0.9" />
                                                <stop offset="100%" style="stop-color:#22d3ee;stop-opacity:0.7" />
                                            </linearGradient>
                                        </defs>
                                        <rect fill="url(#waterGrad1)" width="200" height="120" rx="8"/>
                                        <line x1="0" y1="15" x2="200" y2="15" stroke="#22d3ee" stroke-width="2" stroke-dasharray="8,4" opacity="0.5"/>
                                        <g class="swimmer-side">
                                            <ellipse cx="45" cy="48" rx="8" ry="10" fill="url(#swimmerGrad)"/>
                                            <ellipse cx="70" cy="50" rx="25" ry="12" fill="url(#swimmerGrad)"/>
                                            <ellipse cx="95" cy="52" rx="12" ry="10" fill="url(#swimmerGrad)"/>
                                            <path d="M 105 52 L 135 50 L 138 52" stroke="url(#swimmerGrad)" stroke-width="6" fill="none" stroke-linecap="round"/>
                                            <path d="M 105 52 L 135 54 L 138 56" stroke="url(#swimmerGrad)" stroke-width="5" fill="none" stroke-linecap="round" opacity="0.8"/>
                                            <line x1="40" y1="45" x2="15" y2="42" stroke="url(#swimmerGrad)" stroke-width="5" stroke-linecap="round"/>
                                            <circle cx="15" cy="42" r="4" fill="#06b6d4"/>
                                            <path d="M 50 50 Q 75 65 95 55" stroke="url(#swimmerGrad)" stroke-width="5" fill="none" stroke-linecap="round" class="pull-arm"/>
                                            <circle cx="95" cy="55" r="4" fill="#06b6d4"/>
                                        </g>
                                        <circle cx="40" cy="48" r="2.5" fill="white" opacity="0.6" class="splash1"/>
                                        <circle cx="45" cy="45" r="1.8" fill="white" opacity="0.5" class="splash2"/>
                                        <circle cx="50" cy="50" r="2" fill="white" opacity="0.4" class="splash1"/>
                                        <circle cx="100" cy="58" r="1.5" fill="white" opacity="0.5" class="splash2"/>
                                        <line x1="15" y1="42" x2="15" y2="25" stroke="#fbbf24" stroke-width="1" stroke-dasharray="3,2" opacity="0.7"/>
                                        <path d="M 15 35 A 8 8 0 0 1 20 30" stroke="#fbbf24" stroke-width="1" fill="none" opacity="0.7"/>
                                        <text x="100" y="108" fill="white" font-size="9" text-anchor="middle" opacity="0.9">Side View • Underwater</text>
                                    </svg>
                                </div>
                                <h3>Side View + Underwater</h3>
                                <p class="video-metrics">Streamline, pull path, elbow position, kick timing</p>
                            </div>
                        
                            <div class="video-card">
                                <div class="video-preview">
                                    <svg viewBox="0 0 200 120" class="video-svg">
                                        <defs>
                                            <linearGradient id="skyGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                                                <stop offset="0%" style="stop-color:#87ceeb;stop-opacity:1" />
                                                <stop offset="100%" style="stop-color:#4a90a4;stop-opacity:1" />
                                            </linearGradient>
                                        </defs>
                                        <rect fill="url(#skyGrad)" width="200" height="120" rx="8"/>
                                        <rect x="0" y="58" width="200" height="62" fill="#0f2847" opacity="0.6"/>
                                        <line x1="0" y1="58" x2="200" y2="58" stroke="#22d3ee" stroke-width="2" opacity="0.8"/>
                                        <g class="swimmer-side">
                                            <ellipse cx="50" cy="52" rx="7" ry="9" fill="#06b6d4"/>
                                            <ellipse cx="75" cy="58" rx="18" ry="8" fill="#06b6d4" opacity="0.8"/>
                                            <ellipse cx="95" cy="63" rx="14" ry="9" fill="#06b6d4" opacity="0.5"/>
                                            <path d="M 55 54 Q 85 30 115 45" stroke="#06b6d4" stroke-width="5" fill="none" stroke-linecap="round"/>
                                            <circle cx="115" cy="45" r="4" fill="#06b6d4"/>
                                            <path d="M 70 60 Q 80 75 90 68" stroke="#06b6d4" stroke-width="4" fill="none" stroke-linecap="round" opacity="0.6"/>
                                            <ellipse cx="120" cy="68" rx="15" ry="7" fill="#06b6d4" opacity="0.4"/>
                                        </g>
                                        <circle cx="115" cy="55" r="3" fill="white" opacity="0.6" class="splash1"/>
                                        <circle cx="120" cy="52" r="2" fill="white" opacity="0.4" class="splash2"/>
                                        <circle cx="48" cy="56" r="2.5" fill="white" opacity="0.5" class="splash1"/>
                                        <text x="100" y="108" fill="white" font-size="9" text-anchor="middle">Side View • Above Water</text>
                                    </svg>
                                </div>
                                <h3>Side View + Above Water</h3>
                                <p class="video-metrics">Recovery arm, head position, breathing timing</p>
                            </div>
                        
                            <div class="video-card">
                                <div class="video-preview">
                                    <svg viewBox="0 0 200 120" class="video-svg">
                                        <rect fill="url(#waterGrad1)" width="200" height="120" rx="8"/>
                                        <line x1="0" y1="15" x2="200" y2="15" stroke="#22d3ee" stroke-width="2" stroke-dasharray="8,4" opacity="0.4"/>
                                        <g class="swimmer-front">
                                            <ellipse cx="100" cy="35" rx="11" ry="13" fill="#06b6d4" opacity="0.95"/>
                                            <ellipse cx="95" cy="33" rx="3" ry="2" fill="#0a1628" opacity="0.6"/>
                                            <ellipse cx="105" cy="33" rx="3" ry="2" fill="#0a1628" opacity="0.6"/>
                                            <ellipse cx="100" cy="55" rx="22" ry="12" fill="#06b6d4" opacity="0.85"/>
                                            <ellipse cx="100" cy="75" rx="18" ry="10" fill="#06b6d4" opacity="0.75"/>
                                            <ellipse cx="100" cy="90" rx="14" ry="8" fill="#06b6d4" opacity="0.65"/>
                                            <line x1="78" y1="52" x2="50" y2="70" stroke="#06b6d4" stroke-width="7" stroke-linecap="round" class="arm-left"/>
                                            <circle cx="50" cy="70" r="5" fill="#06b6d4"/>
                                            <line x1="122" y1="52" x2="150" y2="70" stroke="#06b6d4" stroke-width="7" stroke-linecap="round" class="arm-right"/>
                                            <circle cx="150" cy="70" r="5" fill="#06b6d4"/>
                                            <line x1="93" y1="98" x2="88" y2="115" stroke="#06b6d4" stroke-width="6" stroke-linecap="round"/>
                                            <line x1="107" y1="98" x2="112" y2="115" stroke="#06b6d4" stroke-width="6" stroke-linecap="round"/>
                                        </g>
                                        <path d="M 75 62 A 25 25 0 0 1 125 62" stroke="#fbbf24" stroke-width="1.5" fill="none" stroke-dasharray="4,2" class="roll-arc"/>
                                        <circle cx="95" cy="38" r="2" fill="white" opacity="0.5" class="splash1"/>
                                        <circle cx="105" cy="40" r="1.5" fill="white" opacity="0.4" class="splash2"/>
                                        <text x="100" y="108" fill="white" font-size="9" text-anchor="middle">Front View • Underwater</text>
                                    </svg>
                                </div>
                                <h3>Front View + Underwater</h3>
                                <p class="video-metrics">Body roll, hand entry width, kick symmetry</p>
                            </div>
                        
                            <div class="video-card">
                                <div class="video-preview">
                                    <svg viewBox="0 0 200 120" class="video-svg">
                                        <rect fill="url(#skyGrad)" width="200" height="120" rx="8"/>
                                        <rect x="0" y="62" width="200" height="58" fill="#0f2847" opacity="0.5"/>
                                        <line x1="0" y1="62" x2="200" y2="62" stroke="#22d3ee" stroke-width="2" opacity="0.7"/>
                                        <g class="swimmer-front-surface">
                                            <ellipse cx="100" cy="56" rx="9" ry="11" fill="#06b6d4" opacity="0.95"/>
                                            <ellipse cx="100" cy="68" rx="18" ry="8" fill="#06b6d4" opacity="0.6"/>
                                            <line x1="82" y1="64" x2="58" y2="38" stroke="#06b6d4" stroke-width="6" stroke-linecap="round" class="entry-arm-l"/>
                                            <circle cx="58" cy="38" r="4.5" fill="#06b6d4"/>
                                            <line x1="118" y1="64" x2="142" y2="45" stroke="#06b6d4" stroke-width="6" stroke-linecap="round" class="entry-arm-r"/>
                                            <circle cx="142" cy="45" r="4.5" fill="#06b6d4"/>
                                        </g>
                                        <line x1="58" y1="38" x2="58" y2="62" stroke="#fbbf24" stroke-width="1" stroke-dasharray="3,2" opacity="0.8"/>
                                        <path d="M 58 50 L 65 48" stroke="#fbbf24" stroke-width="1" opacity="0.8"/>
                                        <circle cx="58" cy="62" r="3" fill="white" opacity="0.6" class="splash1"/>
                                        <circle cx="62" cy="60" r="2" fill="white" opacity="0.4" class="splash2"/>
                                        <circle cx="138" cy="62" r="2.5" fill="white" opacity="0.5" class="splash1"/>
                                        <text x="100" y="108" fill="white" font-size="9" text-anchor="middle">Front View • Above Water</text>
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
                        <button id="checkout-button" class="cta-button">Get Analysis → $4.99</button>
                    </div>
                </section>
            </main>

            <footer>
                <div class="container">
                    <p>© 2026 SwimForm AI · <a href="#">Privacy</a> · <a href="#">Terms</a> · <a href="mailto:support@swimform.ai">support@swimform.ai</a></p>
                </div>
            </footer>
        </div>

        <div id="success-content" style="display: none;">
            <div class="success-page">
                <div class="success-card">
                    <div class="success-icon">🎉</div>
                    <h1>Payment Successful!</h1>
                    <p>Your analysis credit is ready. Click below to upload your swim video.</p>
                    <a id="upload-link" href="#" class="cta-button">Upload Your Video →</a>
                    <p class="success-note">Check your email for a receipt from Stripe</p>
                </div>
            </div>
        </div>

        <script>
            const CONFIG = {{
                PAYMENT_LINK: 'https://buy.stripe.com/test_XXXXX',  // ← REPLACE WITH REAL LINK
                APP_URL: '{APP_BASE_URL}',
            }};
            
            document.getElementById('checkout-button').addEventListener('click', function() {{
                this.disabled = true;
                this.textContent = 'Redirecting to checkout...';
                window.location.href = CONFIG.PAYMENT_LINK;
            }});
            
            const urlParams = new URLSearchParams(window.location.search);
            
            if (urlParams.get('success') === 'true') {{
                document.getElementById('main-content').style.display = 'none';
                document.getElementById('success-content').style.display = 'block';
                document.getElementById('upload-link').href = CONFIG.APP_URL;
            }}
        </script>
    </body>
    </html>
    """

    st.markdown(landing_html, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MAIN ROUTER
# ─────────────────────────────────────────────
query_params = st.query_params

if st.session_state.paid:
    try:
        from pages.two_Dashboard import main as dashboard_main
        dashboard_main()
    except Exception as e:
        st.error(f"Error loading dashboard: {e}")
else:
    success = query_params.get("success", [None])[0] == "true"
    demo    = query_params.get("demo",    [None])[0] == "true"
    cancel  = query_params.get("payment", [None])[0] == "cancel"

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
