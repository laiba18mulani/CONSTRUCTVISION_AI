import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="ConstructVision AI - Inspection History",
    page_icon="📜",
    layout="wide"
)

# -----------------------------
# ADVANCED MOCK HISTORICAL DATASET
# -----------------------------
@st.cache_data
def load_historical_data():
    return pd.DataFrame([
        {
            "Record_ID": "INSP-2026-0891",
            "Date": date(2026, 8, 9),
            "Project": "Site A - High-Rise Building",
            "Inspection_Type": "Concrete Crack Detection",
            "Inspector": "Eng. Sarah Chen",
            "Defects_Found": 1,
            "AI_Confidence": 0.96,
            "Status": "Safe",
            "Severity": "Low",
            "Image_Ref": "https://raw.githubusercontent.com/streamlit/demo-uber-nyc-pickups/master/labels.png",
            "Notes": "Micro-fracture detected in Level 4 shear wall. Within acceptable BS EN 1992 limits."
        },
        {
            "Record_ID": "INSP-2026-0888",
            "Date": date(2026, 8, 8),
            "Project": "Site B - Suspension Bridge",
            "Inspection_Type": "Structural Cable & Deck Scan",
            "Inspector": "Eng. David Miller",
            "Defects_Found": 4,
            "AI_Confidence": 0.91,
            "Status": "Review Required",
            "Severity": "Medium",
            "Image_Ref": "https://raw.githubusercontent.com/streamlit/demo-uber-nyc-pickups/master/labels.png",
            "Notes": "Surface spalling observed near Anchor Pier 2. Requires manual ultrasonic verification."
        },
        {
            "Record_ID": "INSP-2026-0882",
            "Date": date(2026, 8, 7),
            "Project": "Site C - Highway Paving",
            "Inspection_Type": "Surface Damage & Pothole Scan",
            "Inspector": "Drone Unit #04",
            "Defects_Found": 0,
            "AI_Confidence": 0.99,
            "Status": "Safe",
            "Severity": "None",
            "Image_Ref": "https://raw.githubusercontent.com/streamlit/demo-uber-nyc-pickups/master/labels.png",
            "Notes": "Sub-grade layer density and surface roughness pass standard compaction criteria."
        },
        {
            "Record_ID": "INSP-2026-0875",
            "Date": date(2026, 8, 6),
            "Project": "Site A - High-Rise Building",
            "Inspection_Type": "PPE & Site Safety Compliance",
            "Inspector": "AI Site Monitor",
            "Defects_Found": 3,
            "AI_Confidence": 0.94,
            "Status": "Critical Alert",
            "Severity": "High",
            "Image_Ref": "https://raw.githubusercontent.com/streamlit/demo-uber-nyc-pickups/master/labels.png",
            "Notes": "Multiple personnel detected in zone 2 B1 basement without hard hats/harnesses."
        },
        {
            "Record_ID": "INSP-2026-0860",
            "Date": date(2026, 8, 4),
            "Project": "Site B - Suspension Bridge",
            "Inspection_Type": "Rebar Corrosion Assessment",
            "Inspector": "Eng. Sarah Chen",
            "Defects_Found": 2,
            "AI_Confidence": 0.88,
            "Status": "Review Required",
            "Severity": "Medium",
            "Image_Ref": "https://raw.githubusercontent.com/streamlit/demo-uber-nyc-pickups/master/labels.png",
            "Notes": "Delamination detected along eastern abutment retaining wall."
        }
    ])

df_history = load_historical_data()

# -----------------------------
# DASHBOARD HEADER
# -----------------------------
st.title("📜 Inspection History & Audit Logs")
st.caption("ConstructVision AI — Centralized Inspection Records, AI Audits & Structural Trends")

# -----------------------------
# ADVANCED FILTER BAR
# -----------------------------
st.subheader("🔎 Query & Filter Records")

with st.expander("🛠️ Filter Controls", expanded=True):
    col1, col2, col3, col4 = st.columns([2, 2, 2, 3])

    with col1:
        project_filter = st.selectbox("Project Site", ["All Sites"] + list(df_history["Project"].unique()))
    
    with col2:
        status_filter = st.selectbox("Safety Status", ["All Statuses"] + list(df_history["Status"].unique()))
    
    with col3:
        severity_filter = st.selectbox("Severity Level", ["All Severities", "Low", "Medium", "High", "None"])

    with col4:
        search_term = st.text_input("🔍 Search Keyword (ID, Inspector, Notes)", "")

    date_col1, date_col2 = st.columns(2)
    with date_col1:
        start_date = st.date_input("Start Date", date(2026, 8, 1))
    with date_col2:
        end_date = st.date_input("End Date", date(2026, 8, 10))

# Apply Filtering Logic
filtered_df = df_history.copy()

if project_filter != "All Sites":
    filtered_df = filtered_df[filtered_df["Project"] == project_filter]

if status_filter != "All Statuses":
    filtered_df = filtered_df[filtered_df["Status"] == status_filter]

if severity_filter != "All Severities":
    filtered_df = filtered_df[filtered_df["Severity"] == severity_filter]

filtered_df = filtered_df[(filtered_df["Date"] >= start_date) & (filtered_df["Date"] <= end_date)]

if search_term:
    search_query = search_term.lower()
    filtered_df = filtered_df[
        filtered_df["Record_ID"].str.lower().str.contains(search_query) |
        filtered_df["Inspector"].str.lower().str.contains(search_query) |
        filtered_df["Notes"].str.lower().str.contains(search_query)
    ]

