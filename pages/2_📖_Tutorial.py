

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================
st.set_page_config(
    page_title="Tutorial & Guide | CONSTRUCTVISION AI",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# CUSTOM DARK BLUEPRINT STYLING
# ==========================================================
st.markdown("""
<style>
    /* Global App Styling */
    .stApp {
        background-color: #0B0F17;
        color: #E2E8F0;
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }

    /* Dark Blueprint Background Grid Overlay */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image:
            linear-gradient(rgba(56, 189, 248, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(56, 189, 248, 0.03) 1px, transparent 1px);
        background-size: 35px 35px;
        pointer-events: none;
        z-index: 0;
    }

    /* Hide Default Headers/Footers */
    #MainMenu, footer, header {
        visibility: hidden;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #111827 !important;
        border-right: 1px solid #1E293B;
    }

    /* Dark Cards & Hover Effects */
    .dark-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
        transition: all 0.3s ease-in-out;
    }
    .dark-card:hover {
        border-color: #38BDF8;
        box-shadow: 0 6px 25px rgba(56, 189, 248, 0.2);
        transform: translateY(-3px);
    }

    /* Comparison Card Styling */
    .comparison-card-manual {
        background: #1E1B18;
        border: 1px solid #7C2D12;
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .comparison-card-ai {
        background: #061E29;
        border: 1px solid #0369A1;
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 20px;
    }

    /* Hero Banner */
    .hero-dark {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid #334155;
        border-left: 6px solid #38BDF8;
        border-radius: 16px;
        padding: 32px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }

    /* Accent Typography */
    h1, h2, h3, h4 {
        color: #F8FAFC !important;
        font-weight: 700;
    }
    .accent-cyan { color: #38BDF8 !important; }
    .accent-orange { color: #F97316 !important; }
    .accent-green { color: #10B981 !important; }
    .accent-red { color: #EF4444 !important; }

    /* Custom Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #0284C7 0%, #0369A1 100%);
        color: white !important;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.6rem 1.2rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #EA580C 0%, #C2410C 100%);
        box-shadow: 0 0 15px rgba(234, 88, 12, 0.4);
    }

    /* Streamlit Expander Dark Override */
    .streamlit-expanderHeader {
        background-color: #1E293B !important;
        color: #F8FAFC !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================================
# SIDEBAR NAVIGATION & QUICK JUMP
# ==========================================================
with st.sidebar:
    st.markdown("### 📘 **CONSTRUCTVISION AI**")
    st.caption("Interactive Tutorial & User Guide")
    st.divider()

    guide_section = st.radio(
        "Tutorial Navigation",
        [
            "🏠 Platform Overview",
            "🔄 Manual vs. AI Inspection",
            "⚙️ Interactive Workflow Stepper",
            "🧱 Dashboard Module Guide",
            "⚡ AI vs. Manual ROI Calculator",
            "⚖️ Advantages & Disadvantages",
            "📋 Best Practices & Guidelines",
            "💡 Practice Knowledge Check",
            "❓ Interactive FAQ",
            "👷 Team & Credits"
        ]
    )

    st.divider()
    st.info("💡 **Tip:** Check the **Manual vs. AI Inspection** section to see step-by-step comparative workflows.")
    st.caption("Version 2.4 Dark Blueprint | © 2026")

# ==========================================================
# SECTION 1: PLATFORM OVERVIEW
# ==========================================================
if guide_section == "🏠 Platform Overview":
    st.markdown("""
    <div class="hero-dark">
        <h1>📘 Tutorial & <span class="accent-cyan">User Guide</span></h1>
        <p style="font-size: 1.15rem; color: #94A3B8;">
            Master the <b>CONSTRUCTVISION AI</b> residential inspection workspace.
        </p>
        <hr style="border-color: #334155;">
        <p style="color: #CBD5E1; line-height: 1.8;">
            <b>CONSTRUCTVISION AI</b> is an engineering decision-support platform designed to automate residential structural defect recognition, perform damage severity assessments, estimate repair costs, and compile compliant audit reports using Artificial Intelligence and Computer Vision.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🎯 Core Engineering Objectives")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="dark-card">
            <h3 class="accent-cyan">📷 Automated Vision</h3>
            <p style="color:#94A3B8; font-size:14px;">Replaces subjective manual sight checks with high-precision YOLO object detection for micro-cracks, spalling, and voids.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="dark-card">
            <h3 class="accent-orange">📊 Quantitative Risk</h3>
            <p style="color:#94A3B8; font-size:14px;">Evaluates structural integrity based on civil engineering codes (IS 456 / ACI 318) to classify defect severity grades.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="dark-card">
            <h3 class="accent-green">📄 Instant Audits</h3>
            <p style="color:#94A3B8; font-size:14px;">Generates structured, professional site inspection reports ready for project managers and structural consultants.</p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================================
# SECTION 2: MANUAL VS. AI INSPECTION (NEW SECTION)
# ==========================================================
elif guide_section == "🔄 Manual vs. AI Inspection":
    st.markdown("## 🔄 Traditional Manual Inspection vs. AI Digital Workflow")
    st.caption("How civil engineers historically conducted structural audits vs. how CONSTRUCTVISION AI modernizes the process.")

    st.write("")

    # Visual Workflow Timeline Simulation (Plotly Chart)
    st.markdown("### ⏱️ Time & Labor Allocation Breakdown")
    
    tasks_df = pd.DataFrame([
        dict(Task="1. Site Preparation & Scaffolding", Method="Manual Inspection", Duration=2.0, Details="Erecting ladders/scaffolding to access high columns and beams"),
        dict(Task="2. Visual Surface Inspection", Method="Manual Inspection", Duration=3.5, Details="Engineers inspect with flashlights, magnifying lenses, and crack gauges"),
        dict(Task="3. Manual Measurement & Sketching", Method="Manual Inspection", Duration=2.5, Details="Hand-drawing crack maps on paper clipboards and using calipers"),
        dict(Task="4. Office Report Compilation", Method="Manual Inspection", Duration=4.0, Details="Typing observations, formatting photos, calculating repair estimates in Excel"),
        
        dict(Task="1. Drone/Phone Image Capture", Method="CONSTRUCTVISION AI", Duration=0.5, Details="Capturing high-res photos via smartphone, drone, or IoT cameras"),
        dict(Task="2. AI Crack & Spall Detection", Method="CONSTRUCTVISION AI", Duration=0.1, Details="Instant computer vision bounding boxes and severity scoring (< 2 sec)"),
        dict(Task="3. Automated 3D Risk Mapping", Method="CONSTRUCTVISION AI", Duration=0.2, Details="Automatic overlay on 3D building twin with live strain telemetry"),
        dict(Task="4. 1-Click PDF Report Export", Method="CONSTRUCTVISION AI", Duration=0.2, Details="Instant generation of standardized audit logs with cost estimates")
    ])

    fig_timeline = px.bar(
        tasks_df, 
        x="Duration", 
        y="Task", 
        color="Method", 
        orientation='h',
        title="Inspection Hours Required per Structural Component",
        labels={"Duration": "Hours Required"},
        template="plotly_dark",
        color_discrete_map={"Manual Inspection": "#EF4444", "CONSTRUCTVISION AI": "#38BDF8"},
        hover_data=["Details"]
    )
    fig_timeline.update_layout(paper_bgcolor="#1E293B", plot_bgcolor="#1E293B", height=420)
    st.plotly_chart(fig_timeline, use_container_width=True)

    st.markdown("---")
    st.markdown("### 🔍 Step-by-Step Methodological Comparison")

    col_m1, col_a1 = st.columns(2)

    with col_m1:
        st.markdown("""
        <div class="comparison-card-manual">
            <h3 class="accent-orange">🔨 Traditional Manual Workflow</h3>
            <p style="color:#CBD5E1; font-size:14px;">How engineers traditionally inspect buildings:</p>
            <ol style="color:#94A3B8; font-size:13px; line-height:1.7;">
                <li><b>Visual Observation:</b> Engineers walk around the site using flashlights, measuring tapes, and crack width comparison cards (optical scales).</li>
                <li><b>Physical Marking:</b> Cracks are marked directly on concrete faces using chalk, paint, or masking tape with hand-written dates.</li>
                <li><b>Paper Logbook Recording:</b> Crack dimensions, location references, and visual notes are handwritten into field clipboards.</li>
                <li><b>Destructive Tapping:</b> Using a tapping hammer (or rebound hammer) to listen for hollow sounds indicating internal concrete delamination.</li>
                <li><b>Manual Report Writing:</b> Returning to the office, downloading camera photos, cropping images, typing Word documents, and manually estimating repair quantities.</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

    with col_a1:
        st.markdown("""
        <div class="comparison-card-ai">
            <h3 class="accent-cyan">🤖 CONSTRUCTVISION AI Workflow</h3>
            <p style="color:#CBD5E1; font-size:14px;">How the modern digital twin platform operates:</p>
            <ol style="color:#94A3B8; font-size:13px; line-height:1.7;">
                <li><b>Multi-Sensor Image Capture:</b> High-res photo uploaded directly via smartphone, drone feed, or fixed CCTV camera.</li>
                <li><b>Sub-Pixel AI Computer Vision:</b> YOLO neural network identifies micro-cracks (<0.1mm), spalling, rebar exposure, and honeycombing instantly.</li>
                <li><b>Automated Code Compliance:</b> Software maps crack widths against standard civil codes (IS 456 / ACI 318) to assign hazard levels (Low, Med, Critical).</li>
                <li><b>3D Twin Spatial Integration:</b> Defect coordinates are mapped onto a interactive 3D building frame with IoT strain gauge overlays.</li>
                <li><b>1-Click Audit & Costing:</b> Instant cost estimation for epoxy grouting/jacketing and downloadable PDF/text audit reports.</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

# ==========================================================
# SECTION 3: INTERACTIVE WORKFLOW STEPPER
# ==========================================================
elif guide_section == "⚙️ Interactive Workflow Stepper":
    st.markdown("## ⚙️ Interactive Inspection Workflow Pipeline")
    st.caption("Step through the 4-phase automated inspection pipeline to see how data flows from site capture to final report.")

    step = st.select_slider(
        "Move slider to test each phase of the workflow:",
        options=["Phase 1: Image Capture", "Phase 2: AI Computer Vision", "Phase 3: Structural Assessment", "Phase 4: Audit Report Generation"]
    )

    st.write("")

    if "Phase 1" in step:
        st.markdown("""
        <div class="dark-card">
            <h3 class="accent-cyan">Phase 1: High-Resolution Image Capture 📷</h3>
            <p><b>Objective:</b> Collect visual evidence from columns, beams, slabs, or masonry brickwork.</p>
            <ul>
                <li>Ensure adequate natural lighting or artificial floodlights.</li>
                <li>Hold camera perpendicular to the target surface to minimize perspective distortion.</li>
                <li>Supported formats: JPG, PNG, WEBP (Minimum recommended resolution: 1080p).</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    elif "Phase 2" in step:
        st.markdown("""
        <div class="dark-card">
            <h3 class="accent-orange">Phase 2: Deep Learning Inference 🧠</h3>
            <p><b>Objective:</b> Computer Vision model parses pixel matrices to localize structural anomalies.</p>
            <ul>
                <li>Detects <b>Shear Cracks</b>, <b>Concrete Spalling</b>, and <b>Aggregate Honeycombing</b>.</li>
                <li>Draws real-time bounding boxes with confidence probability scores (e.g., 94.8%).</li>
                <li>Filters out non-structural surface dirt or paint scuffs based on model sensitivity sliders.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    elif "Phase 3" in step:
        st.markdown("""
        <div class="dark-card">
            <h3 class="accent-green">Phase 3: Civil Engineering Assessment 🏗️</h3>
            <p><b>Objective:</b> Evaluate structural threat level and determine remediation requirements.</p>
            <ul>
                <li><b>Low Severity:</b> Hairline crazing (< 0.2 mm width) - Seal & monitor.</li>
                <li><b>Medium Severity:</b> Flexural cracking (0.2 mm - 1.5 mm) - Polymer resin injection.</li>
                <li><b>High Severity:</b> Spalling with exposed reinforcement steel - Jacketing & structural repair.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    elif "Phase 4" in step:
        st.markdown("""
        <div class="dark-card">
            <h3 class="accent-cyan">Phase 4: Automated Report Generation 📄</h3>
            <p><b>Objective:</b> Compile findings into an exportable, official engineering document.</p>
            <ul>
                <li>Aggregates date, location, lead engineer details, and defect annotations.</li>
                <li>Exports formatted plain text or PDF summary logs for project archiving.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ==========================================================
# SECTION 4: DASHBOARD MODULE GUIDE
# ==========================================================
elif guide_section == "🧱 Dashboard Module Guide":
    st.markdown("## 🧱 Platform Module Explorer")
    st.caption("Explore what each module inside CONSTRUCTVISION AI does.")

    m1, m2 = st.columns(2)

    with m1:
        st.markdown("""
        <div class="dark-card">
            <h4 class="accent-cyan">🏠 Home Overview</h4>
            <p style="font-size:14px; color:#94A3B8;">Executive dashboard showing global system metrics, model status, and platform architecture overview.</p>
        </div>
        <div class="dark-card">
            <h4 class="accent-cyan">📷 AI Inspection Engine</h4>
            <p style="font-size:14px; color:#94A3B8;">Upload site photos to run real-time defect identification, confidence scoring, and bounding box visualization.</p>
        </div>
        <div class="dark-card">
            <h4 class="accent-cyan">🧱 Material Knowledge Base</h4>
            <p style="font-size:14px; color:#94A3B8;">Filterable database for Concrete (M15-M40), Steel Rebar grades, and IS 10262 mix calculation tools.</p>
        </div>
        <div class="dark-card">
            <h4 class="accent-cyan">📊 Damage & Risk Analytics</h4>
            <p style="font-size:14px; color:#94A3B8;">Interactive Plotly risk heatmaps and component defect breakdown charts for data-driven decisions.</p>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown("""
        <div class="dark-card">
            <h4 class="accent-orange">🏢 3D Structural Explorer</h4>
            <p style="font-size:14px; color:#94A3B8;">Interactive structural component viewer for load paths, footings, columns, and slabs.</p>
        </div>
        <div class="dark-card">
            <h4 class="accent-orange">💰 Cost & Remediation Estimator</h4>
            <p style="font-size:14px; color:#94A3B8;">Provides instant cost projections for epoxy grouting, concrete jacketing, or plaster repairs.</p>
        </div>
        <div class="dark-card">
            <h4 class="accent-orange">📄 Audit Report Generator</h4>
            <p style="font-size:14px; color:#94A3B8;">Customizable form builder to aggregate site findings into downloadable engineering documentation.</p>
        </div>
        <div class="dark-card">
            <h4 class="accent-orange">📘 Interactive Tutorial</h4>
            <p style="font-size:14px; color:#94A3B8;">Complete platform guide, efficiency calculators, and knowledge checks (Current Module).</p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================================
# SECTION 5: AI VS MANUAL ROI CALCULATOR
# ==========================================================
elif guide_section == "⚡ AI vs. Manual ROI Calculator":
    st.markdown("## ⚡ Inspection Efficiency & ROI Calculator")
    st.caption("Calculate the time and financial savings of adopting AI-powered visual inspections for your team.")

    col_in1, col_in2 = st.columns(2)

    with col_in1:
        num_sites = st.slider("Buildings Inspected per Month:", 1, 50, 12)
        manual_hours = st.slider("Manual Inspection Hours per Building:", 2.0, 16.0, 6.0)
    with col_in2:
        engineer_rate = st.slider("Engineer Hourly Rate ($/hr or local currency):", 20, 200, 65)
        ai_speedup = st.slider("Estimated AI Inspection Time Reduction (%):", 40, 90, 75)

    # Calculations
    manual_total_hours = num_sites * manual_hours
    manual_cost = manual_total_hours * engineer_rate

    ai_total_hours = manual_total_hours * (1 - (ai_speedup / 100.0))
    ai_cost = ai_total_hours * engineer_rate

    hours_saved = manual_total_hours - ai_total_hours
    money_saved = manual_cost - ai_cost

    st.write("")
    m_c1, m_c2, m_c3 = st.columns(3)

    with m_c1:
        st.markdown(f"""
        <div class="dark-card" style="text-align:center;">
            <p style="color:#94A3B8; margin:0;">Monthly Time Saved</p>
            <h2 class="accent-cyan" style="font-size:36px; margin:5px 0;">{hours_saved:.1f} hrs</h2>
            <p style="font-size:12px; color:#10B981;">⚡ {ai_speedup}% Faster Workflows</p>
        </div>
        """, unsafe_allow_html=True)

    with m_c2:
        st.markdown(f"""
        <div class="dark-card" style="text-align:center;">
            <p style="color:#94A3B8; margin:0;">Monthly Cost Savings</p>
            <h2 class="accent-green" style="font-size:36px; margin:5px 0;">${money_saved:,.0f}</h2>
            <p style="font-size:12px; color:#10B981;">💰 Reduced Engineering Overhead</p>
        </div>
        """, unsafe_allow_html=True)

    with m_c3:
        st.markdown(f"""
        <div class="dark-card" style="text-align:center;">
            <p style="color:#94A3B8; margin:0;">Annual Projected Savings</p>
            <h2 class="accent-orange" style="font-size:36px; margin:5px 0;">${(money_saved * 12):,.0f}</h2>
            <p style="font-size:12px; color:#38BDF8;">📈 Scalable Inspection Capacity</p>
        </div>
        """, unsafe_allow_html=True)

    # Plotly Comparison Chart
    df_calc = pd.DataFrame({
        "Method": ["Traditional Manual Audit", "CONSTRUCTVISION AI"],
        "Hours Spent": [manual_total_hours, ai_total_hours],
        "Cost ($)": [manual_cost, ai_cost]
    })

    fig = px.bar(
        df_calc, x="Method", y=["Hours Spent", "Cost ($)"],
        barmode="group",
        title="Monthly Resource Consumption Comparison",
        template="plotly_dark",
        color_discrete_sequence=["#EF4444", "#38BDF8"]
    )
    fig.update_layout(paper_bgcolor="#1E293B", plot_bgcolor="#1E293B")
    st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# SECTION 6: ADVANTAGES & DISADVANTAGES (NEW SECTION)
# ==========================================================
elif guide_section == "⚖️ Advantages & Disadvantages":
    st.markdown("## ⚖️ Engineering Trade-Off Analysis: AI vs. Manual")
    st.caption("Objective analysis of benefits, limitations, and operational trade-offs of AI-driven structural inspection.")

    st.write("")

    col_adv, col_dis = st.columns(2)

    with col_adv:
        st.markdown("""
        <div class="dark-card">
            <h3 class="accent-green">✅ Advantages of CONSTRUCTVISION AI</h3>
            <ul style="line-height: 1.8; color: #CBD5E1; font-size:14px;">
                <li><b>⚡ Exponential Speed:</b> Reduces component visual inspection time from hours to seconds (< 2 sec inference).</li>
                <li><b>🎯 Elimination of Human Bias:</b> Standardizes crack severity grading based on codified engineering algorithms rather than subjective technician opinion.</li>
                <li><b>🧗 Safety Enhancement:</b> Drones and long-range telephoto cameras can inspect high-rise facades, bridges, and roof beams without risking human lives on scaffolding.</li>
                <li><b>📊 Sub-Pixel Precision:</b> Detects micro-cracks (<0.1 mm width) that are virtually invisible to the naked human eye during routine walkthroughs.</li>
                <li><b>📁 Historical Digital Twin Logs:</b> Creates searchable digital archives with temporal tracking (comparing crack growth over 6 months).</li>
                <li><b>💰 Significant Cost Savings:</b> Saves up to 75% in engineering field hours, lowering overall audit costs.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_dis:
        st.markdown("""
        <div class="dark-card">
            <h3 class="accent-red">⚠️ Disadvantages & Practical Constraints</h3>
            <ul style="line-height: 1.8; color: #CBD5E1; font-size:14px;">
                <li><b>🔍 Surface-Only Visibility:</b> Computer vision models only detect surface defects; internal voids or deep sub-surface rebar corrosion still require ultrasonic pulse or rebound hammer tests.</li>
                <li><b>💡 Environmental Sensitivity:</b> Extreme darkness, heavy dust, or mud splatters can obscure concrete surfaces and reduce AI accuracy.</li>
                <li><b>🌐 Hardware & Connectivity Needs:</b> Requires high-resolution camera gear and reliable compute power for high-throughput batch processing.</li>
                <li><b>⚖️ Legal & Certification Mandate:</b> AI predictions serve as decision-support; legal building safety sign-offs strictly mandate human engineering endorsement.</li>
                <li><b>🎨 Surface False Positives:</b> Paint scuffs, electrical cables, or cobwebs can occasionally be misclassified as cracks if lighting parameters are poor.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📊 Direct Feature Matrix Comparison")

    feature_data = {
        "Evaluation Criterion": [
            "Inspection Speed", 
            "High-Altitude Access Safety", 
            "Micro-Crack Detection (<0.1mm)", 
            "Subjective Human Bias", 
            "Internal Void Detection", 
            "Instant PDF Audit Generation", 
            "Historical Trend Tracking"
        ],
        "Traditional Manual Method": ["Slow (Hours/Days)", "High Risk (Ladders/Scaffolding)", "Low / Missed easily", "High (Varies by engineer)", "Possible (Rebound Hammer)", "Slow (Manual Typing)", "Difficult (Paper Records)"],
        "CONSTRUCTVISION AI Platform": ["Ultra-Fast (< 2 sec)", "Zero Risk (Drone/Remote Cameras)", "Ultra-High (Sub-pixel AI)", "Zero (Standardized Rules)", "Requires Hybrid NDT Tools", "Instant (Automated 1-Click)", "Seamless (3D Digital Twin)"]
    }
    st.table(pd.DataFrame(feature_data))

# ==========================================================
# SECTION 7: BEST PRACTICES
# ==========================================================
elif guide_section == "📋 Best Practices & Guidelines":
    st.markdown("## 📋 Civil Engineering Best Practices")

    col_p1, col_p2 = st.columns(2)

    with col_p1:
        st.markdown("""
        <div class="dark-card">
            <h3 class="accent-cyan">📷 Image Acquisition Rules</h3>
            <ul style="line-height:1.8; color:#CBD5E1;">
                <li><b>Perpendicular Alignment:</b> Capture structural faces at 90-degree straight-on camera angles.</li>
                <li><b>Distance Standard:</b> Maintain a distance of 0.5m to 1.5m for surface crack measurement.</li>
                <li><b>Lighting Uniformity:</b> Avoid strong direct shadows across concrete surfaces.</li>
                <li><b>Scale Reference:</b> Place a standard scale ruler or coin near critical cracks for precise measurement.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_p2:
        st.markdown("""
        <div class="dark-card">
            <h3 class="accent-orange">🏗️ Engineering Verification Rules</h3>
            <ul style="line-height:1.8; color:#CBD5E1;">
                <li><b>Human-in-the-Loop:</b> AI predictions serve as decision-support; final structural sign-offs require a licensed Civil Engineer.</li>
                <li><b>Destructive Testing:</b> Combine visual AI detection with ultrasonic pulse velocity or rebound hammer tests for deep void checks.</li>
                <li><b>Environmental Factors:</b> Cross-check crack patterns with soil settlement logs and seismic history.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ==========================================================
# SECTION 8: PRACTICE KNOWLEDGE CHECK
# ==========================================================
elif guide_section == "💡 Practice Knowledge Check":
    st.markdown("## 💡 Engineering Knowledge Check")
    st.caption("Quick 3-question self-test to verify your understanding of structural defect classification.")

    with st.form("quiz_form"):
        q1 = st.radio(
            "1. What is the primary cause of diagonal cracking near column-beam joints?",
            ["Concrete Curing Shrinkage", "Shear Stress Concentration", "Plaster Deterioration", "Superficial Paint Flaking"]
        )

        q2 = st.radio(
            "2. When spalling exposes rusted rebar, what is the recommended immediate repair?",
            ["Apply standard interior paint", "Rust removal, anti-corrosive coating & polymer concrete jacketing", "Fill with fine aggregate sand only", "No action needed"]
        )

        q3 = st.radio(
            "3. Does CONSTRUCTVISION AI replace the necessity of a certified Civil Engineer on site?",
            ["Yes, it completely replaces human engineers", "No, it acts as an intelligent decision-support assistant"]
        )

        submit_quiz = st.form_submit_button("Submit Assessment")

    if submit_quiz:
        score = 0
        if q1 == "Shear Stress Concentration": score += 1
        if q2 == "Rust removal, anti-corrosive coating & polymer concrete jacketing": score += 1
        if q3 == "No, it acts as an intelligent decision-support assistant": score += 1

        if score == 3:
            st.success("🎉 Perfect Score! 3/3 - You are ready to conduct AI site inspections.")
        else:
            st.warning(f"You scored {score}/3. Review the Best Practices module and try again.")

# ==========================================================
# SECTION 9: INTERACTIVE FAQ
# ==========================================================
elif guide_section == "❓ Interactive FAQ":
    st.markdown("## ❓ Frequently Asked Questions")

    with st.expander("📷 What types of residential structures can be inspected?"):
        st.write("CONSTRUCTVISION AI is trained on Reinforced Cement Concrete (RCC) frames, brick masonry walls, structural columns, beams, floor slabs, and foundation footings.")

    with st.expander("🤖 How does the computer vision model detect cracks?"):
        st.write("The system utilizes object detection algorithms trained on labeled civil engineering datasets to recognize contrast gradients, texture breaks, and linear defect geometries.")

    with st.expander("📄 Can I export generated inspection reports?"):
        st.write("Yes, reports can be downloaded as structured text files (.txt) or compiled directly into formatted engineering logs in the Report Generator module.")

# ==========================================================
# SECTION 10: TEAM & CREDITS
# ==========================================================
elif guide_section == "👷 Team & Credits":
    st.markdown("## 👷 Development Team")

    dev1, dev2 = st.columns(2)

    with dev1:
        st.markdown("""
        <div class="dark-card">
            <h3 class="accent-cyan">👷 Ritika Bhumkar</h3>
            <p><b>Role:</b> Civil Engineering Intern & AI Developer</p>
            <hr style="border-color:#334155;">
            <p style="font-size:14px; color:#CBD5E1;">
                • System Architecture & Streamlit UI Development<br>
                • Deep Learning Model Integration & Research<br>
                • Structural Defect Dataset Annotation<br>
                • Concrete Material Knowledge Library Setup
            </p>
        </div>
        """, unsafe_allow_html=True)

    with dev2:
        st.markdown("""
        <div class="dark-card">
            <h3 class="accent-orange">👷 Laiba Mulani</h3>
            <p><b>Role:</b> Civil Engineering Intern & AI Developer</p>
            <hr style="border-color:#334155;">
            <p style="font-size:14px; color:#CBD5E1;">
                • System Architecture & Streamlit UI Development<br>
                • Computer Vision Pipeline Design<br>
                • Structural Damage Risk Grading Rules<br>
                • Technical Documentation & Testing
            </p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================================
# FOOTER
# ==========================================================
st.write("")
st.divider()
st.markdown("""
<div style="text-align:center; padding:15px; color:#64748B; font-size:13px;">
    <b>CONSTRUCTVISION AI</b> | Designed & Developed by <b>Ritika Bhumkar</b> & <b>Laiba Mulani</b><br>
    Department of Civil Engineering Internship Project © 2026
</div>
""", unsafe_allow_html=True)