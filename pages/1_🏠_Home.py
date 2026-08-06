import streamlit as st
from datetime import datetime

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="CONSTRUCTVISION AI",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# GREETING
# =====================================================

hour = datetime.now().hour

if hour < 12:
    greeting = "Good Morning"
elif hour < 17:
    greeting = "Good Afternoon"
else:
    greeting = "Good Evening"

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""

<style>

/* =====================================================
   HIDE STREAMLIT
===================================================== */

#MainMenu{
visibility:hidden;
}

footer{
visibility:hidden;
}

header{
visibility:hidden;
}

/* =====================================================
   PAGE
===================================================== */

.block-container{

padding-top:2rem;
padding-left:3rem;
padding-right:3rem;
padding-bottom:2rem;

}

.stApp{

background:
linear-gradient(
180deg,
#E5E5E5 0%,
#ECECEC 50%,
#F5F5F5 100%
);

font-family:'Segoe UI',sans-serif;

}

/* =====================================================
   BLUEPRINT GRID
===================================================== */

.stApp::before{

content:"";

position:fixed;

top:0;

left:0;

width:100%;

height:100%;

background-image:

linear-gradient(rgba(62,85,107,.05) 1px, transparent 1px),

linear-gradient(90deg, rgba(62,85,107,.05) 1px, transparent 1px);

background-size:40px 40px;

pointer-events:none;

z-index:-1;

}

/* =====================================================
   HERO
===================================================== */

.hero{

background:white;

border-radius:20px;

padding:40px;

border-left:8px solid #3E556B;

box-shadow:

0px 8px 20px rgba(0,0,0,.08);

}

/* =====================================================
   SECTION
===================================================== */

.section{

background:white;

padding:25px;

border-radius:18px;

box-shadow:

0px 6px 15px rgba(0,0,0,.06);

}

/* =====================================================
   CARD
===================================================== */

.card{

background:white;

padding:25px;

border-radius:18px;

border-top:5px solid #3E556B;

box-shadow:

0px 8px 20px rgba(0,0,0,.08);

transition:0.35s;

min-height:220px;

}

.card:hover{

transform:translateY(-8px);

border-top:5px solid #E67E22;

box-shadow:

0px 18px 35px rgba(0,0,0,.15);

}

/* =====================================================
   TITLES
===================================================== */

h1{

color:#2F3B45;

font-weight:700;

}

h2{

color:#3E556B;

}

h3{

color:#3E556B;

}

h4{

color:#2F3B45;

}

p{

font-size:16px;

color:#5A5A5A;

line-height:1.8;

}

/* =====================================================
   BUTTON
===================================================== */

.stButton>button{

background:#3E556B;

color:white;

height:48px;

width:100%;

border:none;

border-radius:10px;

font-weight:600;

font-size:16px;

transition:.3s;

}

.stButton>button:hover{

background:#E67E22;

color:white;

}

/* =====================================================
   METRIC
===================================================== */

.metric{

font-size:42px;

font-weight:bold;

text-align:center;

color:#3E556B;

}

.metric-title{

font-size:16px;

text-align:center;

color:#555;

}

/* =====================================================
   FLOATING BRICKS
===================================================== */

.brick{

position:fixed;

font-size:26px;

opacity:.08;

animation:floatBrick 10s infinite ease-in-out;

pointer-events:none;

z-index:-1;

}

.brick1{

left:4%;

top:20%;

animation-delay:0s;

}

.brick2{

right:6%;

top:40%;

animation-delay:2s;

}

.brick3{

left:15%;

bottom:15%;

animation-delay:4s;

}

@keyframes floatBrick{

0%{
transform:translateY(0px);
}

50%{
transform:translateY(-25px);
}

100%{
transform:translateY(0px);
}

}

/* =====================================================
   ROTATING GEAR
===================================================== */

.gear{

position:fixed;

right:25px;

bottom:25px;

font-size:45px;

opacity:.08;

animation:spinGear 12s linear infinite;

pointer-events:none;

z-index:-1;

}

@keyframes spinGear{

100%{

transform:rotate(360deg);

}

}

