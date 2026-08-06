import streamlit as st
from streamlit.components.v1 import html

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Tutorial | CONSTRUCTVISION AI",
    page_icon="📘",
    layout="wide"
)

# ==========================================================
# PROFESSIONAL CIVIL CSS
# ==========================================================

st.markdown("""
<style>

/* ---------- Background ---------- */

.stApp{
    background:linear-gradient(135deg,#ECECEC,#D9D9D9,#F3F3F3);
}

/* ---------- Hide Streamlit ---------- */

#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
header{visibility:hidden;}

/* ---------- Sidebar ---------- */

section[data-testid="stSidebar"]{
    background:#0F1E2E;
}

section[data-testid="stSidebar"] *{
    color:white;
}

/* ---------- Main Heading ---------- */

.main-title{

    font-size:50px;

    font-weight:800;

    color:#243447;

    text-align:center;

    margin-bottom:5px;

}

.sub-title{

    font-size:22px;

    color:#5A6773;

    text-align:center;

    margin-bottom:40px;

}

/* ---------- White Cards ---------- */

.card{

    background:#ffffff;

    color:#404040;

    border:1px solid #d8d8d8;

    padding:30px;

    border-radius:22px;

    border-left:8px solid #3E556B;

    box-shadow:0px 8px 25px rgba(0,0,0,.12);

    transition:.35s;

    margin-bottom:20px;

}

.card:hover{

    transform:translateY(-6px);

}

/* ---------- Section ---------- */

.section{

    background:#ffffff;

    color:#404040;

    border:1px solid #d8d8d8;

    padding:30px;

    border-radius:20px;

    box-shadow:0px 5px 20px rgba(0,0,0,.08);

    margin-top:20px;

    margin-bottom:20px;

}

/* ---------- FORCE ALL TITLES ---------- */

h1,
h2,
h3,
h4,
h5,
h6{

    color:#243447 !important;

    opacity:1 !important;

    visibility:visible !important;

    display:block !important;

    font-weight:700 !important;

}

.card h1,
.card h2,
.card h3,
.card h4,
.card h5,
.card h6{

    color:#243447 !important;

}

.feature h1,
.feature h2,
.feature h3{

    color:#243447 !important;

}

.section h1,
.section h2,
.section h3{

    color:#243447 !important;

}

.main-title{

    color:#243447 !important;

}

.sub-title{

    color:#5A6773 !important;

}

p{

    color:#525252;

    font-size:18px;

    line-height:1.9;

}

/* ---------- Feature Box ---------- */

.feature{

    background:#ffffff;

    color:#404040;

    border:1px solid #d8d8d8;

    padding:25px;

    border-radius:18px;

    border-top:6px solid #3E556B;

    box-shadow:0px 6px 18px rgba(0,0,0,.10);

    text-align:center;

    height:260px;

}

.feature h3{

    color:#243447;

}

.feature p{

    font-size:16px;

}

/* ---------- Footer ---------- */

.footer{

    background:#3E556B;

    border-radius:20px;

    padding:35px;

    color:white;

    text-align:center;

}

.footer h2{

    color:white;

}

.footer p{

    color:white;

}

/* ---------- Floating Civil Icons ---------- */

.floating{

position:fixed;

font-size:32px;

opacity:.10;

animation:float 12s linear infinite;

pointer-events:none;

z-index:0;

}

.f1{left:5%;top:15%;animation-delay:0s;}
.f2{left:92%;top:22%;animation-delay:2s;}
.f3{left:12%;top:75%;animation-delay:5s;}
.f4{left:86%;top:82%;animation-delay:8s;}
.f5{left:50%;top:10%;animation-delay:3s;}

@keyframes float{

0%{transform:translateY(0px);}
50%{transform:translateY(-25px);}
100%{transform:translateY(0px);}

}

</style>
""",unsafe_allow_html=True)

# ==========================================================
# FLOATING CIVIL ANIMATION
# ==========================================================

html("""

<div class="floating f1">🧱</div>

<div class="floating f2">🏗️</div>

<div class="floating f3">🪨</div>

<div class="floating f4">🏢</div>

<div class="floating f5">📐</div>

""",height=0)

# ==========================================================
# HEADER
# ==========================================================

st.markdown("""

<div class="main-title">

🏗️ CONSTRUCTVISION AI

</div>

<div class="sub-title">

Tutorial & User Guide

</div>

""",unsafe_allow_html=True)