# -----------------------------
# EXECUTIVE METRICS
# -----------------------------
st.divider()
m1, m2, m3, m4, m5 = st.columns(5)

total_records = len(filtered_df)
safe_count = len(filtered_df[filtered_df["Status"] == "Safe"])
review_count = len(filtered_df[filtered_df["Status"] == "Review Required"])
alert_count = len(filtered_df[filtered_df["Status"] == "Critical Alert"])
avg_confidence = f"{filtered_df['AI_Confidence'].mean() * 100:.1f}%" if total_records > 0 else "N/A"

m1.metric("Total Inspections", total_records)
m2.metric("Safe Sites", safe_count)
m3.metric("Under Review", review_count)
m4.metric("Critical Alerts", alert_count, delta_color="inverse")
m5.metric("Avg AI Accuracy", avg_confidence)

# -----------------------------
# INTERACTIVE DATA TABLE
# -----------------------------
st.subheader("📋 Inspection Audit Trail")

if not filtered_df.empty:
    st.dataframe(
        filtered_df,
        column_config={
            "Record_ID": st.column_config.TextColumn("Record ID", width="small"),
            "Date": st.column_config.DateColumn("Date", format="DD-MM-YYYY"),
            "Project": st.column_config.TextColumn("Site Name", width="medium"),
            "Inspection_Type": st.column_config.TextColumn("Inspection Type", width="medium"),
            "AI_Confidence": st.column_config.ProgressColumn(
                "AI Confidence",
                format="%.0f%%",
                min_value=0,
                max_value=1
            ),
            "Status": st.column_config.SelectboxColumn(
                "Status",
                options=["Safe", "Review Required", "Critical Alert"],
                required=True
            ),
            "Severity": st.column_config.TextColumn("Severity"),
            "Image_Ref": st.column_config.LinkColumn("Visual Proof", display_text="View Snap")
        },
        use_container_width=True,
        hide_index=True
    )
else:
    st.warning("⚠️ No inspection records match your specified criteria.")

# -----------------------------
# DRILL-DOWN RECORD INSPECTOR
# -----------------------------
st.divider()
st.subheader("🔍 Deep-Dive Record Inspector")

if not filtered_df.empty:
    selected_id = st.selectbox(
        "Select Inspection Record to Audit:",
        filtered_df["Record_ID"].tolist(),
        format_func=lambda x: f"{x} - {filtered_df[filtered_df['Record_ID'] == x]['Inspection_Type'].values[0]} ({filtered_df[filtered_df['Record_ID'] == x]['Project'].values[0]})"
    )

    record = filtered_df[filtered_df["Record_ID"] == selected_id].iloc[0]

    with st.container():
        c_left, c_right = st.columns([1, 1])

        with c_left:
            st.markdown(f"### Record: `{record['Record_ID']}`")
            st.write(f"**📅 Date:** {record['Date'].strftime('%d %B %Y')}")
            st.write(f"**🏗️ Site:** {record['Project']}")
            st.write(f"**🔬 Assessment:** {record['Inspection_Type']}")
            st.write(f"**👤 Inspector:** {record['Inspector']}")
            st.write(f"**🎯 AI Model Confidence:** {record['AI_Confidence']*100:.1f}%")

            # Status highlight box
            if record['Status'] == "Safe":
                st.success(f"Status: **{record['Status']}** | Severity: **{record['Severity']}**")
            elif record['Status'] == "Review Required":
                st.warning(f"Status: **{record['Status']}** | Severity: **{record['Severity']}**")
            else:
                st.error(f"Status: **{record['Status']}** | Severity: **{record['Severity']}**")

        with c_right:
            st.markdown("### 📝 Field Engineering Notes & Evidence")
            st.info(record['Notes'])
            st.metric("Defects / Anomaly Count Identified", record['Defects_Found'])

# -----------------------------
# HISTORICAL ANALYTICS & CHARTS
# -----------------------------
st.divider()
st.subheader("📊 Historical Safety Analytics")

chart_tab1, chart_tab2 = st.tabs(["Site Safety Distribution", "Inspection Volume & Defects"])

with chart_tab1:
    fig_status = px.pie(
        filtered_df,
        names="Status",
        title="Safety Status Breakdown Across Inspections",
        color="Status",
        color_discrete_map={
            "Safe": "#2ECC71",
            "Review Required": "#F1C40F",
            "Critical Alert": "#E74C3C"
        },
        hole=0.4
    )
    fig_status.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_status, use_container_width=True)

with chart_tab2:
    fig_bar = px.bar(
        filtered_df,
        x="Project",
        y="Defects_Found",
        color="Severity",
        title="Defects Detected Per Project Site",
        barmode="group",
        color_discrete_map={
            "None": "#2ECC71",
            "Low": "#3498DB",
            "Medium": "#F39C12",
            "High": "#E74C3C"
        }
    )
    fig_bar.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_bar, use_container_width=True)

# -----------------------------
# EXPORT & AUDIT REPORT GENERATION
# -----------------------------
st.divider()
st.subheader("📥 Export & Compliance Audit")

col_exp1, col_exp2 = st.columns(2)

with col_exp1:
    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered History (CSV)",
        data=csv_data,
        file_name=f"constructvision_audit_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True
    )

with col_exp2:
    if st.button("📄 Generate Executive Audit Summary", use_container_width=True):
        st.success("✅ Audit Summary compiled successfully!")
        st.caption("Includes ISO-compliant inspection signatures and structural risk summaries.")

st.caption("ConstructVision AI | Enterprise Safety Compliance & Inspection History Module")
