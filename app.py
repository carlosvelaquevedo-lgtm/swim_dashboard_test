import streamlit as st
import stripe

# ─────────────────────────────────────────────
# CONFIG & SECRETS
# ─────────────────────────────────────────────
stripe.api_key = st.secrets["stripe"]["secret_key"]
APP_BASE_URL = st.secrets["stripe"].get("base_url", "https://your-app.streamlit.app")

IS_DEV = True

# Session state for payment
if "paid" not in st.session_state:
    st.session_state.paid = False

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
# FULL LANDING PAGE HTML (your new code)
# ─────────────────────────────────────────────
landing_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SwimForm AI - Instant Technique Analysis</title>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Space+Mono:wght@700&display=swap" rel="stylesheet">
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

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'DM Sans', -apple-system, sans-serif;
            background: var(--deep-pool);
            color: var(--bubble-white);
            min-height: 100vh;
            overflow-x: hidden;
        }

        .water-bg {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            z-index: -1;
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
            z-index: -1;
            opacity: 0.03;
            background: repeating-linear-gradient(90deg, var(--lane-line) 0px, var(--lane-line) 4px, transparent 4px, transparent 150px);
        }

        .bubble {
            position: fixed;
            border-radius: 50%;
            background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.4), rgba(6, 182, 212, 0.1));
            animation: float 15s infinite ease-in-out;
            z-index: -1;
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

        .container { max-width: 1100px; margin: 0 auto; padding: 0 24px; }

        header { padding: 20px 0; position: relative; z-index: 10; }

        .logo {
            font-family: 'Space Mono', monospace;
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--surface-glow);
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 10px;
        }

        .hero { padding: 60px 0 80px; text-align: center; }

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

        .hero-badge::before { content: '⚡'; }

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
            margin: 0 auto;
            position: relative;
            overflow: hidden;
            animation: fadeInUp 0.6s ease-out 0.3s both;
        }

        .cta-box::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--surface-glow), transparent);
        }

        .price-tag {
            display: flex;
            align-items: baseline;
            justify-content: center;
            gap: 8px;
            margin-bottom: 8px;
        }

        .price-amount {
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
        }

        .cta-button {
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
        }

        .cta-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 30px rgba(6, 182, 212, 0.5);
        }

        .cta-button:active {
            transform: translateY(0);
        }

        .trust-signals {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 24px;
            font-size: 0.875rem;
            color: rgba(240, 253, 255, 0.6);
        }

        .trust-signal {
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .trust-signal::before {
            content: '✓';
            color: var(--success-green);
            font-weight: 700;
        }

        .features-section {
            padding: 60px 0;
            background: linear-gradient(180deg, transparent 0%, rgba(6, 182, 212, 0.02) 100%);
        }

        .section-title {
            text-align: center;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 48px;
        }

        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 24px;
        }

        .feature {
            background: rgba(15, 40, 71, 0.4);
            border: 1px solid rgba(6, 182, 212, 0.15);
            border-radius: 16px;
            padding: 32px;
            transition: all 0.3s ease;
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

        .feature h3 {
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 12px;
            color: var(--lane-line);
        }

        .feature p {
            color: rgba(240, 253, 255, 0.7);
            line-height: 1.6;
        }

        .video-section {
            padding: 60px 0;
        }

        .demo-section {
            padding: 60px 0;
            background: linear-gradient(180deg, rgba(6, 182, 212, 0.02) 0%, transparent 100%);
        }

        .demo-video-container {
            max-width: 900px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 24px;
        }

        .demo-video-wrapper {
            background: rgba(15, 40, 71, 0.4);
            border: 1px solid rgba(6, 182, 212, 0.15);
            border-radius: 16px;
            padding: 8px;
            min-height: 400px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .demo-video-wrapper iframe {
            width: 100%;
            height: 100%;
            min-height: 400px;
            border-radius: 12px;
        }

        .demo-placeholder {
            text-align: center;
            padding: 60px 40px;
            color: rgba(240, 253, 255, 0.5);
        }

        .demo-placeholder svg {
            margin-bottom: 20px;
            opacity: 0.6;
        }

        .demo-placeholder p {
            font-size: 1.125rem;
            margin-bottom: 8px;
            color: rgba(240, 253, 255, 0.7);
        }

        .demo-instruction {
            font-size: 0.875rem;
            color: rgba(6, 182, 212, 0.6);
            font-style: italic;
        }

        .video-cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 24px;
            margin-bottom: 32px;
        }

        .video-card {
            background: rgba(15, 40, 71, 0.4);
            border: 1px solid rgba(6, 182, 212, 0.15);
            border-radius: 16px;
            padding: 20px;
            transition: all 0.3s ease;
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

        .video-card.recommended:hover {
            border-color: var(--gold-medal);
            box-shadow: 0 8px 24px rgba(251, 191, 36, 0.25);
        }

        .video-preview {
            border-radius: 12px;
            overflow: hidden;
            margin-bottom: 16px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        }

        .video-svg {
            width: 100%;
            height: auto;
            display: block;
        }

        .video-card h3 {
            font-size: 1rem;
            font-weight: 600;
            color: var(--lane-line);
            margin-bottom: 8px;
        }

        .video-metrics {
            font-size: 0.875rem;
            color: rgba(240, 253, 255, 0.6);
            line-height: 1.5;
        }

        .video-tip {
            background: rgba(251, 191, 36, 0.1);
            border: 1px solid rgba(251, 191, 36, 0.3);
            border-radius: 12px;
            padding: 16px 20px;
            font-size: 0.9375rem;
            color: rgba(240, 253, 255, 0.9);
            text-align: center;
        }

        .how-section {
            padding: 60px 0;
            background: linear-gradient(180deg, transparent 0%, rgba(6, 182, 212, 0.02) 100%);
        }

        .steps {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            align-items: center;
            gap: 24px;
        }

        .step {
            flex: 0 1 280px;
            background: rgba(15, 40, 71, 0.4);
            border: 1px solid rgba(6, 182, 212, 0.15);
            border-radius: 16px;
            padding: 32px;
            text-align: center;
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

        .step h3 {
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 12px;
            color: var(--lane-line);
        }

        .step p {
            color: rgba(240, 253, 255, 0.7);
            line-height: 1.6;
        }

        .step-arrow {
            font-size: 1.5rem;
            color: var(--surface-glow);
            flex: 0 0 auto;
        }

        .testimonial-section {
            padding: 60px 0;
        }

        .testimonial-card {
            background: rgba(15, 40, 71, 0.4);
            border: 1px solid rgba(6, 182, 212, 0.15);
            border-radius: 20px;
            padding: 40px;
            max-width: 700px;
            margin: 0 auto;
        }

        .testimonial-stars {
            font-size: 1.5rem;
            color: var(--gold-medal);
            margin-bottom: 20px;
        }

        .testimonial-quote {
            font-size: 1.125rem;
            line-height: 1.7;
            color: rgba(240, 253, 255, 0.9);
            margin-bottom: 24px;
            font-style: italic;
        }

        .testimonial-author {
            display: flex;
            align-items: center;
            gap: 16px;
        }

        .testimonial-avatar {
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
        }

        .testimonial-info h4 {
            font-weight: 600;
            color: var(--lane-line);
            margin-bottom: 4px;
        }

        .testimonial-info p {
            font-size: 0.875rem;
            color: rgba(240, 253, 255, 0.6);
        }

        .final-cta {
            padding: 80px 0;
            text-align: center;
        }

        .final-cta h2 {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 16px;
        }

        .final-cta p {
            font-size: 1.25rem;
            color: rgba(240, 253, 255, 0.7);
            margin-bottom: 32px;
        }

        footer {
            padding: 40px 0;
            border-top: 1px solid rgba(6, 182, 212, 0.1);
            text-align: center;
        }

        footer p {
            color: rgba(240, 253, 255, 0.5);
            font-size: 0.875rem;
        }

        footer a {
            color: var(--surface-glow);
            text-decoration: none;
        }

        footer a:hover {
            text-decoration: underline;
        }

        .success-page {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 24px;
        }

        .success-card {
            background: linear-gradient(135deg, rgba(15, 40, 71, 0.8) 0%, rgba(10, 22, 40, 0.9) 100%);
            border: 1px solid rgba(6, 182, 212, 0.2);
            border-radius: 24px;
            padding: 60px 40px;
            max-width: 500px;
            text-align: center;
        }

        .success-icon {
            font-size: 4rem;
            margin-bottom: 24px;
        }

        .success-card h1 {
            font-size: 2rem;
            margin-bottom: 16px;
        }

        .success-card p {
            color: rgba(240, 253, 255, 0.7);
            margin-bottom: 32px;
        }

        .success-note {
            font-size: 0.875rem;
            color: rgba(240, 253, 255, 0.5);
            margin-top: 24px !important;
        }

        /* Enhanced SVG Animations */
        @keyframes swim-stroke {
            0%, 100% { transform: translateX(0) rotate(0deg); }
            50% { transform: translateX(-8px) rotate(-3deg); }
        }

        @keyframes arm-pull {
            0%, 100% { transform: rotate(0deg); }
            50% { transform: rotate(-15deg); }
        }

        @keyframes bubble-rise {
            0% { transform: translateY(0) scale(1); opacity: 0.6; }
            100% { transform: translateY(-30px) scale(0.5); opacity: 0; }
        }

        @keyframes wave-motion {
            0%, 100% { d: path('M 0 60 Q 50 55 100 60 T 200 60'); }
            50% { d: path('M 0 60 Q 50 65 100 60 T 200 60'); }
        }

        .swimmer-side { animation: swim-stroke 2s ease-in-out infinite; }
        .pull-arm { animation: arm-pull 2s ease-in-out infinite; }
        .splash1 { animation: bubble-rise 1.5s ease-out infinite; }
        .splash2 { animation: bubble-rise 1.5s ease-out 0.3s infinite; }
        .arm-left { animation: arm-pull 2s ease-in-out infinite; }
        .arm-right { animation: arm-pull 2s ease-in-out infinite 1s; }
        .entry-arm-l { animation: arm-pull 2.5s ease-in-out infinite; }
        .entry-arm-r { animation: arm-pull 2.5s ease-in-out infinite 1.25s; }
        .roll-arc { 
            stroke-dashoffset: 100;
            animation: dash 3s linear infinite;
        }
        @keyframes dash {
            to { stroke-dashoffset: 0; }
        }

        @media (max-width: 768px) {
            .steps { flex-direction: column; }
            .step-arrow { transform: rotate(90deg); }
            .trust-signals { flex-direction: column; gap: 12px; }
            .demo-video-container { 
                grid-template-columns: 1fr;
            }
            .demo-video-wrapper {
                min-height: 300px;
            }
            .demo-video-wrapper iframe {
                min-height: 300px;
            }
        }
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
                                Skip Payment – Enter Demo Mode (for testing)
                            </button>
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
                            <div class="demo-placeholder">
                                <svg viewBox="0 0 120 120" width="80" height="80">
                                    <circle cx="60" cy="60" r="55" fill="none" stroke="rgba(6, 182, 212, 0.3)" stroke-width="2"/>
                                    <circle cx="60" cy="60" r="45" fill="rgba(6, 182, 212, 0.1)"/>
                                    <path d="M 50 40 L 50 80 L 80 60 Z" fill="#06b6d4"/>
                                </svg>
                                <p>Add your Loom demo video here</p>
                                <span class="demo-instruction">See HTML comments above for instructions</span>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <section class="video-section">
                <div class="container">
                    <h2 class="section-title">Best camera angles</h2>
                    <div class="video-cards">
                        <!-- Your SVG cards here (Side View Underwater, etc.) - paste the full <div class="video-card"> blocks -->
                        <!-- I omitted them here for brevity, but include all 4 from your code -->
                    </div>

                    <p class="video-tip">💡 <strong>Tip:</strong> 10-15 seconds of continuous swimming works best. Our AI auto-detects your camera angle!</p>
                </div>
            </section>

            <section class="how-section">
                <div class="container">
                    <h2 class="section-title">How it works</h2>
                    <div class="steps">
                        <!-- Your 3 step divs here -->
                        <!-- Paste the full <div class="step"> blocks -->
                    </div>
                </div>
            </section>

            <section class="testimonial-section">
                <div class="container">
                    <!-- Your testimonial card here -->
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
        const CONFIG = {
            PAYMENT_LINK: 'https://buy.stripe.com/test_XXXXX',  # ← YOUR STRIPE PAYMENT LINK
            APP_URL: '""" + APP_BASE_URL + """',  # ← Your app URL
        };
        
        document.getElementById('checkout-button').addEventListener('click', function() {
            this.disabled = true;
            this.textContent = 'Redirecting to checkout...';
            window.location.href = CONFIG.PAYMENT_LINK;
        });
        
        const urlParams = new URLSearchParams(window.location.search);
        
        if (urlParams.get('success') === 'true') {
            document.getElementById('main-content').style.display = 'none';
            document.getElementById('success-content').style.display = 'block';
            document.getElementById('upload-link').href = CONFIG.APP_URL;
        }
    </script>
</body>
</html>
    """

    st.markdown(landing_html, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ROUTER
# ─────────────────────────────────────────────
if st.session_state.paid:
    # Run dashboard (your analyzer)
    from pages.two_Dashboard import main as dashboard_main
    dashboard_main()

else:
    # Handle success redirect
    query_params = st.query_params   # ← don't forget this line!

    if query_params.get("success", [None])[0] == "true":
        st.session_state.paid = True
        st.success("Payment successful! Loading dashboard...")
        st.balloons()
        st.query_params.clear()
        st.rerun()

    elif query_params.get("demo", [None])[0] == "true":
        st.session_state.paid = True
        st.info("Demo mode activated — full access granted for testing!")
        st.query_params.clear()
        st.rerun()

    elif query_params.get("payment", [None])[0] == "cancel":
        st.warning("Payment cancelled. You can try again.")
        st.query_params.clear()

    # ← Landing page should be shown when NOT paid (including after handling query params)
    st.markdown(landing_html, unsafe_allow_html=True)
