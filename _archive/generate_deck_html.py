#!/usr/bin/env python3
"""
Generate SLASHR HTML presentation deck for Ahold Delhaize / Carlos Vicente.
Premium dark-first design, full brand system, self-contained single file.
"""
import base64, os

# Read images as base64
def img_to_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_b64 = img_to_b64("/Users/quentin/Desktop/LOGO-SLASHR-BLANC-1.png")
janus_b64 = img_to_b64("/Users/quentin/Downloads/iPhone-13-PRO-MAX-janus.agence-slashr.fr.png")

html = f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SLASHR - Presentation Ahold Delhaize</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Funnel+Display:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
/* ===== RESET & BASE ===== */
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
:root {{
  --orange: #E74601;
  --magenta: #CE08A9;
  --violet: #8962FD;
  --bg: #1a1a1a;
  --surface: #2C2E34;
  --surface-alt: #25272E;
  --white: #ffffff;
  --white-90: rgba(255,255,255,0.9);
  --white-70: rgba(255,255,255,0.7);
  --white-50: rgba(255,255,255,0.5);
  --white-30: rgba(255,255,255,0.3);
  --white-15: rgba(255,255,255,0.15);
  --white-10: rgba(255,255,255,0.1);
  --white-05: rgba(255,255,255,0.05);
  --gradient: linear-gradient(135deg, #E74601, #CE08A9, #8962FD);
  --gradient-h: linear-gradient(90deg, #E74601, #CE08A9, #8962FD);
  --font-display: 'Funnel Display', 'Sora', 'DM Sans', sans-serif;
  --font-body: 'Inter', -apple-system, 'Segoe UI', sans-serif;
  --radius: 16px;
  --radius-sm: 10px;
  --radius-lg: 24px;
  --max-w: 1200px;
  --slide-h: 100vh;
}}

html {{ height: 100%; scroll-behavior: smooth; }}
body {{
  height: 100%;
  background: var(--bg);
  color: var(--white);
  font-family: var(--font-body);
  overflow: hidden;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}}

/* ===== SCROLL CONTAINER ===== */
.deck {{
  height: 100vh;
  overflow-y: auto;
  scroll-snap-type: y proximity;
  scroll-behavior: smooth;
}}

/* ===== SLIDE ===== */
.slide {{
  min-height: var(--slide-h);
  scroll-snap-align: start;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 60px 40px;
  position: relative;
  overflow: hidden;
}}
.slide .inner {{
  max-width: var(--max-w);
  margin: 0 auto;
  width: 100%;
  position: relative;
  z-index: 2;
}}

/* ===== HERO BLOBS ===== */
.blobs {{
  position: absolute;
  inset: 0;
  z-index: 0;
  overflow: hidden;
  pointer-events: none;
}}
.blobs .blob {{
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.18;
  transform: translateZ(0);
  backface-visibility: hidden;
}}
.blobs .b-orange {{ background: linear-gradient(239deg, #E74601 43%, #FF9011 71%); width: 500px; height: 500px; bottom: -15%; left: -5%; }}
.blobs .b-magenta {{ background: linear-gradient(239deg, #CE08A9 43%, #CE16B5 71%); width: 650px; height: 450px; bottom: -5%; left: 25%; }}
.blobs .b-violet {{ background: linear-gradient(180deg, #8962FD, #AD21FE); width: 500px; height: 550px; bottom: -10%; right: -5%; }}

/* Top positioned variant */
.blobs-top .b-orange {{ bottom: auto; top: -15%; }}
.blobs-top .b-magenta {{ bottom: auto; top: -5%; }}
.blobs-top .b-violet {{ bottom: auto; top: -10%; }}

/* Subtle variant */
.blobs-subtle .blob {{ opacity: 0.08; }}

/* ===== NAV BAR ===== */
.nav {{
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  padding: 16px 40px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  background: rgba(26,26,26,0.7);
  border-bottom: 1px solid var(--white-10);
}}
.nav .logo {{ height: 24px; opacity: 0.9; }}
.nav .nav-right {{
  display: flex;
  align-items: center;
  gap: 20px;
  font-size: 12px;
  color: var(--white-50);
  letter-spacing: 0.05em;
}}
.nav .slide-counter {{
  font-variant-numeric: tabular-nums;
  font-weight: 600;
  color: var(--white-70);
}}

/* ===== PROGRESS BAR ===== */
.progress {{
  position: fixed;
  top: 56px;
  left: 0;
  height: 2px;
  background: var(--gradient-h);
  z-index: 101;
  transition: width 0.3s ease;
  width: 0%;
}}

/* ===== TYPOGRAPHY ===== */
.display-xl {{
  font-family: var(--font-display);
  font-size: clamp(48px, 7vw, 88px);
  font-weight: 700;
  line-height: 0.95;
  letter-spacing: -0.03em;
}}
.display-l {{
  font-family: var(--font-display);
  font-size: clamp(36px, 5vw, 64px);
  font-weight: 700;
  line-height: 0.95;
  letter-spacing: -0.03em;
}}
.heading {{
  font-family: var(--font-display);
  font-size: clamp(28px, 4vw, 44px);
  font-weight: 700;
  line-height: 1.05;
  letter-spacing: -0.03em;
}}
.title {{ font-size: 20px; font-weight: 700; line-height: 1.3; letter-spacing: -0.01em; }}
.subtitle {{ font-size: 18px; font-weight: 500; line-height: 1.4; }}
.body {{ font-size: 16px; font-weight: 400; line-height: 1.55; color: var(--white-70); }}
.body-sm {{ font-size: 14px; font-weight: 400; line-height: 1.5; color: var(--white-70); }}
.caption {{ font-size: 12px; font-weight: 500; line-height: 1.4; color: var(--white-50); }}
.tag {{
  display: inline-block;
  padding: 6px 16px;
  background: var(--surface);
  border-radius: 100px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--white-50);
  border: 1px solid var(--white-10);
}}
.gradient-text {{
  background: var(--gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}}
.accent {{ color: var(--orange); }}
.accent-m {{ color: var(--magenta); }}
.accent-v {{ color: var(--violet); }}

/* ===== ACCENT BAR ===== */
.accent-bar {{
  width: 48px;
  height: 3px;
  background: var(--gradient-h);
  border-radius: 2px;
  margin-bottom: 20px;
}}

/* ===== CARDS ===== */
.card {{
  background: var(--surface);
  border: 1px solid var(--white-10);
  border-radius: var(--radius);
  padding: 28px;
  transition: border-color 0.3s, transform 0.3s;
}}
.card:hover {{
  border-color: var(--white-15);
  transform: scale(1.015);
}}
.card-accent-top {{
  position: relative;
  overflow: hidden;
}}
.card-accent-top::before {{
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
}}
.card-accent-top.a-orange::before {{ background: var(--orange); }}
.card-accent-top.a-magenta::before {{ background: var(--magenta); }}
.card-accent-top.a-violet::before {{ background: var(--violet); }}
.card-accent-top.a-gradient::before {{ background: var(--gradient-h); }}

/* ===== GRID LAYOUTS ===== */
.grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }}
.grid-3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }}
.grid-4 {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }}
.grid-5 {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 16px; }}
.grid-2-1 {{ display: grid; grid-template-columns: 2fr 1fr; gap: 32px; align-items: center; }}
.grid-1-1 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 40px; align-items: start; }}

/* ===== SPECIFIC COMPONENTS ===== */
.kpi-card {{
  text-align: center;
  padding: 24px 16px;
}}
.kpi-num {{
  font-family: var(--font-display);
  font-size: 36px;
  font-weight: 700;
  letter-spacing: -0.02em;
  margin-bottom: 4px;
}}
.kpi-label {{ font-size: 14px; font-weight: 600; margin-bottom: 2px; }}
.kpi-sub {{ font-size: 12px; color: var(--white-50); }}

.team-card {{
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
}}
.team-avatar {{
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: var(--surface-alt);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
  flex-shrink: 0;
  border: 1px solid var(--white-10);
}}
.team-avatar.founder {{
  width: 56px;
  height: 56px;
  font-size: 16px;
  border-color: var(--orange);
  background: rgba(231,70,1,0.1);
  color: var(--orange);
}}
.team-info .name {{ font-weight: 700; font-size: 15px; }}
.team-info .role {{ font-size: 13px; color: var(--white-50); margin-top: 2px; }}

.case-result {{
  text-align: center;
  padding: 20px;
}}
.case-result .num {{
  font-family: var(--font-display);
  font-size: 32px;
  font-weight: 700;
  color: var(--orange);
  letter-spacing: -0.02em;
}}
.case-result .label {{
  font-size: 12px;
  color: var(--white-50);
  margin-top: 4px;
  line-height: 1.3;
}}
.verbatim {{
  font-style: italic;
  color: var(--white-50);
  font-size: 14px;
  line-height: 1.5;
  padding-left: 20px;
  border-left: 2px solid var(--orange);
  margin-top: 24px;
}}
.verbatim .author {{ font-style: normal; font-weight: 600; color: var(--white-30); margin-top: 6px; }}

.section-label {{
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--white-50);
  margin-bottom: 12px;
}}

.vs-card {{
  padding: 32px;
}}
.vs-card.dimmed {{ opacity: 0.5; }}
.vs-card .quote {{
  font-size: 18px;
  font-weight: 500;
  line-height: 1.4;
  margin: 16px 0;
}}

.diff-card {{ padding: 20px 24px; }}
.diff-card .diff-title {{
  font-size: 14px;
  font-weight: 700;
  color: var(--orange);
  margin-bottom: 6px;
}}
.diff-card .diff-desc {{
  font-size: 13px;
  color: var(--white-50);
  line-height: 1.4;
}}

.step-number {{
  font-family: var(--font-display);
  font-size: 48px;
  font-weight: 700;
  letter-spacing: -0.02em;
  margin-bottom: 8px;
}}
.step-title {{
  font-size: 18px;
  font-weight: 800;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin-bottom: 12px;
}}
.step-desc {{
  font-size: 14px;
  color: var(--white-70);
  line-height: 1.6;
}}

.phase-card {{
  padding: 32px;
}}
.phase-badge {{
  display: inline-block;
  padding: 4px 14px;
  border-radius: 100px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin-bottom: 12px;
}}
.phase-badge.p1 {{ background: rgba(231,70,1,0.15); color: var(--orange); }}
.phase-badge.p2 {{ background: rgba(206,8,169,0.15); color: var(--magenta); }}

.phase-list {{ list-style: none; margin-top: 16px; }}
.phase-list li {{
  padding: 8px 0;
  font-size: 14px;
  color: var(--white-70);
  display: flex;
  align-items: flex-start;
  gap: 10px;
  line-height: 1.4;
}}
.phase-list li::before {{
  content: '';
  width: 6px;
  height: 6px;
  border-radius: 50%;
  flex-shrink: 0;
  margin-top: 7px;
}}
.phase-list.p1 li::before {{ background: var(--orange); }}
.phase-list.p2 li::before {{ background: var(--magenta); }}

.ref-card {{
  padding: 20px 24px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}}
.ref-card .ref-name {{ font-weight: 700; font-size: 15px; }}
.ref-card .ref-desc {{ font-size: 12px; color: var(--white-50); line-height: 1.3; }}

.janus-mockup {{
  max-height: 500px;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.5);
}}

.value-card {{
  padding: 32px 28px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}}
.value-num {{
  font-family: var(--font-display);
  font-size: 28px;
  font-weight: 700;
  letter-spacing: -0.02em;
}}
.value-title {{
  font-size: 18px;
  font-weight: 700;
}}
.value-desc {{
  font-size: 13px;
  color: var(--white-70);
  line-height: 1.55;
}}

/* ===== HERO SPECIFIC ===== */
.hero {{ justify-content: center; min-height: 100vh; }}
.hero .tag {{ margin-bottom: 24px; }}
.hero .display-xl {{ margin-bottom: 20px; }}
.hero .subtitle {{ color: var(--white-50); }}

/* ===== CTA SLIDE ===== */
.cta-slide {{ text-align: center; }}
.cta-slide .display-l {{ margin-bottom: 16px; }}
.cta-slide .gradient-bar {{
  width: 120px;
  height: 3px;
  background: var(--gradient-h);
  border-radius: 2px;
  margin: 32px auto;
}}
.cta-slide .cta-text {{
  font-size: 22px;
  font-weight: 600;
  margin-bottom: 16px;
}}
.cta-slide .contact {{
  font-size: 15px;
  color: var(--white-50);
}}

/* ===== FOOTER TAG ===== */
.slide-footer {{
  position: absolute;
  bottom: 20px;
  left: 40px;
  right: 40px;
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  color: var(--white-30);
  z-index: 2;
}}

/* ===== SPACERS ===== */
.mt-8 {{ margin-top: 8px; }}
.mt-12 {{ margin-top: 12px; }}
.mt-16 {{ margin-top: 16px; }}
.mt-20 {{ margin-top: 20px; }}
.mt-24 {{ margin-top: 24px; }}
.mt-32 {{ margin-top: 32px; }}
.mt-40 {{ margin-top: 40px; }}
.mt-48 {{ margin-top: 48px; }}
.mb-8 {{ margin-bottom: 8px; }}
.mb-12 {{ margin-bottom: 12px; }}
.mb-16 {{ margin-bottom: 16px; }}
.mb-24 {{ margin-bottom: 24px; }}
.gap-32 {{ gap: 32px; }}
.gap-40 {{ gap: 40px; }}

/* ===== ANIMATIONS ===== */
@keyframes fadeInUp {{
  from {{ opacity: 0; transform: translateY(30px); }}
  to {{ opacity: 1; transform: translateY(0); }}
}}
.slide .inner > * {{
  opacity: 0;
  animation: fadeInUp 0.6s ease forwards;
}}
.slide .inner > *:nth-child(1) {{ animation-delay: 0.1s; }}
.slide .inner > *:nth-child(2) {{ animation-delay: 0.2s; }}
.slide .inner > *:nth-child(3) {{ animation-delay: 0.3s; }}
.slide .inner > *:nth-child(4) {{ animation-delay: 0.4s; }}
.slide .inner > *:nth-child(5) {{ animation-delay: 0.5s; }}
.slide .inner > *:nth-child(6) {{ animation-delay: 0.6s; }}

/* Re-trigger on scroll via IntersectionObserver */
.slide:not(.visible) .inner > * {{ opacity: 0; animation: none; }}
.slide.visible .inner > * {{ animation: fadeInUp 0.6s ease forwards; }}

/* ===== RESPONSIVE ===== */
@media (max-width: 900px) {{
  .grid-4 {{ grid-template-columns: repeat(2, 1fr); }}
  .grid-5 {{ grid-template-columns: repeat(3, 1fr); }}
  .grid-3 {{ grid-template-columns: 1fr; }}
  .grid-2-1 {{ grid-template-columns: 1fr; }}
  .grid-1-1 {{ grid-template-columns: 1fr; }}
  .slide {{ padding: 40px 24px; }}
}}

/* ===== PRINT ===== */
@media print {{
  .nav, .progress {{ display: none !important; }}
  .deck {{ overflow: visible; height: auto; }}
  .slide {{ min-height: auto; page-break-after: always; padding: 30px; }}
  .blobs {{ display: none; }}
  body {{ background: #fff; color: #1a1a1a; }}
  .card {{ border-color: #ddd; background: #f5f5f5; }}
  .body, .body-sm, .step-desc, .value-desc {{ color: #333; }}
}}
</style>
</head>
<body>

<!-- NAV -->
<nav class="nav">
  <img src="data:image/png;base64,{logo_b64}" alt="SLASHR" class="logo">
  <div class="nav-right">
    <span>AHOLD DELHAIZE</span>
    <span>|</span>
    <span>AVRIL 2026</span>
    <span>|</span>
    <span class="slide-counter"><span id="current-slide">1</span> / <span id="total-slides">16</span></span>
  </div>
</nav>
<div class="progress" id="progress"></div>

<!-- DECK -->
<div class="deck" id="deck">

  <!-- ============ SLIDE 1 - HERO ============ -->
  <section class="slide hero" id="slide-1">
    <div class="blobs">
      <div class="blob b-orange"></div>
      <div class="blob b-magenta"></div>
      <div class="blob b-violet"></div>
    </div>
    <div class="inner">
      <span class="tag">AGENCE SEARCH MARKETING</span>
      <h1 class="display-xl">Prenez le contrôle<br>du Search.</h1>
      <p class="subtitle mt-20">Présentation à Carlos Vicente &nbsp;|&nbsp; Ahold Delhaize &nbsp;|&nbsp; Avril 2026</p>
    </div>
    <div class="slide-footer">
      <span>SLASHR &nbsp;|&nbsp; Confidentiel</span>
      <span>01</span>
    </div>
  </section>

  <!-- ============ SLIDE 2 - LE SEARCH A CHANGE ============ -->
  <section class="slide" id="slide-2">
    <div class="blobs blobs-subtle blobs-top">
      <div class="blob b-violet"></div>
    </div>
    <div class="inner">
      <div class="accent-bar"></div>
      <h2 class="heading">Le Search a changé.</h2>
      <p class="body mt-16" style="max-width: 700px;">Les algorithmes évoluent, l'IA redistribue les cartes, les comportements de recherche se fragmentent. Ce qui fonctionnait il y a deux ans ne fonctionne plus.</p>
      <div class="grid-4 mt-40">
        <div class="card card-accent-top a-orange">
          <div class="title accent mb-8">Google</div>
          <p class="body-sm">Toujours dominant. Mais les pages de résultats se transforment, les AI Overviews redistribuent les clics et la visibilité se joue autrement.</p>
        </div>
        <div class="card card-accent-top a-magenta">
          <div class="title accent-m mb-8">IA générative</div>
          <p class="body-sm">ChatGPT, Claude, Gemini, Perplexity - vos clients leur posent des questions. Êtes-vous dans les réponses ?</p>
        </div>
        <div class="card card-accent-top a-violet">
          <div class="title accent-v mb-8">Social Search</div>
          <p class="body-sm">TikTok, YouTube, Instagram sont devenus des moteurs de recherche. Les jeunes y cherchent avant Google.</p>
        </div>
        <div class="card card-accent-top a-orange">
          <div class="title accent mb-8">Zero-click</div>
          <p class="body-sm">60% des recherches Google n'aboutissent plus à un clic. La visibilité se joue au-delà du lien bleu.</p>
        </div>
      </div>
    </div>
    <div class="slide-footer">
      <span>SLASHR &nbsp;|&nbsp; Confidentiel</span>
      <span>02</span>
    </div>
  </section>


  <!-- ============ SLIDE 3 - CE QU'ON VOIT CHEZ DELHAIZE ============ -->
  <section class="slide" id="slide-3">
    <div class="blobs blobs-subtle">
      <div class="blob b-orange" style="left: -10%; bottom: -20%;"></div>
    </div>
    <div class="inner">
      <div class="accent-bar"></div>
      <h2 class="heading">Ce qu'on voit chez Delhaize.</h2>
      <p class="body mt-16" style="max-width: 700px;">Avant de parler de nous, on a regardé votre situation. Voici les enjeux Search qu'on identifie pour un acteur comme Delhaize.</p>
      <div class="grid-3 mt-40 gap-32">
        <div class="card card-accent-top a-orange" style="padding: 28px;">
          <div class="title accent mb-12">Multi-pays, multi-marques</div>
          <p class="body-sm">Delhaize, Albert Heijn, Food Lion, Hannaford... Chaque marché a ses spécificités Search. La stratégie doit être cohérente au niveau groupe et exécutée localement.</p>
        </div>
        <div class="card card-accent-top a-magenta" style="padding: 28px;">
          <div class="title accent-m mb-12">SEO local à grande échelle</div>
          <p class="body-sm">800+ magasins. Les requêtes "supermarché + ville", "promotions + enseigne" sont un levier d'acquisition massif. Chaque point de vente est une opportunité de visibilité.</p>
        </div>
        <div class="card card-accent-top a-violet" style="padding: 28px;">
          <div class="title accent-v mb-12">E-commerce alimentaire</div>
          <p class="body-sm">Le drive et la livraison accélèrent. Les intentions de recherche produit évoluent. Les IA commencent à recommander des enseignes. Êtes-vous dans les réponses ?</p>
        </div>
      </div>
      <div class="card mt-24" style="padding: 20px 28px; border-color: rgba(231,70,1,0.2);">
        <p class="body" style="color: var(--white-90);">On ne prétend pas connaître votre business mieux que vous. Mais on sait lire les données Search d'un marché. Et ce qu'on voit, c'est du potentiel inexploité sur les requêtes hors-marque, le local et la visibilité IA.</p>
      </div>
    </div>
    <div class="slide-footer">
      <span>SLASHR &nbsp;|&nbsp; Confidentiel</span>
      <span>03</span>
    </div>
  </section>

  <!-- ============ SLIDE 4 - SLASHR EN BREF ============ -->
  <section class="slide" id="slide-4">
    <div class="inner">
      <div class="accent-bar"></div>
      <h2 class="heading">SLASHR en bref.</h2>
      <p class="body mt-16" style="max-width: 750px;">On rend les marques visibles là où leurs clients cherchent. Google, ChatGPT, TikTok, YouTube. On analyse les données du marché pour savoir où investir.</p>
      <div class="grid-5 mt-40">
        <div class="card kpi-card">
          <div class="kpi-num accent">2021</div>
          <div class="kpi-label">Fondation</div>
          <div class="kpi-sub">à Lille</div>
        </div>
        <div class="card kpi-card">
          <div class="kpi-num accent">8</div>
          <div class="kpi-label">Collaborateurs</div>
          <div class="kpi-sub">dont 3 associés</div>
        </div>
        <div class="card kpi-card">
          <div class="kpi-num accent">~30</div>
          <div class="kpi-label">Clients</div>
          <div class="kpi-sub">actifs</div>
        </div>
        <div class="card kpi-card">
          <div class="kpi-num accent">+60%</div>
          <div class="kpi-label">Croissance</div>
          <div class="kpi-sub">annuelle</div>
        </div>
        <div class="card kpi-card">
          <div class="kpi-num accent">19</div>
          <div class="kpi-label">Outils</div>
          <div class="kpi-sub">propriétaires</div>
        </div>
      </div>
      <div class="mt-40" style="text-align: center;">
        <p class="caption mb-12">ILS NOUS FONT CONFIANCE</p>
        <p class="body" style="color: var(--white-50);">Vestiaire Collective &nbsp;&middot;&nbsp; Carter Cash &nbsp;&middot;&nbsp; Decathlon &nbsp;&middot;&nbsp; Cofidis Belgique &nbsp;&middot;&nbsp; Le Fourgon &nbsp;&middot;&nbsp; Somfy &nbsp;&middot;&nbsp; SKEMA &nbsp;&middot;&nbsp; EDHEC &nbsp;&middot;&nbsp; Agryco &nbsp;&middot;&nbsp; Ateliers Vanderschooten</p>
      </div>
    </div>
    <div class="slide-footer">
      <span>SLASHR &nbsp;|&nbsp; Confidentiel</span>
      <span>04</span>
    </div>
  </section>

  <!-- ============ SLIDE 5 - CE QU'ON EST / N'EST PAS ============ -->
  <section class="slide" id="slide-5">
    <div class="inner">
      <div class="accent-bar"></div>
      <h2 class="heading">Ce qu'on est.<br>Ce qu'on n'est pas.</h2>
      <div class="grid-2 mt-40 gap-32">
        <div class="card" style="border-color: rgba(231,70,1,0.3);">
          <div class="title accent mb-16">SLASHR est</div>
          <div style="display: flex; flex-direction: column; gap: 14px;">
            <div style="display: flex; align-items: flex-start; gap: 12px;">
              <span style="color: var(--orange); font-size: 18px; line-height: 1.2;">&#10003;</span>
              <span class="body-sm" style="color: var(--white-90);">Une agence Search Marketing stratégique</span>
            </div>
            <div style="display: flex; align-items: flex-start; gap: 12px;">
              <span style="color: var(--orange); font-size: 18px; line-height: 1.2;">&#10003;</span>
              <span class="body-sm" style="color: var(--white-90);">Stratèges et praticiens : on conçoit et on exécute</span>
            </div>
            <div style="display: flex; align-items: flex-start; gap: 12px;">
              <span style="color: var(--orange); font-size: 18px; line-height: 1.2;">&#10003;</span>
              <span class="body-sm" style="color: var(--white-90);">Des explorateurs qui testent avant de recommandér</span>
            </div>
            <div style="display: flex; align-items: flex-start; gap: 12px;">
              <span style="color: var(--orange); font-size: 18px; line-height: 1.2;">&#10003;</span>
              <span class="body-sm" style="color: var(--white-90);">Agiles et disponibles : la réactivité d'une équipe dédiée</span>
            </div>
            <div style="display: flex; align-items: flex-start; gap: 12px;">
              <span style="color: var(--orange); font-size: 18px; line-height: 1.2;">&#10003;</span>
              <span class="body-sm" style="color: var(--white-90);">Taille humaine, expertise pointue : pas de couches, un accès direct aux experts</span>
            </div>
          </div>
        </div>
        <div class="card" style="opacity: 0.6;">
          <div class="title mb-16" style="color: var(--white-50);">SLASHR n'est pas</div>
          <div style="display: flex; flex-direction: column; gap: 14px;">
            <div style="display: flex; align-items: flex-start; gap: 12px;">
              <span style="color: var(--white-30); font-size: 18px; line-height: 1.2;">&#10007;</span>
              <span class="body-sm" style="color: var(--white-50);">Une agence SEO qui vend des positions Google</span>
            </div>
            <div style="display: flex; align-items: flex-start; gap: 12px;">
              <span style="color: var(--white-30); font-size: 18px; line-height: 1.2;">&#10007;</span>
              <span class="body-sm" style="color: var(--white-50);">Un prestataire qui deroule des audits génériques</span>
            </div>
            <div style="display: flex; align-items: flex-start; gap: 12px;">
              <span style="color: var(--white-30); font-size: 18px; line-height: 1.2;">&#10007;</span>
              <span class="body-sm" style="color: var(--white-50);">Un vendeur de promesses déconnectées de la data</span>
            </div>
            <div style="display: flex; align-items: flex-start; gap: 12px;">
              <span style="color: var(--white-30); font-size: 18px; line-height: 1.2;">&#10007;</span>
              <span class="body-sm" style="color: var(--white-50);">Un one-size-fits-all qui force le multicanal</span>
            </div>
            <div style="display: flex; align-items: flex-start; gap: 12px;">
              <span style="color: var(--white-30); font-size: 18px; line-height: 1.2;">&#10007;</span>
              <span class="body-sm" style="color: var(--white-50);">Un fournisseur de contenu a la chaîne</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="slide-footer">
      <span>SLASHR &nbsp;|&nbsp; Confidentiel</span>
      <span>05</span>
    </div>
  </section>

  <!-- ============ SLIDE 6 - VALEURS ============ -->
  <section class="slide" id="slide-6">
    <div class="inner">
      <div class="accent-bar"></div>
      <h2 class="heading">Nos 4 valeurs.</h2>
      <div class="grid-4 mt-40">
        <div class="card value-card card-accent-top a-orange">
          <div class="value-num accent">01</div>
          <div class="value-title">Curiosité</div>
          <p class="value-desc">On remet en question, on creuse, on teste sur nos propres sites avant de recommandér. Notre avantage : ne jamais arrêter d'apprendre.</p>
        </div>
        <div class="card value-card card-accent-top a-magenta">
          <div class="value-num accent-m">02</div>
          <div class="value-title">Audace</div>
          <p class="value-desc">On ose dire ce qu'on pense, meme quand ca dérange. 90 jours au lieu de 12 mois d'engagement. Conviction argumentée plutôt que consensus mou.</p>
        </div>
        <div class="card value-card card-accent-top a-violet">
          <div class="value-num accent-v">03</div>
          <div class="value-title">Impact</div>
          <p class="value-desc">Pas de théorie sans résultat. Chaque recommandation est adossée à une donnée, chaque action est mesurable. On vise le résultat.</p>
        </div>
        <div class="card value-card card-accent-top a-gradient">
          <div class="value-num gradient-text">04</div>
          <div class="value-title">Transparence</div>
          <p class="value-desc">On partage nos hypothèses, nos projections et nos limites. Le client voit les mêmes chiffres que nous. Le ROI est conditionnel.</p>
        </div>
      </div>
    </div>
    <div class="slide-footer">
      <span>SLASHR &nbsp;|&nbsp; Confidentiel</span>
      <span>06</span>
    </div>
  </section>

  <!-- ============ SLIDE 7 - METHODE ============ -->
  <section class="slide" id="slide-7">
    <div class="inner">
      <div class="accent-bar"></div>
      <h2 class="heading">Notre méthode.</h2>
      <p class="body mt-16">Trois temps, toujours dans cet ordre.</p>
      <div class="grid-3 mt-40 gap-32">
        <div class="card card-accent-top a-orange" style="padding: 36px 28px;">
          <div class="step-number accent">01</div>
          <div class="step-title accent">Analyser</div>
          <p class="step-desc">Comprendre le marché, les intentions de recherche et les opportunités. Décrypter avant de décider.</p>
          <p class="step-desc mt-12">Cartographie complète de votre marché Search. Pas un échantillon - l'exhaustivité.</p>
        </div>
        <div class="card card-accent-top a-magenta" style="padding: 36px 28px;">
          <div class="step-number accent-m">02</div>
          <div class="step-title accent-m">Prioriser</div>
          <p class="step-desc">Selectionner les bons leviers selon le marché, la maturité de la marque et les moyens. Dire non a ce qui ne sert pas.</p>
          <p class="step-desc mt-12">On ne travaille pas tout en meme temps. On concentre les ressources sur ce qui débloque le plus de valeur.</p>
        </div>
        <div class="card card-accent-top a-violet" style="padding: 36px 28px;">
          <div class="step-number accent-v">03</div>
          <div class="step-title accent-v">Executer</div>
          <p class="step-desc">Déployer, mesurer, ajuster. Des recommandations actionnables, des résultats traçables, un bilan honnête.</p>
          <p class="step-desc mt-12">Quick wins à 90 jours. Bilan sur données réelles. On continue, on ajuste ou on arrête.</p>
        </div>
      </div>
    </div>
    <div class="slide-footer">
      <span>SLASHR &nbsp;|&nbsp; Confidentiel</span>
      <span>07</span>
    </div>
  </section>

  <!-- ============ SLIDE 8 - PERIMETRE / 4 PILIERS ============ -->
  <section class="slide" id="slide-8">
    <div class="blobs blobs-subtle">
      <div class="blob b-orange" style="left: -10%; bottom: -20%;"></div>
      <div class="blob b-violet" style="right: -10%; bottom: -10%;"></div>
    </div>
    <div class="inner">
      <div class="accent-bar"></div>
      <h2 class="heading">Le Search, au complet.</h2>
      <p class="body mt-16" style="max-width: 700px;">On ne fait pas "juste du SEO". On orchestre votre visibilité sur l'ensemble des plateformes de recherche. Le périmètre s'adapte a votre besoin.</p>
      <div class="grid-4 mt-40">
        <div class="card card-accent-top a-orange" style="padding: 32px 24px;">
          <div style="font-size: 32px; margin-bottom: 12px;">&#x1F50D;</div>
          <div class="title accent mb-8">SEO</div>
          <p class="body-sm">Stratégie d'acquisition organique. Audit, architecture, contenu, technique, link building. Le socle de la visibilité durable.</p>
          <div class="caption mt-16">Audit &middot; Architecture &middot; Contenu &middot; Technique</div>
        </div>
        <div class="card card-accent-top a-magenta" style="padding: 32px 24px;">
          <div style="font-size: 32px; margin-bottom: 12px;">&#x1F4B0;</div>
          <div class="title accent-m mb-8">Ads / SEA</div>
          <p class="body-sm">Google Ads, Shopping, PMax, Meta Ads. Audit de compte, restructuration, pilotage continu. Synergie SEO/SEA pour maximiser le ROI.</p>
          <div class="caption mt-16">Audit &middot; Structure &middot; Enchères &middot; PMax</div>
        </div>
        <div class="card card-accent-top a-violet" style="padding: 32px 24px;">
          <div style="font-size: 32px; margin-bottom: 12px;">&#x1F916;</div>
          <div class="title accent-v mb-8">GEO / IA</div>
          <p class="body-sm">Visibilité dans ChatGPT, Claude, Gemini, Perplexity. Monitoring avec Janus. Données structurées et AI Search readiness.</p>
          <div class="caption mt-16">Monitoring &middot; Structured Data &middot; E-E-A-T</div>
        </div>
        <div class="card card-accent-top a-gradient" style="padding: 32px 24px;">
          <div style="font-size: 32px; margin-bottom: 12px;">&#x1F4F1;</div>
          <div class="title mb-8">Social Search</div>
          <p class="body-sm">TikTok, YouTube, Instagram comme moteurs de recherche. Stratégie de présence, optimisation des contenus pour la découverte.</p>
          <div class="caption mt-16">TikTok &middot; YouTube &middot; Instagram</div>
        </div>
      </div>
      <p class="body-sm mt-24" style="text-align: center; color: var(--white-50);">Le périmètre suit le besoin du client. Si vous avez besoin de SEO + Ads, on fait SEO + Ads. Pas besoin de tout activer.</p>
    </div>
    <div class="slide-footer">
      <span>SLASHR &nbsp;|&nbsp; Confidentiel</span>
      <span>08</span>
    </div>
  </section>

  <!-- ============ SLIDE 9 - ENGAGEMENT ============ -->
  <section class="slide" id="slide-9">
    <div class="inner">
      <div class="accent-bar"></div>
      <h2 class="heading">Modèle d'engagement.</h2>
      <p class="body mt-16">Vous restez parce que ca marché, pas parce qu'un contrat vous y oblige.</p>
      <div class="grid-2 mt-40 gap-32">
        <div class="card phase-card card-accent-top a-orange">
          <span class="phase-badge p1">Phase 1</span>
          <div class="title mt-8">Mission structurante</div>
          <p class="body-sm mt-8" style="color: var(--white-50);">90 jours &nbsp;|&nbsp; Ponctuelle</p>
          <ul class="phase-list p1">
            <li>Audit SEO : cartographie complète du marché Search</li>
            <li>Benchmark : analyse des concurrents directs</li>
            <li>Architecture : arborescence et maillage optimisés</li>
            <li>Contenus : spécification des pages piliers</li>
            <li>Ads : audit compte, restructuration, stratégie d'enchères</li>
            <li>Quick wins : premiers gains à 90 jours</li>
            <li>Bilan : on continue, on ajuste ou on arrête</li>
          </ul>
        </div>
        <div class="card phase-card card-accent-top a-magenta">
          <span class="phase-badge p2">Phase 2</span>
          <div class="title mt-8">Orchestration mensuelle</div>
          <p class="body-sm mt-8" style="color: var(--white-50);">Mensuel &nbsp;|&nbsp; Sans engagement</p>
          <ul class="phase-list p2">
            <li>Pilotage : gouvernance et ajustements stratégiques</li>
            <li>Production : contenu, optimisations, link building</li>
            <li>Ads : pilotage campagnes, enchères, synergies SEA/SEO</li>
            <li>Monitoring : positions, alertes IA, veille concurrentielle</li>
            <li>Reporting : dashboard live, revue mensuelle</li>
            <li>Comité bi-mensuel avec vos équipes</li>
            <li>Bilan trimestriel sur données réelles</li>
          </ul>
        </div>
      </div>
    </div>
    <div class="slide-footer">
      <span>SLASHR &nbsp;|&nbsp; Confidentiel</span>
      <span>09</span>
    </div>
  </section>

  <!-- ============ SLIDE 10 - DIFFERENCIATEURS ============ -->
  <section class="slide" id="slide-10">
    <div class="inner">
      <div class="accent-bar"></div>
      <h2 class="heading">Ce qui nous différencie.</h2>
      <div class="grid-2 mt-32 gap-32">
        <div class="card vs-card dimmed">
          <div class="section-label">L'AGENCE CLASSIQUE DIT</div>
          <div class="quote">"On vous envoie le reporting mensuel. Pour le reste, on se voit au comité trimestriel."</div>
          <p class="body-sm">Interlocuteur junior. Réponse sous 72h. Recommandations déconnectées du terrain.</p>
        </div>
        <div class="card vs-card card-accent-top a-orange">
          <div class="section-label" style="color: var(--orange);">SLASHR DIT</div>
          <div class="quote">"On a regardé vos données ce matin, on vous appelle pour en parler."</div>
          <p class="body-sm">Accès direct aux experts. Réponse dans la journée. On recommande, on exécute, on mesure.</p>
        </div>
      </div>
      <div class="grid-4 mt-24">
        <div class="card diff-card">
          <div class="diff-title">Data avant le call</div>
          <div class="diff-desc">On analyse vos données avant de vous parler.</div>
        </div>
        <div class="card diff-card">
          <div class="diff-title">ROI mesurable</div>
          <div class="diff-desc">Quick wins à 90 jours. Pas de promesse vide.</div>
        </div>
        <div class="card diff-card">
          <div class="diff-title">IA intégrée</div>
          <div class="diff-desc">19 outils propriétaires. Monitoring IA avec Janus.</div>
        </div>
        <div class="card diff-card">
          <div class="diff-title">Sans engagement</div>
          <div class="diff-desc">Phase 1 de 90 jours. Vous décidez de la suite.</div>
        </div>
      </div>
    </div>
    <div class="slide-footer">
      <span>SLASHR &nbsp;|&nbsp; Confidentiel</span>
      <span>10</span>
    </div>
  </section>

  <!-- ============ SLIDE 11 - JANUS ============ -->
  <section class="slide" id="slide-11">
    <div class="blobs blobs-subtle">
      <div class="blob b-magenta" style="left: 50%;"></div>
    </div>
    <div class="inner">
      <div class="grid-2-1" style="grid-template-columns: 1fr 1fr; align-items: center;">
        <div>
          <div class="accent-bar"></div>
          <h2 class="heading">Janus.<br><span class="gradient-text">Visibilité IA.</span></h2>
          <p class="body mt-20" style="max-width: 500px;">Savez-vous ce que l'IA dit de votre marque ?</p>
          <p class="body mt-12" style="max-width: 500px;">ChatGPT, Claude, Gemini, Perplexity - vos clients leur posent des questions. Janus, notre outil propriétaire, surveille ce que les IA disent de votre marque et de vos concurrents. Inclus dans l'accompagnement, sans licence supplémentaire.</p>
          <div class="grid-3 mt-32" style="max-width: 500px;">
            <div class="card" style="padding: 16px; text-align: center;">
              <div class="kpi-label accent">Visibilité</div>
              <div class="caption mt-8">Score de présence dans les IA</div>
            </div>
            <div class="card" style="padding: 16px; text-align: center;">
              <div class="kpi-label accent-m">Sentiment</div>
              <div class="caption mt-8">Tonalité des réponses LLM</div>
            </div>
            <div class="card" style="padding: 16px; text-align: center;">
              <div class="kpi-label accent-v">Sources</div>
              <div class="caption mt-8">Domaines cités par les IA</div>
            </div>
          </div>
        </div>
        <div style="text-align: center;">
          <img src="data:image/png;base64,{janus_b64}" alt="Janus - Monitoring IA" class="janus-mockup">
        </div>
      </div>
    </div>
    <div class="slide-footer">
      <span>SLASHR &nbsp;|&nbsp; Confidentiel</span>
      <span>11</span>
    </div>
  </section>

  <!-- ============ SLIDE 12 - CAS CLIENT VESTIAIRE COLLECTIVE ============ -->
  <section class="slide" id="slide-12">
    <div class="inner">
      <div class="accent-bar"></div>
      <div style="display: flex; align-items: center; gap: 16px; flex-wrap: wrap;">
        <h2 class="heading">Cas client.</h2>
        <span class="tag">VESTIAIRE COLLECTIVE &nbsp;|&nbsp; FUSION SEO &nbsp;|&nbsp; US + EUROPE &nbsp;|&nbsp; MULTI-LANGUES</span>
      </div>
      <div class="grid-1-1 mt-32">
        <div>
          <div class="section-label">CONTEXTE</div>
          <p class="body">Vestiaire Collective, marketplace de luxe seconde main valorisée à 1,7 milliard d'euros, acquiert Tradesy, son équivalent américain. 1,6 million de mots-clés positionnés à récupérer. Plus de 10 millions d'URLs à rediriger. Traitement manuel impossible : 1 400 heures estimées.</p>
          <div class="section-label mt-24">CE QU'ON A FAIT</div>
          <p class="body">Framework hybride automatisation + traitement manuel. Segmentation et priorisation des URLs. Matching des 10M d'URLs dans des délais serrés. Monitoring et optimisation post-migration. Collaboration étroite avec les équipes Vestiaire Collective.</p>
          <div class="verbatim mt-24">
            "SLASHR a su gérer cette migration complexe avec une méthodologie rigoureuse et des outils automatisés qui nous ont permis de respecter nos délais tout en minimisant les risques. Les résultats parlent d'eux-mêmes : +162% de trafic SEO."
            <div class="author">Jean-Éric Blas-Châtelain, Principal Engineer Buyer Experience, Vestiaire Collective</div>
          </div>
        </div>
        <div class="grid-2" style="gap: 16px;">
          <div class="card case-result" style="grid-column: span 2;">
            <div class="num" style="font-size: 42px;">+162%</div>
            <div class="label" style="font-size: 14px;">de trafic SEO<br>après la fusion</div>
          </div>
          <div class="card case-result">
            <div class="num">+1,6M</div>
            <div class="label">mots-clés<br>récupérés</div>
          </div>
          <div class="card case-result">
            <div class="num">+10 000</div>
            <div class="label">domaines référents<br>récupérés</div>
          </div>
        </div>
      </div>
      <div class="mt-16" style="display: flex; gap: 8px; flex-wrap: wrap;">
        <span class="tag" style="font-size: 10px;">MIGRATION SEO</span>
        <span class="tag" style="font-size: 10px;">SEO INTERNATIONAL</span>
        <span class="tag" style="font-size: 10px;">SEO E-COMMERCE</span>
        <span class="tag" style="font-size: 10px;">10M+ URLs</span>
      </div>
    </div>
    <div class="slide-footer">
      <span>SLASHR &nbsp;|&nbsp; Confidentiel</span>
      <span>12</span>
    </div>
  </section>

  <!-- ============ SLIDE 13 - CAS CLIENT CARTER CASH ============ -->
  <section class="slide" id="slide-13">
    <div class="inner">
      <div class="accent-bar"></div>
      <div style="display: flex; align-items: center; gap: 16px; flex-wrap: wrap;">
        <h2 class="heading">Cas client.</h2>
        <span class="tag">CARTER CASH &nbsp;|&nbsp; FUSION SEO E-COMMERCE</span>
      </div>
      <div class="grid-1-1 mt-32">
        <div>
          <div class="section-label">CONTEXTE</div>
          <p class="body">Carter Cash (groupe Mobivia - Norauto, Midas) acquiert les actifs de Yakarouler pour amplifier sa présence digitale sur le marché de la pièce auto. Architecture complexe : catégories, marques, modèles, cylindrées créant un volume d'URLs exponentiel. 30 000 URLs stratégiques à rediriger sans casser l'existant.</p>
          <div class="section-label mt-24">CE QU'ON A FAIT</div>
          <p class="body">Développement d'une méthodologie de fusion sur-mesure. Segmentation et priorisation par trafic et revenus. Matching des URLs. Monitoring post-migration et optimisation continue.</p>
          <div class="verbatim mt-24">
            "SLASHR nous a accompagnés tout au long de cette fusion complexe. Leur méthodologie rigoureuse et leurs outils automatisés nous ont permis de respecter nos délais tout en minimisant les risques. Les gains de positionnement parlent d'eux-mêmes."
            <div class="author">Antoine Thomas, SEO Manager, Carter Cash</div>
          </div>
        </div>
        <div class="grid-3" style="gap: 16px;">
          <div class="card case-result">
            <div class="num">+37%</div>
            <div class="label">mots-clés<br>Top 3</div>
          </div>
          <div class="card case-result">
            <div class="num">+45%</div>
            <div class="label">mots-clés<br>Top 4-10</div>
          </div>
          <div class="card case-result">
            <div class="num">+35%</div>
            <div class="label">mots-clés<br>Top 11-20</div>
          </div>
        </div>
      </div>
      <div class="mt-16" style="display: flex; gap: 8px; flex-wrap: wrap;">
        <span class="tag" style="font-size: 10px;">MIGRATION SEO</span>
        <span class="tag" style="font-size: 10px;">SEO E-COMMERCE</span>
        <span class="tag" style="font-size: 10px;">STRATÉGIE DE REDIRECTION</span>
        <span class="tag" style="font-size: 10px;">GROUPE MOBIVIA</span>
      </div>
    </div>
    <div class="slide-footer">
      <span>SLASHR &nbsp;|&nbsp; Confidentiel</span>
      <span>13</span>
    </div>
  </section>

  <!-- ============ SLIDE 14 - EQUIPE ============ -->
  <section class="slide" id="slide-14">
    <div class="inner">
      <div class="accent-bar"></div>
      <h2 class="heading">L'équipe.</h2>
      <p class="body mt-16">3 associés-fondateurs. Une équipe de consultants spécialisés. Un interlocuteur dédié.</p>
      <div class="grid-3 mt-32 gap-32">
        <div class="card team-card" style="padding: 24px;">
          <div class="team-avatar founder">QC</div>
          <div class="team-info">
            <div class="name">Quentin Clément</div>
            <div class="role">Directeur commercial & Associé</div>
          </div>
        </div>
        <div class="card team-card" style="padding: 24px;">
          <div class="team-avatar founder">BD</div>
          <div class="team-info">
            <div class="name">Benoit Demonchaux</div>
            <div class="role">Directeur de production & Associé</div>
          </div>
        </div>
        <div class="card team-card" style="padding: 24px;">
          <div class="team-avatar founder">AL</div>
          <div class="team-info">
            <div class="name">Anthony Lecas</div>
            <div class="role">Directeur Conseil & Associé</div>
          </div>
        </div>
      </div>
      <div class="grid-3 mt-16">
        <div class="card team-card">
          <div class="team-avatar" style="color: var(--violet);">LC</div>
          <div class="team-info">
            <div class="name">Lucas Colin</div>
            <div class="role">Chef de projet senior</div>
          </div>
        </div>
        <div class="card team-card">
          <div class="team-avatar" style="color: var(--violet);">JT</div>
          <div class="team-info">
            <div class="name">Jessica Tan</div>
            <div class="role">Chef de projet senior</div>
          </div>
        </div>
        <div class="card team-card">
          <div class="team-avatar" style="color: var(--magenta);">PAH</div>
          <div class="team-info">
            <div class="name">Pierre-Antoine Henneaux</div>
            <div class="role">Consultant SEO/GEO</div>
          </div>
        </div>
        <div class="card team-card">
          <div class="team-avatar" style="color: var(--magenta);">TC</div>
          <div class="team-info">
            <div class="name">Tom Chemin</div>
            <div class="role">Consultant SEO/GEO</div>
          </div>
        </div>
        <div class="card team-card">
          <div class="team-avatar" style="color: var(--magenta);">ML</div>
          <div class="team-info">
            <div class="name">Maxime Legru</div>
            <div class="role">Consultant SEO/GEO</div>
          </div>
        </div>
        <div class="card team-card">
          <div class="team-avatar" style="color: var(--orange);">HP</div>
          <div class="team-info">
            <div class="name">Hubert Pajot</div>
            <div class="role">Consultant SEA/SMA</div>
          </div>
        </div>
      </div>
    </div>
    <div class="slide-footer">
      <span>SLASHR &nbsp;|&nbsp; Confidentiel</span>
      <span>14</span>
    </div>
  </section>

  <!-- ============ SLIDE 15 - REFERENCES ============ -->
  <section class="slide" id="slide-15">
    <div class="inner">
      <div class="accent-bar"></div>
      <h2 class="heading">Nos références.</h2>
      <p class="body mt-16">Des marques de tous secteurs qui nous font confiance pour leur stratégie Search.</p>
      <div class="grid-2 mt-32 gap-32">
        <div class="card card-accent-top a-orange" style="padding: 28px; border-color: rgba(231,70,1,0.3);">
          <div class="section-label" style="color: var(--orange);">BELGIQUE</div>
          <div class="title" style="font-size: 22px;">Cofidis Belgique</div>
          <p class="body-sm mt-8">Services financiers, marché belge. Stratégie Search multi-produits et acquisition organique.</p>
        </div>
        <div class="card card-accent-top a-magenta" style="padding: 28px; border-color: rgba(206,8,169,0.3);">
          <div class="section-label" style="color: var(--magenta);">RETAIL</div>
          <div class="title" style="font-size: 22px;">Decathlon</div>
          <p class="body-sm mt-8">Retail sport, réseau physique + e-commerce. Stratégie Search à grande échelle.</p>
        </div>
      </div>
      <div class="grid-4 mt-16">
        <div class="card ref-card">
          <div class="ref-name">Vestiaire Collective</div>
          <div class="ref-desc">E-commerce mode<br>Migration internationale</div>
        </div>
        <div class="card ref-card">
          <div class="ref-name">Carter Cash</div>
          <div class="ref-desc">Groupe Mobivia<br>Migration SEO</div>
        </div>
        <div class="card ref-card">
          <div class="ref-name">Le Fourgon</div>
          <div class="ref-desc">E-commerce alimentaire<br>Acquisition organique</div>
        </div>
        <div class="card ref-card">
          <div class="ref-name">Somfy</div>
          <div class="ref-desc">Industrie / IoT<br>Stratégie Search</div>
        </div>
        <div class="card ref-card">
          <div class="ref-name">SKEMA</div>
          <div class="ref-desc">Business School<br>SEO international</div>
        </div>
        <div class="card ref-card">
          <div class="ref-name">EDHEC</div>
          <div class="ref-desc">Business School<br>Visibilité Search</div>
        </div>
        <div class="card ref-card">
          <div class="ref-name">Agryco</div>
          <div class="ref-desc">Agroalimentaire<br>Acquisition organique</div>
        </div>
        <div class="card ref-card">
          <div class="ref-name">Ateliers Vanderschooten</div>
          <div class="ref-desc">Industrie<br>Stratégie Search</div>
        </div>
      </div>
    </div>
    <div class="slide-footer">
      <span>SLASHR &nbsp;|&nbsp; Confidentiel</span>
      <span>15</span>
    </div>
  </section>

  <!-- ============ SLIDE 16 - PROCHAINES ETAPES ============ -->
  <section class="slide" id="slide-16">
    <div class="inner">
      <div class="accent-bar"></div>
      <h2 class="heading">Prochaines étapes.</h2>
      <p class="body mt-16" style="max-width: 600px;">Un processus simple, sans engagement prématuré.</p>
      <div class="grid-3 mt-40 gap-32">
        <div class="card card-accent-top a-orange" style="padding: 32px 24px;">
          <div class="step-number accent">01</div>
          <div class="step-title accent">Échange</div>
          <p class="step-desc">On prend 45 minutes pour comprendre vos enjeux, vos contraintes et vos priorités. On vous partage nos premières observations sur vos données Search.</p>
        </div>
        <div class="card card-accent-top a-magenta" style="padding: 32px 24px;">
          <div class="step-number accent-m">02</div>
          <div class="step-title accent-m">Recommandation</div>
          <p class="step-desc">On revient avec une proposition sur-mesure : diagnostic, périmètre, budget. Pas de template, pas de grille tarifaire. Un plan adapté à Delhaize.</p>
        </div>
        <div class="card card-accent-top a-violet" style="padding: 32px 24px;">
          <div class="step-number accent-v">03</div>
          <div class="step-title accent-v">Décision</div>
          <p class="step-desc">Vous décidez. Phase 1 de 90 jours. À la fin, bilan sur données réelles. On continue, on ajuste ou on arrête. Zéro risque.</p>
        </div>
      </div>
    </div>
    <div class="slide-footer">
      <span>SLASHR &nbsp;|&nbsp; Confidentiel</span>
      <span>16</span>
    </div>
  </section>

  <!-- ============ SLIDE 17 - CLOTURE ============ -->
  <section class="slide hero cta-slide" id="slide-17">
    <div class="blobs">
      <div class="blob b-orange"></div>
      <div class="blob b-magenta"></div>
      <div class="blob b-violet"></div>
    </div>
    <div class="inner">
      <img src="data:image/png;base64,{logo_b64}" alt="SLASHR" style="height: 40px; margin-bottom: 32px; opacity: 0.9;">
      <h2 class="display-l">Prenez le contrôle<br>du Search.</h2>
      <p class="subtitle mt-16" style="color: var(--white-50);">Agence Search Marketing &nbsp;|&nbsp; Lille, France</p>
      <div class="gradient-bar"></div>
      <p class="cta-text">Discutons de votre stratégie Search.</p>
      <p class="contact">Quentin Clément &nbsp;|&nbsp; quentin@agence-slashr.fr</p>
    </div>
    <div class="slide-footer">
      <span>SLASHR &nbsp;|&nbsp; Confidentiel</span>
      <span>17</span>
    </div>
  </section>

</div>

<!-- SCRIPTS -->
<script>
(function() {{
  const deck = document.getElementById('deck');
  const slides = document.querySelectorAll('.slide');
  const counter = document.getElementById('current-slide');
  const progress = document.getElementById('progress');
  const total = slides.length;
  document.getElementById('total-slides').textContent = total;

  // Intersection Observer for animations
  const observer = new IntersectionObserver((entries) => {{
    entries.forEach(e => {{
      if (e.isIntersecting) e.target.classList.add('visible');
    }});
  }}, {{ root: deck, threshold: 0.3 }});
  slides.forEach(s => observer.observe(s));

  // Update counter + progress on scroll
  deck.addEventListener('scroll', () => {{
    const scrollTop = deck.scrollTop;
    const scrollHeight = deck.scrollHeight - deck.clientHeight;
    const pct = scrollHeight > 0 ? (scrollTop / scrollHeight) * 100 : 0;
    progress.style.width = pct + '%';

    let current = 1;
    slides.forEach((s, i) => {{
      if (s.offsetTop <= scrollTop + deck.clientHeight * 0.4) current = i + 1;
    }});
    counter.textContent = current;
  }});

  // Keyboard navigation
  document.addEventListener('keydown', (e) => {{
    const currentIdx = parseInt(counter.textContent) - 1;
    if (e.key === 'ArrowDown' || e.key === 'ArrowRight' || e.key === ' ') {{
      e.preventDefault();
      if (currentIdx < total - 1) slides[currentIdx + 1].scrollIntoView({{ behavior: 'smooth' }});
    }}
    if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') {{
      e.preventDefault();
      if (currentIdx > 0) slides[currentIdx - 1].scrollIntoView({{ behavior: 'smooth' }});
    }}
    if (e.key === 'Home') {{ e.preventDefault(); slides[0].scrollIntoView({{ behavior: 'smooth' }}); }}
    if (e.key === 'End') {{ e.preventDefault(); slides[total-1].scrollIntoView({{ behavior: 'smooth' }}); }}
  }});

  // Initial state
  slides[0].classList.add('visible');
}})();
</script>
</body>
</html>'''

output_path = "/Users/quentin/Desktop/SLASHR-Presentation-Ahold-Delhaize.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"HTML presentation saved to {output_path}")
print(f"File size: {os.path.getsize(output_path) / 1024:.0f} KB")