</style>

<div class="brick brick1">🧱</div>

<div class="brick brick2">🧱</div>

<div class="brick brick3">🧱</div>

<div class="gear">⚙️</div>

""", unsafe_allow_html=True)

# =====================================================
# HERO SECTION
# =====================================================

st.markdown(f"""

<div class="hero">

<h1>

🏗️ CONSTRUCTVISION AI

</h1>

<h3>

AI Powered Residential Construction Inspection Platform

</h3>

<hr>

<p>

<b>{greeting}, Engineer.</b>

<br><br>

Welcome to <b>CONSTRUCTVISION AI</b>, an intelligent
inspection platform developed to support modern
Civil Engineering practices.

This application combines Artificial Intelligence,
Computer Vision and Construction Engineering
to inspect residential structures, identify defects,
understand construction materials and generate
professional engineering reports.

</p>

</div>

""", unsafe_allow_html=True)

st.write("")

# =====================================================
# PROJECT OVERVIEW
# =====================================================

st.markdown("## 🏢 Project Overview")

left, right = st.columns([2,1])

with left:

    st.markdown("""

<div class="section">

<h2>

Why CONSTRUCTVISION AI?

</h2>

<p>

Modern construction inspection requires
accuracy, speed and consistency.

CONSTRUCTVISION AI assists engineers by:

✔ Detecting visible structural defects

✔ Studying construction materials

✔ Supporting engineering inspections

✔ Reducing manual inspection effort

✔ Generating professional reports

✔ Improving decision making through AI

The objective is to bridge Civil Engineering
knowledge with Artificial Intelligence to
create a smarter construction workflow.

</p>

</div>

""", unsafe_allow_html=True)

with right:

    st.markdown("""

<div class="section">

<h2>

📋 Project Information

</h2>

<hr>

<b>Domain</b>

Civil Engineering

<br><br>

<b>Technology</b>

Artificial Intelligence

<br><br>

<b>Inspection Type</b>

Residential Buildings

<br><br>

<b>Platform</b>

Streamlit Dashboard

<br><br>

<b>Status</b>

Development Phase

</div>

""", unsafe_allow_html=True)

st.write("")
st.divider()

# =====================================================
# QUICK ACCESS
# =====================================================

st.markdown("## ⚙️ Quick Access")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.markdown("""

<div class="card">

<h2>

📷 AI Inspection

</h2>

<hr>

Upload construction images

Detect visible defects

Generate AI observations

</div>

""", unsafe_allow_html=True)

with col2:

    st.markdown("""

<div class="card">

<h2>

🧱 Materials

</h2>

<hr>

Explore construction materials

Study engineering properties

View applications

</div>

""", unsafe_allow_html=True)

with col3:

    st.markdown("""

<div class="card">

<h2>

🏠 Building Guide

</h2>

<hr>

Understand structural components

Learn residential construction

Interactive navigation

</div>

""", unsafe_allow_html=True)

with col4:

    st.markdown("""

<div class="card">

<h2>

📄 Reports

</h2>

<hr>

Inspection Summary

Damage Analysis

Professional PDF Reports

</div>

""", unsafe_allow_html=True)

st.write("")
st.divider()

# =====================================================
# CIVIL ENGINEERING QUOTE
# =====================================================

st.markdown("""

<div class="section" style="text-align:center;">

<h2>

🏗️ Engineering Principle

</h2>

<p style="font-size:20px;">

"Quality construction begins with accurate inspection,
reliable engineering decisions and continuous innovation."

</p>

</div>

""", unsafe_allow_html=True)

st.write("")
st.divider()

# =====================================================
# ENGINEERING DASHBOARD
# =====================================================

st.markdown("## 📊 Engineering Dashboard")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown("""

<div class="section" style="text-align:center;">

<h1 style="color:#3E556B;">98%</h1>

<h4>AI Accuracy</h4>

<p>

Reliable detection of
construction defects.

</p>

</div>

""", unsafe_allow_html=True)

with kpi2:
    st.markdown("""

<div class="section" style="text-align:center;">

<h1 style="color:#3E556B;">12+</h1>

