"""Public-facing portfolio landing experience for ConstructVision."""
from __future__ import annotations

import streamlit as st


def _style() -> None:
    st.markdown(
        """
        <style>
        .cv-portfolio {max-width: 1240px; margin: 0 auto; padding: 0.5rem 0 4rem;}
        .cv-kicker {color:#70e1d0; font-family:monospace; font-size:.78rem; font-weight:700; letter-spacing:.16em; text-transform:uppercase;}
        .cv-hero {position:relative; overflow:hidden; padding:4.5rem 3.2rem 3rem; border:1px solid rgba(112,225,208,.24); border-radius:28px; background:radial-gradient(circle at 84% 16%,rgba(57,198,217,.23),transparent 27%), radial-gradient(circle at 12% 82%,rgba(169,155,255,.17),transparent 27%), linear-gradient(135deg,#0a1a2a,#07131f 60%,#102333);}
        .cv-hero:after {content:''; position:absolute; inset:0; pointer-events:none; opacity:.22; background-image:linear-gradient(rgba(112,225,208,.16) 1px,transparent 1px),linear-gradient(90deg,rgba(112,225,208,.16) 1px,transparent 1px); background-size:42px 42px; mask-image:linear-gradient(90deg,transparent,black 35%,black 70%,transparent);}
        .cv-hero h1 {position:relative; z-index:1; max-width:850px; margin:.5rem 0 1rem; color:#f2fbff; font-size:clamp(2.8rem,7vw,5.9rem); line-height:.96; letter-spacing:-.065em;}
        .cv-hero p {position:relative; z-index:1; max-width:700px; color:#b8d0dc; font-size:1.16rem; line-height:1.65;}
        .cv-nav {display:flex; flex-wrap:wrap; gap:.8rem; margin:1rem 0 1.3rem;}
        .cv-nav a {color:#b8d0dc; text-decoration:none; padding:.45rem .7rem; border:1px solid #294354; border-radius:999px; font-size:.82rem;}
        .cv-nav a:hover {border-color:#70e1d0; color:#70e1d0;}
        .cv-section {padding:4rem .45rem 0;}
        .cv-section h2 {font-size:clamp(1.8rem,3vw,2.8rem); letter-spacing:-.045em; color:#f2fbff; margin:.35rem 0 .7rem;}
        .cv-lead {max-width:760px; color:#a9c1cc; line-height:1.7; font-size:1.05rem;}
        .cv-card {height:100%; min-height:175px; border:1px solid #294354; border-radius:18px; padding:1.35rem; background:linear-gradient(145deg,rgba(16,35,51,.92),rgba(7,19,31,.84)); box-shadow:0 18px 45px rgba(0,0,0,.16);}
        .cv-card:hover {border-color:rgba(112,225,208,.7); transform:translateY(-3px); transition:.2s ease;}
        .cv-card h3 {color:#edf7fa; font-size:1.08rem; margin:.15rem 0 .6rem;}
        .cv-card p,.cv-card li {color:#9db7c4; font-size:.91rem; line-height:1.55;}
        .cv-number {color:#f7b955; font-size:.78rem; font-family:monospace; letter-spacing:.12em;}
        .cv-stage {border-left:1px solid #507c7f; padding:0 0 1.7rem 1.3rem; margin-left:.55rem; position:relative;}
        .cv-stage:before {content:''; position:absolute; left:-.38rem; top:.1rem; width:.68rem; height:.68rem; border-radius:50%; background:#70e1d0; box-shadow:0 0 0 5px rgba(112,225,208,.13);}
        .cv-stage h3 {margin:0 0 .35rem; color:#edf7fa;}
        .cv-stage p {color:#9db7c4; margin:0; line-height:1.55;}
        .cv-quote {margin-top:2rem; padding:2rem; border-radius:18px; border:1px solid #384e7b; background:linear-gradient(110deg,rgba(80,124,255,.17),rgba(16,35,51,.4)); color:#dce9ff; font-size:1.25rem; line-height:1.5;}
        .cv-footer {margin-top:4rem; padding:2rem 0; border-top:1px solid #294354; color:#8caab7; font-size:.9rem;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render() -> None:
    """Render a polished narrative landing page without making engineering claims."""
    _style()
    st.markdown('<main class="cv-portfolio">', unsafe_allow_html=True)
    st.markdown(
        """
        <nav class="cv-nav" aria-label="Portfolio navigation">
          <a href="#platform">Platform</a><a href="#workflow">Workflow</a><a href="#architecture">Architecture</a>
          <a href="#philosophy">Philosophy</a><a href="#roadmap">Roadmap</a><a href="#report">Report</a>
        </nav>
        <section class="cv-hero">
          <div class="cv-kicker">ConstructVision AI / Built environment intelligence</div>
          <h1>Make the built world legible.</h1>
          <p>ConstructVision brings site evidence, material context, telemetry and engineering workflows into one clear digital-twin narrative—built to help teams inspect, understand and act with traceability.</p>
        </section>
        """,
        unsafe_allow_html=True,
    )
    action, spacer = st.columns([1, 4])
    with action:
        st.button("Enter twin workspace", type="primary", icon=":material/arrow_forward:", key="portfolio_enter")
    if st.session_state.get("portfolio_enter"):
        st.session_state["portfolio_requested_workspace"] = True
        st.info("Use the sidebar to open Command center, Twin studio, Capture & reconstruction, Asset health, or Integration.")

    st.markdown('<section id="platform" class="cv-section"><div class="cv-kicker">01 / The proposition</div><h2>An inspection portfolio with a real platform behind it.</h2><p class="cv-lead">This landing page presents the project as a professional case study while the product workspace remains available alongside it. The goal is not decorative 3D: it is a trustworthy path from field observation to reviewable engineering evidence.</p></section>', unsafe_allow_html=True)
    cols = st.columns(3)
    cards = [
        ("CAPTURE", "Evidence, not assumptions", "Register calibrated image packages with coverage, scale and provenance requirements before reconstruction is considered."),
        ("TWIN", "A living asset context", "Explore a parametric structural frame, material assumptions and scenario inputs in a single operational view."),
        ("DECIDE", "Traceable review", "Preserve model revisions, telemetry inputs, solver readiness and the boundary between screening and certified analysis."),
    ]
    for col, (label, title, text) in zip(cols, cards):
        with col:
            st.markdown(f'<article class="cv-card"><div class="cv-number">{label}</div><h3>{title}</h3><p>{text}</p></article>', unsafe_allow_html=True)

    st.markdown('<section id="workflow" class="cv-section"><div class="cv-kicker">02 / Experience map</div><h2>From the jobsite to a decision-ready record.</h2></section>', unsafe_allow_html=True)
    steps = [
        ("01", "Capture", "Collect overlapping, calibrated imagery and record scale control. A handful of photographs is a visual reference—not metric geometry."),
        ("02", "Interpret", "Use computer vision and material knowledge to triage observations, with confidence and limitations shown clearly."),
        ("03", "Model", "Associate observations with an asset revision, semantic components and monitored conditions."),
        ("04", "Review", "Send approved scenarios to validated reconstruction, FEA or CFD workers; retain solver version, logs and artifacts."),
    ]
    left, right = st.columns(2)
    for col, group in ((left, steps[:2]), (right, steps[2:])):
        with col:
            for no, title, text in group:
                st.markdown(f'<div class="cv-stage"><div class="cv-number">{no}</div><h3>{title}</h3><p>{text}</p></div>', unsafe_allow_html=True)

    st.markdown('<section id="architecture" class="cv-section"><div class="cv-kicker">03 / System architecture</div><h2>Designed as an API-first digital-twin foundation.</h2><p class="cv-lead">The dashboard is one client of the platform. The core product is the governed data and workflow layer that records what was captured, calculated, simulated and signed off.</p></section>', unsafe_allow_html=True)
    arch = st.columns(4)
    layers = [
        ("01", "Experience layer", "Streamlit product workspace today; a future web 3D client can consume API-approved glTF/3D Tiles."),
        ("02", "Platform API", "FastAPI contracts for assets, capture packages, telemetry batches and analysis jobs."),
        ("03", "Data foundation", "SQLite locally; PostgreSQL/TimescaleDB plus object storage in deployment."),
        ("04", "Compute workers", "COLMAP, OpenSees and OpenFOAM are explicit worker capabilities, never fabricated visual output."),
    ]
    for col, (no, title, text) in zip(arch, layers):
        with col:
            st.markdown(f'<article class="cv-card"><div class="cv-number">LAYER {no}</div><h3>{title}</h3><p>{text}</p></article>', unsafe_allow_html=True)

    st.markdown('<section id="philosophy" class="cv-section"><div class="cv-kicker">04 / Philosophy</div><h2>Trust is a feature.</h2><div class="cv-quote">“A useful digital twin should make uncertainty visible, preserve evidence, and make it easier for qualified people to reach a better decision.”</div></section>', unsafe_allow_html=True)
    values = st.columns(3)
    for col, (title, text) in zip(values, [
        ("Evidence before spectacle", "Visual richness must never be confused with measurement accuracy or engineering verification."),
        ("Human accountability", "AI supports inspection and prioritisation; licensed engineers remain responsible for design judgement and sign-off."),
        ("Interoperability by design", "Versioned API contracts, open geometry formats and isolated workers prevent a single UI or vendor from owning the truth."),
    ]):
        with col:
            st.markdown(f'<article class="cv-card"><h3>{title}</h3><p>{text}</p></article>', unsafe_allow_html=True)

    st.markdown('<section id="roadmap" class="cv-section"><div class="cv-kicker">05 / Delivery roadmap</div><h2>From portfolio prototype to deployment-ready platform.</h2></section>', unsafe_allow_html=True)
    roadmap = st.columns(3)
    for col, (no, title, text) in zip(roadmap, [
        ("NOW", "Foundation", "Validate API contracts, establish report evidence, improve UX and demonstrate the local workflow."),
        ("NEXT", "Production hardening", "Add authentication, migrations, container images, CI, PostgreSQL/TimescaleDB, object storage and a job queue."),
        ("LATER", "Engineering scale", "Deploy validated reconstruction and solver workers, semantic BIM import, browser-native 3D and formal review workflows."),
    ]):
        with col:
            st.markdown(f'<article class="cv-card"><div class="cv-number">{no}</div><h3>{title}</h3><p>{text}</p></article>', unsafe_allow_html=True)

    st.markdown('<section id="report" class="cv-section"><div class="cv-kicker">06 / Documentation</div><h2>A report structure ready for academic and portfolio use.</h2><p class="cv-lead">The documentation pack contains an abstract, complete chapter draft, architecture analysis, evaluation plan, ethical statement and deployment checklist. Replace bracketed placeholders with institution, mentor, contributor and measured evaluation details before submission.</p></section>', unsafe_allow_html=True)
    report_col, api_col = st.columns(2)
    with report_col:
        st.markdown('<article class="cv-card"><div class="cv-number">REPORT PACK</div><h3>Project documentation</h3><p>Use the repository’s <code>docs/REPORT_DRAFT.md</code> and <code>docs/ABSTRACT.md</code> as the source drafts for the final report.</p></article>', unsafe_allow_html=True)
    with api_col:
        st.markdown('<article class="cv-card"><div class="cv-number">API CONTRACT</div><h3>Live developer evidence</h3><p>When the API is running, Swagger documentation is served at <code>/docs</code>. It exposes the asset, capture, telemetry and analysis-job contracts.</p></article>', unsafe_allow_html=True)
    st.markdown('<footer class="cv-footer">CONSTRUCTVISION AI · Built environment intelligence · Portfolio and digital-twin platform foundation</footer></main>', unsafe_allow_html=True)
