from datetime import date, datetime
import json
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# =========================================================
# 1. PAGE CONFIGURATION & DARK GLASS UI THEME
# =========================================================
st.set_page_config(
    page_title="Inspection History & Audit Logs | CONSTRUCTVISION AI",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Dark Glass UI CSS
st.markdown("""
<style>
    /* Glowing Dark Radial Background */
    .stApp {
        background: radial-gradient(circle at 50% -20%, #172437 0%, #080D14 60%, #03060A 100%) !important;
        color: #E2E8F0;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Hide Streamlit Default Header/Footer */
    #MainMenu, footer, header {
        visibility: hidden;
    }

    /* Dark Glass Cards & Containers */
    .dark-card, .metric-box, .story-card {
        background: rgba(13, 20, 32, 0.78) !important;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.09) !important;
        border-radius: 16px !important;
        padding: 22px !important;
        margin-bottom: 18px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        transition: all 0.3s ease;
    }
    .dark-card:hover, .story-card:hover {
        border-color: rgba(56, 189, 248, 0.4) !important;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.15);
        transform: translateY(-2px);
    }

    /* Typography & Accents */
    h1, h2, h3, h4 {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }
    .accent-cyan { color: #38BDF8 !important; text-shadow: 0 0 12px rgba(56, 189, 248, 0.4); }
    .accent-orange { color: #F97316 !important; text-shadow: 0 0 12px rgba(249, 115, 22, 0.4); }
    .accent-green { color: #10B981 !important; text-shadow: 0 0 12px rgba(16, 185, 129, 0.4); }
    .accent-red { color: #EF4444 !important; text-shadow: 0 0 12px rgba(239, 68, 68, 0.4); }

    /* Custom Badges */
    .badge-blue { background: rgba(37, 99, 235, 0.25); color: #60A5FA; border: 1px solid #2563EB; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; }
    .badge-success { background: rgba(16, 185, 129, 0.25); color: #6EE7B7; border: 1px solid #10B981; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; }
    .badge-warning { background: rgba(249, 115, 22, 0.25); color: #FDBA74; border: 1px solid #F97316; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; }
    .badge-critical { background: rgba(239, 68, 68, 0.25); color: #FCA5A5; border: 1px solid #EF4444; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; }

    /* Custom Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.4rem !important;
        box-shadow: 0 0 15px rgba(2, 132, 199, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #F97316 0%, #EA580C 100%) !important;
        box-shadow: 0 0 20px rgba(249, 115, 22, 0.5) !important;
        transform: translateY(-1px);
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 2. SESSION STATE & HISTORICAL DATASET INGESTION
# =========================================================
gps_info = st.session_state.get("selected_location_info", {
    "site_code": "CV-RES-01",
    "label": "Navi Peth Commercial Center",
    "lat": 17.6599,
    "lon": 75.9064,
    "road": "Rupa Bhavani Road",
    "type": "Commercial High-Rise",
    "risk_score": 88
})

if "selected_component" not in st.session_state:
    st.session_state.selected_component = "Foundation Footing (F-01)"

@st.cache_data
def load_historical_data():
    return [
        {
            "Record_ID": "INSP-2026-0901",
            "Date": date(2026, 8, 22),
            "Project": f"{gps_info.get('site_code','CV-RES-01')}: {gps_info.get('label','Navi Peth Center')}",
            "Inspection_Type": "Model & Sensor Calibration Audit",
            "Inspector": "Er. Ritika Bhumkar & Er. Laiba Mulani",
            "Defects_Found": 0,
            "AI_Confidence": 0.99,
            "Status": "Safe",
            "Severity": "None",
            "Image_Ref": "https://images.unsplash.com/photo-1541888946425-d0fbb186a5b7?w=500",
            "Notes": "Solapur HQ core repository model sync verified. Sub-pixel scale calibrated to 0.15 mm/px."
        },
        {
            "Record_ID": "INSP-2026-0899",
            "Date": date(2026, 8, 18),
            "Project": "CV-RES-01: Navi Peth Commercial Center",
            "Inspection_Type": "Structural Integrity & Rebar Scan",
            "Inspector": "Er. Ritika Bhumkar (Lead Dev)",
            "Defects_Found": 2,
            "AI_Confidence": 0.96,
            "Status": "Review Required",
            "Severity": "Medium",
            "Image_Ref": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=500",
            "Notes": "0.28mm flexural shear crack noted near Column C-12 Level 1 joint. Epoxy grouting scheduled."
        },
        {
            "Record_ID": "INSP-2026-0891",
            "Date": date(2026, 8, 14),
            "Project": "CV-FLY-03: Saat Rasta Traffic Flyover",
            "Inspection_Type": "Concrete Deck Shear & Crack Scan",
            "Inspector": "Er. Laiba Mulani (Lead Dev)",
            "Defects_Found": 4,
            "AI_Confidence": 0.94,
            "Status": "Critical Alert",
            "Severity": "High",
            "Image_Ref": "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=500",
            "Notes": "Concrete spalling with rebar exposure near Pier 2 base. Immediate shoring and polymer mortar patching required."
        },
        {
            "Record_ID": "INSP-2026-0888",
            "Date": date(2026, 8, 10),
            "Project": "CV-INST-02: Sangameshwar Campus Tower",
            "Inspection_Type": "Masonry Joint & Plaster Integrity",
            "Inspector": "Er. Ritika Bhumkar",
            "Defects_Found": 1,
            "AI_Confidence": 0.98,
            "Status": "Safe",
            "Severity": "Low",
            "Image_Ref": "https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=500",
            "Notes": "Hairline mortar joint shrinkage crack (0.08mm) observed. Logged for routine surface seal."
        },
        {
            "Record_ID": "INSP-2026-0882",
            "Date": date(2026, 8, 5),
            "Project": "CV-IND-05: MIDC Logistics Hub",
            "Inspection_Type": "Foundation Plinth Settlement Scan",
            "Inspector": "Drone Autonomous Unit #02",
            "Defects_Found": 0,
            "AI_Confidence": 0.99,
            "Status": "Safe",
            "Severity": "None",
            "Image_Ref": "https://images.unsplash.com/photo-1590069261209-f8e9b8642343?w=500",
            "Notes": "Sub-grade settlement within IS 456 safe limit (< 0.05° tilt). Hydrostatic pressure nominal."
        }
    ]

preset_data = load_historical_data()

# Merge live session inspection records if user ran AI Inspection in current session
session_records = st.session_state.get("inspection_history_records", [])
all_records = []

if session_records:
    for idx, r in enumerate(session_records):
        all_records.append({
            "Record_ID": f"LIVE-2026-{idx+101:04d}",
            "Date": datetime.now().date(),
            "Project": f"{r.get('site_code','CV-SITE')}: {r.get('location','Solapur Field Site')}",
            "Inspection_Type": "Live Computer Vision AI Audit",
            "Inspector": "Er. Ritika Bhumkar & Er. Laiba Mulani",
            "Defects_Found": r.get("total_defects", 0),
            "AI_Confidence": 0.96,
            "Status": "Critical Alert" if "CRITICAL" in str(r.get("verdict","")).upper() else ("Review Required" if "ACTION" in str(r.get("verdict","")).upper() else "Safe"),
            "Severity": "High" if r.get("max_crack_width_mm", 0) > 0.3 else ("Medium" if r.get("max_crack_width_mm", 0) > 0.1 else "Low"),
            "Image_Ref": "https://images.unsplash.com/photo-1541888946425-d0fbb186a5b7?w=500",
            "Notes": f"Live scan verdict: {r.get('verdict','NOMINAL')}. Max crack width: {r.get('max_crack_width_mm',0.0):.2f} mm. Est Cost: ₹{r.get('total_repair_cost_inr',0):,.0f}"
        })

all_records.extend(preset_data)
df_history = pd.DataFrame(all_records)

# =========================================================
# 3. SIDEBAR & HEADER
# =========================================================
with st.sidebar:
    st.markdown("### 📜 **Audit History Controls**")
    st.caption("Centralized Records & Developer System Story")
    st.divider()

    show_origin_story = st.checkbox("💡 Show Project Origin & Creation Story", value=True)
    st.divider()

    st.markdown("#### 🔗 Linked Active Target")
    st.caption(f"• **Active Site:** `{gps_info.get('site_code','CV-SITE')}`")
    st.caption(f"• **3D Member:** `{st.session_state.selected_component}`")

    st.divider()
    st.caption("Department of Civil Engineering © 2026")

st.title("📜 Inspection History & Compliance Audit Logs")
st.caption("ConstructVision AI — Historical site inspection archives, automated audit logs, and civil engineering creation story.")

# Synchronized Site Bar
st.markdown(f"""
<div class="dark-card" style="padding: 12px 20px !important; margin-bottom: 20px !important;">
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
        <div>
            <span class="badge-blue">📍 ACTIVE SYNC SITE</span>
            <span style="font-weight:700; font-size:16px; margin-left:10px;">{gps_info.get('site_code', 'CV-SITE')}: {gps_info.get('label', 'Solapur Field Site')}</span>
        </div>
        <div style="font-size:13px; color:#94A3B8;">
            <b>Active 3D Member:</b> <span class="accent-cyan">{st.session_state.selected_component}</span> | 
            <b>Database Archives:</b> <span class="accent-green">{len(df_history)} Total Logs</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# 4. PROJECT ORIGIN & CREATION STORY SECTION
# =========================================================
if show_origin_story:
    st.markdown("""
    <div class="story-card" style="border-left: 5px solid #38BDF8 !important;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap;">
            <h2 class="accent-cyan" style="margin:0;">💡 The Genesis of CONSTRUCTVISION AI</h2>
            <span class="badge-blue">CIVIL ENGINEERING INNOVATION STORY</span>
        </div>
        <p style="font-size:15px; color:#E2E8F0; margin-top:12px; line-height:1.7;">
            <b>Why was CONSTRUCTVISION AI created?</b><br>
            In traditional Indian civil engineering site practice across Maharashtra, structural audits of high-rise RCC columns, bridges, and housing developments relied heavily on <b>manual visual walkthroughs, handheld magnifying crack scales, chalk markings, and paper clipboards</b>.
        </p>
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:15px; margin-top:15px;">
            <div style="background:rgba(15,23,42,0.6); padding:14px; border-radius:10px; border:1px solid rgba(255,255,255,0.06);">
                <h4 class="accent-orange" style="margin:0 0 6px 0;">⚠️ The Real-World Civil Challenge</h4>
                <p style="font-size:13px; color:#94A3B8; margin:0;">
                    • Subjective human engineer bias when measuring sub-millimeter shear cracks.<br>
                    • Hazardous scaffolding climb work to inspect high-altitude beams & pier caps.<br>
                    • Slow report typing in Word/Excel taking 4 to 6 hours per component.<br>
                    • Missing temporal records to track crack growth over 12 to 24 months.
                </p>
            </div>
            <div style="background:rgba(15,23,42,0.6); padding:14px; border-radius:10px; border:1px solid rgba(255,255,255,0.06);">
                <h4 class="accent-green" style="margin:0 0 6px 0;">🚀 The AI Vision & Solution</h4>
                <p style="font-size:13px; color:#94A3B8; margin:0;">
                    • <b>Computer Vision Sub-Pixel Segmentation:</b> Instant metric measurement ($\text{mm}$) of micro-cracks (<0.1mm) via phone or drone camera.<br>
                    • <b>IS 456 & Eurocode Integration:</b> Codified safety verdict & repair costing.<br>
                    • <b>Live 3D Digital Twin & IoT:</b> Real-time spatial mapping with strain gauges.<br>
                    • <b>Automated Audit Export:</b> Instant GST tax invoicing & downloadable PDF/CSV logs.
                </p>
            </div>
        </div>
        <div style="margin-top:14px; font-size:13px; color:#CBD5E1; border-top:1px solid rgba(255,255,255,0.08); padding-top:10px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap;">
            <span><b>Lead Developers & System Architects:</b> <span class="accent-cyan">Er. Ritika Bhumkar</span> & <span class="accent-orange">Er. Laiba Mulani</span></span>
            <span style="color:#94A3B8;">Department of Civil Engineering © 2026</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# 5. ADVANCED SEARCH & FILTER CONTROLS
# =========================================================
st.markdown("### 🔎 Query & Filter Historical Inspection Logs")

with st.expander("🛠️ Advanced Search Controls & Date Range Filter", expanded=True):
    col1, col2, col3, col4 = st.columns([2, 2, 2, 3])

    with col1:
        project_filter = st.selectbox(
            "Project Site / Location:",
            ["All Sites"] + sorted(list(df_history["Project"].unique()))
        )

    with col2:
        status_filter = st.selectbox(
            "Safety Verdict Status:",
            ["All Statuses"] + sorted(list(df_history["Status"].unique()))
        )

    with col3:
        severity_filter = st.selectbox(
            "Severity Level Grade:",
            ["All Severities", "High", "Medium", "Low", "None"]
        )

    with col4:
        search_term = st.text_input(
            "🔍 Search Keyword (Record ID, Inspector, Notes):", ""
        )

    date_col1, date_col2 = st.columns(2)
    with date_col1:
        start_date = st.date_input("Start Date Filter:", date(2026, 8, 1))
    with date_col2:
        end_date = st.date_input("End Date Filter:", date(2026, 8, 31))

# Apply Filter Logic
filtered_df = df_history.copy()

if project_filter != "All Sites":
    filtered_df = filtered_df[filtered_df["Project"] == project_filter]

if status_filter != "All Statuses":
    filtered_df = filtered_df[filtered_df["Status"] == status_filter]

if severity_filter != "All Severities":
    filtered_df = filtered_df[filtered_df["Severity"] == severity_filter]

filtered_df = filtered_df[
    (filtered_df["Date"] >= start_date) & (filtered_df["Date"] <= end_date)
]

if search_term:
    search_query = search_term.lower()
    filtered_df = filtered_df[
        filtered_df["Record_ID"].str.lower().str.contains(search_query)
        | filtered_df["Inspector"].str.lower().str.contains(search_query)
        | filtered_df["Notes"].str.lower().str.contains(search_query)
        | filtered_df["Project"].str.lower().str.contains(search_query)
    ]

# =========================================================
# 6. EXECUTIVE SUMMARY METRIC KPIS
# =========================================================
st.divider()

m1, m2, m3, m4, m5 = st.columns(5)

total_records = len(filtered_df)
safe_count = len(filtered_df[filtered_df["Status"] == "Safe"])
review_count = len(filtered_df[filtered_df["Status"] == "Review Required"])
alert_count = len(filtered_df[filtered_df["Status"] == "Critical Alert"])
avg_confidence = (
    f"{filtered_df['AI_Confidence'].mean() * 100:.1f}%"
    if total_records > 0
    else "N/A"
)

with m1:
    st.markdown(f"""
    <div class="dark-card">
        <span style="font-size:11px; color:#94A3B8; text-transform:uppercase;">Total Inspections</span>
        <h2 class="accent-cyan" style="margin:4px 0 0 0;">{total_records} Logs</h2>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="dark-card">
        <span style="font-size:11px; color:#94A3B8; text-transform:uppercase;">Safe Sites</span>
        <h2 class="accent-green" style="margin:4px 0 0 0;">{safe_count} Sites</h2>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="dark-card">
        <span style="font-size:11px; color:#94A3B8; text-transform:uppercase;">Review Required</span>
        <h2 class="accent-orange" style="margin:4px 0 0 0;">{review_count} Sites</h2>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class="dark-card">
        <span style="font-size:11px; color:#94A3B8; text-transform:uppercase;">Critical Alerts</span>
        <h2 class="accent-red" style="margin:4px 0 0 0;">{alert_count} Alerts</h2>
    </div>
    """, unsafe_allow_html=True)

with m5:
    st.markdown(f"""
    <div class="dark-card">
        <span style="font-size:11px; color:#94A3B8; text-transform:uppercase;">Avg Model Accuracy</span>
        <h2 style="margin:4px 0 0 0; color:#FFFFFF;">{avg_confidence}</h2>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# 7. INTERACTIVE DATA TABLE ARCHIVE
# =========================================================
st.markdown("### 📋 Inspection Master Audit Trail")

if not filtered_df.empty:
    st.dataframe(
        filtered_df,
        column_config={
            "Record_ID": st.column_config.TextColumn("Record ID", width="small"),
            "Date": st.column_config.DateColumn("Date", format="DD-MM-YYYY"),
            "Project": st.column_config.TextColumn("Site & Location Tag", width="medium"),
            "Inspection_Type": st.column_config.TextColumn("Assessment Type", width="medium"),
            "Inspector": st.column_config.TextColumn("Inspector / Developers", width="medium"),
            "AI_Confidence": st.column_config.ProgressColumn("AI Model Precision", format="%.0f%%", min_value=0, max_value=1),
            "Status": st.column_config.SelectboxColumn(
                "Verdict Status",
                options=["Safe", "Review Required", "Critical Alert"],
                required=True,
            ),
            "Severity": st.column_config.TextColumn("Severity"),
            "Image_Ref": st.column_config.LinkColumn("Visual Proof Frame", display_text="View Image"),
        },
        use_container_width=True,
        hide_index=True,
    )
else:
    st.warning("⚠️ No historical inspection records match your selected search or date range filters.")

# =========================================================
# 8. DEEP-DIVE RECORD INSPECTOR
# =========================================================
st.divider()
st.markdown("### 🔍 Deep-Dive Record Inspector & Visual Proof")

if not filtered_df.empty:
    selected_id = st.selectbox(
        "Choose Inspection Log Record to Deep-Dive:",
        filtered_df["Record_ID"].tolist(),
        format_func=lambda x: f"{x} — {filtered_df[filtered_df['Record_ID'] == x]['Project'].values[0]} ({filtered_df[filtered_df['Record_ID'] == x]['Status'].values[0]})",
    )

    record = filtered_df[filtered_df["Record_ID"] == selected_id].iloc[0]

    col_rec1, col_rec2 = st.columns([1.1, 1])

    with col_rec1:
        st.markdown(f"""
        <div class="dark-card">
            <span style="font-size:11px; color:#94A3B8; text-transform:uppercase;">INSPECTION RECORD KEY</span>
            <h3 class="accent-cyan" style="margin:4px 0 10px 0;">📜 {record['Record_ID']}</h3>
            <p style="margin:3px 0;"><b>Audit Timestamp:</b> {record['Date'].strftime('%d %B %Y')}</p>
            <p style="margin:3px 0;"><b>Project Site:</b> {record['Project']}</p>
            <p style="margin:3px 0;"><b>Inspection Category:</b> {record['Inspection_Type']}</p>
            <p style="margin:3px 0;"><b>Lead Engineers:</b> {record['Inspector']}</p>
            <p style="margin:3px 0;"><b>Model Precision Confidence:</b> <span class="accent-green">{record['AI_Confidence']*100:.1f}%</span></p>
            <p style="margin:3px 0;"><b>Defects / Anomalies Detected:</b> <span class="accent-orange">{record['Defects_Found']} Items</span></p>
            <hr style="border-color:rgba(255,255,255,0.1);">
            <p style="margin:0;"><b>Status Verdict:</b> <span class="{'badge-success' if record['Status']=='Safe' else ('badge-warning' if record['Status']=='Review Required' else 'badge-critical')}">{record['Status'].upper()} ({record['Severity']} Severity)</span></p>
        </div>
        """, unsafe_allow_html=True)

    with col_rec2:
        st.markdown("""
        <div class="dark-card">
            <span style="font-size:11px; color:#94A3B8; text-transform:uppercase;">FIELD ENGINEERING NOTES</span>
        """, unsafe_allow_html=True)
        st.info(record["Notes"])
        st.image(record["Image_Ref"], caption=f"Visual Inspection Snapshot Proof for {record['Record_ID']}", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# 9. HISTORICAL ANALYTICS & PLOTLY CHARTS
# =========================================================
st.divider()
st.markdown("### 📊 Historical Site Safety & Defect Analytics")

chart_tab1, chart_tab2 = st.tabs([
    "📈 Safety Status Breakdown",
    "🧱 Defects Detected Per Site"
])

with chart_tab1:
    fig_status = px.pie(
        filtered_df,
        names="Status",
        title="Safety Status Distribution (IS 456 / Eurocode Standards)",
        color="Status",
        color_discrete_map={
            "Safe": "#10B981",
            "Review Required": "#F97316",
            "Critical Alert": "#EF4444",
        },
        hole=0.45,
        template="plotly_dark"
    )
    fig_status.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=340)
    st.plotly_chart(fig_status, use_container_width=True)

with chart_tab2:
    fig_bar = px.bar(
        filtered_df,
        x="Project",
        y="Defects_Found",
        color="Severity",
        title="Detected Structural Defects Across Project Sites",
        barmode="group",
        color_discrete_map={
            "None": "#10B981",
            "Low": "#38BDF8",
            "Medium": "#F97316",
            "High": "#EF4444",
        },
        template="plotly_dark"
    )
    fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=340)
    st.plotly_chart(fig_bar, use_container_width=True)

# =========================================================
# 10. COMPLIANCE EXPORT & EXECUTIVE SUMMARY
# =========================================================
st.divider()
st.markdown("### 📥 Export Compliance Records & Executive Audit")

col_exp1, col_exp2 = st.columns(2)

with col_exp1:
    csv_data = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="💾 Download Filtered Inspection History (.CSV)",
        data=csv_data,
        file_name=f"ConstructVision_Audit_History_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True,
        type="primary"
    )

with col_exp2:
    audit_summary_txt = f"""================================================================================
CONSTRUCTVISION AI — EXECUTIVE COMPLIANCE AUDIT SUMMARY
================================================================================
Generated Date : {datetime.now().strftime('%d %B %Y, %H:%M:%S')}
Active Site    : {gps_info.get('site_code','CV-SITE')} ({gps_info.get('label','Solapur Site')})
Total Logs     : {total_records} Records
Safe Sites     : {safe_count}
Review Sites   : {review_count}
Critical Alerts: {alert_count}
--------------------------------------------------------------------------------
GOVERNING CODES: IS 456:2000 / IS 10262 / Eurocode 2 Compliant
SYSTEM ARCHITECTS & LEAD DEVELOPERS:
  • Er. Ritika Bhumkar (Lead Civil & AI Engineer)
  • Er. Laiba Mulani (Structural AI Researcher)

ORIGIN MOTIVATION SUMMARY:
Created to modernize manual civil engineering walkthroughs with sub-pixel AI 
defect segmentation, live 3D Digital Twin IoT telemetry, and automated BOQ costing.
================================================================================"""

    st.download_button(
        label="📄 Download Executive Audit Summary (.TXT)",
        data=audit_summary_txt,
        file_name=f"Executive_Audit_Summary_{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain",
        use_container_width=True
    )

# =========================================================
# FOOTER
# =========================================================
st.write("")
st.divider()
st.markdown("""
<div style="text-align:center; padding:12px; color:#64748B; font-size:13px;">
    <b>CONSTRUCTVISION AI HISTORICAL AUDIT HUB</b> | Centralized Civil Inspection Engine<br>
    Developed by <b>Er. Ritika Bhumkar</b> & <b>Er. Laiba Mulani</b> | Department of Civil Engineering © 2026
</div>
""", unsafe_allow_html=True)