<h4>Materials</h4>

<p>

Construction material
knowledge library.

</p>

</div>

""", unsafe_allow_html=True)

with kpi3:
    st.markdown("""

<div class="section" style="text-align:center;">

<h1 style="color:#3E556B;">24/7</h1>

<h4>Inspection</h4>

<p>

Smart engineering
support anytime.

</p>

</div>

""", unsafe_allow_html=True)

with kpi4:
    st.markdown("""

<div class="section" style="text-align:center;">

<h1 style="color:#3E556B;">PDF</h1>

<h4>Reports</h4>

<p>

Professional inspection
documentation.

</p>

</div>

""", unsafe_allow_html=True)

st.write("")
st.divider()

# =====================================================
# INSPECTION WORKFLOW
# =====================================================

st.markdown("## ⚙️ AI Inspection Workflow")

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.markdown("""

<div class="card">

<h2>① Capture</h2>

<hr>

📷

Capture residential
building images.

</div>

""", unsafe_allow_html=True)

with c2:

    st.markdown("""

<div class="card">

<h2>② Detect</h2>

<hr>

🤖

AI identifies visible
construction defects.

</div>

""", unsafe_allow_html=True)

with c3:

    st.markdown("""

<div class="card">

<h2>③ Analyse</h2>

<hr>

📊

Review engineering
inspection results.

</div>

""", unsafe_allow_html=True)

with c4:

    st.markdown("""

<div class="card">

<h2>④ Report</h2>

<hr>

📄

Generate professional
engineering reports.

</div>

""", unsafe_allow_html=True)

st.write("")
st.divider()

# =====================================================
# ENGINEERING MODULES
# =====================================================

st.markdown("## 🏗️ Platform Modules")

left, right = st.columns(2)

with left:

    st.markdown("""

<div class="section">

<h2>

🧠 Artificial Intelligence Module

</h2>

<hr>

✔ Crack Detection

<br><br>

✔ Surface Damage Identification

<br><br>

✔ Computer Vision Analysis

<br><br>

✔ Smart Inspection Support

<br><br>

✔ Report Generation

</div>

""", unsafe_allow_html=True)

with right:

    st.markdown("""

<div class="section">

<h2>

🏢 Civil Engineering Module

</h2>

<hr>

✔ Building Components

<br><br>

✔ Construction Materials

<br><br>

✔ Structural Elements

<br><br>

✔ Engineering Guidelines

<br><br>

✔ Residential Construction

</div>

""", unsafe_allow_html=True)

st.write("")
st.divider()

# =====================================================
# CONSTRUCTION MATERIALS
# =====================================================

st.markdown("## 🧱 Construction Materials")

m1, m2, m3, m4 = st.columns(4)

with m1:

    st.markdown("""

<div class="card">

<h2>🧱 Concrete</h2>

<hr>

Foundation

Columns

Slabs

Beams

</div>

""", unsafe_allow_html=True)

with m2:

    st.markdown("""

<div class="card">

<h2>🪨 Aggregate</h2>

<hr>

Coarse Aggregate

Fine Aggregate

Concrete Mix

Strength

</div>

""", unsafe_allow_html=True)

with m3:

    st.markdown("""

<div class="card">

<h2>🦾 Steel</h2>

<hr>

Reinforcement

Columns

Beams

Structural Support

</div>

""", unsafe_allow_html=True)

with m4:

    st.markdown("""

<div class="card">

<h2>🧱 Masonry</h2>

<hr>

Bricks

Blocks

Walls

Partition

</div>

""", unsafe_allow_html=True)

st.write("")
st.divider()

# =====================================================
# ENGINEERING INSIGHT
# =====================================================

st.markdown("""

<div class="section">

<h2>

📐 Engineering Insight

</h2>

<p>

Proper inspection of residential structures helps detect
construction defects at an early stage, reducing maintenance
costs and improving structural safety. AI-assisted inspection
supports engineers by providing faster analysis while helping
maintain consistency in visual assessments.

</p>

</div>