st.markdown("""

<div class="section">

<h2>📘 Platform Overview</h2>

<p>

<b>CONSTRUCTVISION AI</b> is an Artificial Intelligence powered
Civil Engineering platform developed for residential building
inspection.

The system combines Computer Vision, Artificial Intelligence,
Image Processing and Civil Engineering knowledge to assist
engineers during structural inspection.

This tutorial explains how to use every module of the dashboard
and understand the complete inspection workflow before starting
your project.

</p>

</div>

""",unsafe_allow_html=True)
# ==========================================================
# HOW CONSTRUCTVISION AI WORKS
# ==========================================================

st.markdown("## 🏗 Inspection Workflow")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("""
    <div class="feature">
    <h2>📷</h2>
    <h3>Capture Image</h3>
    <p>
    Upload a clear image of the residential building component
    for inspection.
    </p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="feature">
    <h2>🧠</h2>
    <h3>AI Analysis</h3>
    <p>
    Computer Vision analyses the uploaded image and detects
    visible construction defects.
    </p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="feature">
    <h2>🏗️</h2>
    <h3>Engineering Review</h3>
    <p>
    The detected component is compared with civil engineering
    standards and construction knowledge.
    </p>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="feature">
    <h2>📄</h2>
    <h3>Generate Report</h3>
    <p>
    A professional inspection summary is generated for further
    engineering decisions.
    </p>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.divider()

# ==========================================================
# DASHBOARD MODULES
# ==========================================================

st.markdown("## 🧱 Dashboard Modules")

left, right = st.columns(2)

with left:

    st.markdown("""

<div class="card">

<h3>🏠 Home</h3>

Overview of the complete CONSTRUCTVISION AI platform,
project objectives and quick navigation.

</div>

""", unsafe_allow_html=True)

    st.markdown("""

<div class="card">

<h3>📘 Tutorial</h3>

Learn the inspection workflow, dashboard modules and
recommended usage before starting analysis.

</div>

""", unsafe_allow_html=True)

    st.markdown("""

<div class="card">

<h3>🏢 3D Building</h3>

Explore residential structural components using an
interactive building model.

</div>

""", unsafe_allow_html=True)

    st.markdown("""

<div class="card">

<h3>🧱 Materials</h3>

Study commonly used residential construction materials,
their applications and engineering properties.

</div>

""", unsafe_allow_html=True)

with right:

    st.markdown("""

<div class="card">

<h3>📷 AI Inspection</h3>

Upload building images for AI-powered structural
inspection and defect detection.

</div>

""", unsafe_allow_html=True)

    st.markdown("""

<div class="card">

<h3>📊 Damage Analysis</h3>

Analyse detected defects and understand their possible
impact on structural performance.

</div>

""", unsafe_allow_html=True)

    st.markdown("""

<div class="card">

<h3>💰 Cost Estimation</h3>

Estimate approximate repair cost based on detected
damage severity.

</div>

""", unsafe_allow_html=True)

    st.markdown("""

<div class="card">

<h3>📄 Reports</h3>

Generate organized inspection reports for engineering
documentation and project records.

</div>

""", unsafe_allow_html=True)

st.write("")
st.divider()

# ==========================================================
# EXPECTED OUTPUT
# ==========================================================

st.markdown("## 📈 Expected Output")

a, b, c = st.columns(3)

with a:

    st.markdown("""

<div class="feature">

<h2>🔍</h2>

<h3>AI Detection</h3>

<p>

• Structural Component

<br>

• Visible Defects

<br>

• Inspection Confidence

</p>

</div>

""", unsafe_allow_html=True)

with b:

    st.markdown("""

<div class="feature">

<h2>📋</h2>

<h3>Engineering Summary</h3>

<p>

• Damage Description

<br>

• Material Information

<br>

• Structural Remarks

</p>

</div>

""", unsafe_allow_html=True)

with c:

    st.markdown("""

<div class="feature">

<h2>📄</h2>

<h3>Professional Report</h3>

<p>

• Inspection Report

<br>

• Analysis Results

<br>

• Documentation

</p>

</div>

""", unsafe_allow_html=True)

st.write("")
st.divider()
# ==========================================================
# ENGINEERING BEST PRACTICES
# ==========================================================

st.markdown("## 📋 Best Practices Before Inspection")

left,right = st.columns(2)

with left:

    st.markdown("""

<div class="card">

<h3>📷 Image Quality</h3>

<ul>

<li>Capture images in good daylight.</li>

<li>Keep the camera stable.</li>

<li>Avoid blurry photographs.</li>

<li>Focus on the structural component.</li>

<li>Capture the complete damaged region.</li>

</ul>

</div>

""",unsafe_allow_html=True)

with right:

    st.markdown("""

<div class="card">

<h3>🏗 Engineering Recommendations</h3>

<ul>

<li>Verify AI results with site observations.</li>

<li>Inspect multiple images when required.</li>

<li>Review material properties carefully.</li>

<li>Generate reports after inspection.</li>

<li>Maintain inspection records for future reference.</li>

</ul>

</div>

""",unsafe_allow_html=True)

st.write("")
st.divider()

# ==========================================================
# QUICK FAQ
# ==========================================================

st.markdown("## ❓ Frequently Asked Questions")

with st.expander("📷 Which images should I upload?"):

    st.write("""

Upload clear photographs of residential building
components such as walls, beams, columns, slabs,
footings or structural joints.

""")

with st.expander("🤖 Does AI replace Civil Engineers?"):

    st.write("""

No.

CONSTRUCTVISION AI is an engineering support tool.
Final decisions should always be taken by qualified
Civil Engineers.

""")

with st.expander("📄 What will I receive after inspection?"):

    st.write("""

• AI Detection Result

• Damage Analysis

• Engineering Summary

• Construction Material Information

• Inspection Report

""")

st.write("")
st.divider()

# ==========================================================
# DEVELOPERS
# ==========================================================

st.markdown("## 👷 Development Team")

d1,d2 = st.columns(2)

with d1:

    st.markdown("""

<div class="card">

<h2>👷 Ritika Bhumkar</h2>

<hr>

<b>Role</b>

<br>

Civil Engineering Intern

<br><br>

<b>Project Contributions</b>

<ul>

<li>Dashboard Development</li>

<li>Artificial Intelligence Integration</li>

<li>Computer Vision Research</li>

<li>Construction Material Research</li>

<li>Structural Defect Analysis</li>

<li>Testing & Validation</li>

<li>Technical Documentation</li>

<li>UI Design & Development</li>

</ul>

</div>

""",unsafe_allow_html=True)

with d2:

    st.markdown("""

<div class="card">

<h2>👷 Laiba Mulani</h2>

<hr>

<b>Role</b>

<br>

Civil Engineering Intern

<br><br>

<b>Project Contributions</b>

<ul>

<li>Dashboard Development</li>

<li>Artificial Intelligence Integration</li>

<li>Computer Vision Research</li>

<li>Construction Material Research</li>

<li>Structural Defect Analysis</li>

<li>Testing & Validation</li>

<li>Technical Documentation</li>

<li>UI Design & Development</li>

</ul>

</div>

""",unsafe_allow_html=True)

st.write("")
st.divider()

# ==========================================================
# READY TO START
# ==========================================================

st.markdown("""

<div class="section">

<h2 style="text-align:center;">

🚀 Ready to Start Your Inspection?

</h2>

<p style="text-align:center;">

You are now familiar with the CONSTRUCTVISION AI workflow.

Proceed to the <b>AI Inspection</b> module from the
sidebar to begin analysing residential construction
images using Artificial Intelligence.

</p>

</div>

""",unsafe_allow_html=True)

st.success("✔ Tutorial Completed Successfully. You are ready to use CONSTRUCTVISION AI.")

st.write("")
st.divider()

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("""

<div class="footer">

<h2>🏗 CONSTRUCTVISION AI</h2>

<p>

AI Powered Residential Construction Inspection Platform

</p>

<hr>

<p>

Designed & Developed By

<br><br>

<b>Ritika Bhumkar</b>

&nbsp;&nbsp;|&nbsp;&nbsp;

<b>Laiba Mulani</b>

</p>

<p>

Civil Engineering Internship Project

</p>

<p>

Artificial Intelligence • Computer Vision • Civil Engineering

</p>

</div>

""",unsafe_allow_html=True)

st.write("")

st.caption("© 2026 CONSTRUCTVISION AI | Professional Engineering Dashboard")