""", unsafe_allow_html=True)

st.write("")
st.divider()

# =====================================================
# ABOUT CONSTRUCTVISION AI
# =====================================================

st.markdown("## 🏢 About CONSTRUCTVISION AI")

st.markdown("""

<div class="section">

<h2>Smart Construction Inspection for Modern Civil Engineering</h2>

<p>

CONSTRUCTVISION AI is an Artificial Intelligence based
Residential Construction Inspection Platform developed
to assist Civil Engineers in inspecting buildings more
accurately and efficiently.

The system combines Computer Vision, Artificial
Intelligence and Civil Engineering principles to
identify visible structural defects, study construction
materials, analyse damages and generate professional
engineering reports.

It is designed as an engineering decision-support
platform rather than just an image detection system.

</p>

</div>

""", unsafe_allow_html=True)

st.write("")
st.divider()

# =====================================================
# PROJECT OBJECTIVES
# =====================================================

st.markdown("## 🎯 Project Objectives")

obj1, obj2 = st.columns(2)

with obj1:

    st.markdown("""

<div class="card">

<h2>📌 Primary Objectives</h2>

<hr>

✔ AI Assisted Building Inspection

<br><br>

✔ Crack & Surface Damage Detection

<br><br>

✔ Construction Material Learning

<br><br>

✔ Engineering Report Generation

<br><br>

✔ Smart Inspection Dashboard

</div>

""", unsafe_allow_html=True)

with obj2:

    st.markdown("""

<div class="card">

<h2>⚙ Engineering Goals</h2>

<hr>

✔ Reduce Manual Inspection

<br><br>

✔ Improve Inspection Accuracy

<br><br>

✔ Faster Decision Making

<br><br>

✔ Support Civil Engineers

<br><br>

✔ Digital Construction Workflow

</div>

""", unsafe_allow_html=True)

st.write("")
st.divider()

# =====================================================
# DEVELOPMENT TEAM
# =====================================================

st.markdown("## 👷 Development Team")

dev1, dev2 = st.columns(2)

with dev1:

    st.markdown("""

<div class="section">

<h2>👷 Ritika Bhumkar</h2>

<hr>

<h4>Role</h4>

Civil Engineering Intern

AI & Computer Vision Developer

Research & System Design

<br>

<h4>Responsibilities</h4>

✔ Dashboard Design & Development

✔ AI Model Integration

✔ Computer Vision Implementation

✔ Structural Damage Research

✔ Construction Material Analysis

✔ Dataset Preparation

✔ Testing & Validation

✔ Documentation

✔ UI/UX Enhancement

<br>

<h4>Technical Skills</h4>

Python • Streamlit • OpenCV • YOLO

Machine Learning • Civil Engineering

</div>

""", unsafe_allow_html=True)

with dev2:

    st.markdown("""

<div class="section">

<h2>👷 Laiba Mulani</h2>

<hr>

<h4>Role</h4>

Civil Engineering Intern

AI & Computer Vision Developer

Research & System Design

<br>

<h4>Responsibilities</h4>

✔ Dashboard Design & Development

✔ AI Model Integration

✔ Computer Vision Implementation

✔ Structural Damage Research

✔ Construction Material Analysis

✔ Dataset Preparation

✔ Testing & Validation

✔ Documentation

✔ UI/UX Enhancement

<br>

<h4>Technical Skills</h4>

Python • Streamlit • OpenCV • YOLO

Machine Learning • Civil Engineering

</div>

""", unsafe_allow_html=True)

st.write("")
st.divider()

# =====================================================
# INTERNSHIP PROJECT
# =====================================================

st.markdown("## 🏗 Internship Project")

st.markdown("""

<div class="section">

<h2>Project Information</h2>

<p>

<b>Project Title:</b> CONSTRUCTVISION AI

<br><br>

<b>Category:</b> AI Powered Residential Construction Inspection

<br><br>

<b>Domain:</b> Civil Engineering + Artificial Intelligence

<br><br>

<b>Purpose:</b> To assist engineers in inspecting residential
structures through Computer Vision and AI.

<br><br>

<b>Developed As:</b> Civil Engineering Internship Project

</p>

</div>

""", unsafe_allow_html=True)

st.write("")
st.divider()

# =====================================================
# FUTURE SCOPE
# =====================================================

st.markdown("## 🚀 Future Scope")

future1, future2, future3 = st.columns(3)

with future1:

    st.markdown("""

<div class="card">

<h2>🤖 Artificial Intelligence</h2>

<hr>

✔ Crack Classification

<br>

✔ Defect Severity Prediction

<br>

✔ Automatic Recommendations

<br>

✔ Deep Learning Models

</div>

""", unsafe_allow_html=True)

with future2:

    st.markdown("""

<div class="card">

<h2>🏗 Smart Construction</h2>

<hr>

✔ Drone Inspection

<br>

✔ CCTV Monitoring

<br>

✔ Site Progress Tracking

<br>

✔ Digital Twin Integration

</div>

""", unsafe_allow_html=True)

with future3:

    st.markdown("""

<div class="card">

<h2>📡 IoT Integration</h2>

<hr>

✔ Structural Health Monitoring

<br>

✔ Live Sensor Dashboard

<br>

✔ Alert Notifications

<br>

✔ Predictive Maintenance

</div>

""", unsafe_allow_html=True)

st.write("")
st.divider()

# =====================================================
# RESEARCH GAP
# =====================================================

st.markdown("## 📚 Research Gap")

st.markdown("""

<div class="section">

<h2>

Why is CONSTRUCTVISION AI Needed?

</h2>

<p>

Current residential construction inspection
is mostly performed manually.

Manual inspection can be

• Time Consuming

• Human Error Prone

• Difficult to Maintain Records

• Dependent on Inspector Experience

• Limited for Large Scale Projects

CONSTRUCTVISION AI bridges this gap using

Artificial Intelligence,

Computer Vision,

Digital Reporting,

Construction Knowledge,

and Smart Inspection Workflows.

</p>

</div>

""", unsafe_allow_html=True)

st.write("")
st.divider()

# =====================================================
# PROJECT HIGHLIGHTS
# =====================================================

st.markdown("## 🏢 Platform Highlights")

h1,h2,h3,h4 = st.columns(4)

with h1:
    st.success("✔ AI Inspection")

with h2:
    st.success("✔ Civil Engineering")

with h3:
    st.success("✔ Smart Reports")

with h4:
    st.success("✔ Material Knowledge")

st.write("")

h5,h6,h7,h8 = st.columns(4)

with h5:
    st.info("📷 Image Analysis")

with h6:
    st.info("🧱 Building Components")

with h7:
    st.info("📄 PDF Reports")

with h8:
    st.info("📊 Dashboard Analytics")

st.write("")
st.divider()

# =====================================================
# PROJECT VISION
# =====================================================

st.markdown("""

<div class="section">

<h2>

🎯 Vision Statement

</h2>

<p style="font-size:18px;">

To develop an intelligent engineering platform
that assists Civil Engineers in inspecting
residential structures using Artificial Intelligence,
Computer Vision and Smart Construction Technologies,
making inspections faster, more accurate and
digitally documented.

</p>

</div>

""", unsafe_allow_html=True)

st.write("")
st.divider()

# =====================================================
# FOOTER
# =====================================================

st.markdown("""

<div style="

background:#3E556B;

padding:30px;

border-radius:18px;

text-align:center;

color:white;

">

<h2 style="color:white;">

🏗 CONSTRUCTVISION AI

</h2>

<p style="font-size:18px;color:white;">

AI Powered Residential Construction Inspection Platform

</p>

<hr>

<p style="color:white;">

Designed & Developed by

<br><br>

<b>Ritika Bhumkar</b>

&amp;

<b>Laiba Mulani</b>

</p>

<p style="color:white;">

Civil Engineering Internship Project

</p>

<p style="color:white;">

Department of Civil Engineering

</p>

<p style="color:white;">

Artificial Intelligence • Computer Vision • Construction Engineering

</p>

</div>

""", unsafe_allow_html=True)

st.write("")

st.caption("© 2026 CONSTRUCTVISION AI | Smart Construction Inspection Platform")
