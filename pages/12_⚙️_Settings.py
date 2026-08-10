import streamlit as st
import json
from datetime import datetime

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="ConstructVision AI - Settings",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ System Settings & Governance")
st.caption("ConstructVision AI — Enterprise Model Calibration, Edge Node & Alert Preferences")

# -----------------------------
# INITIAL CONFIGURATION STATE
# -----------------------------
if "config" not in st.session_state:
    st.session_state.config = {
        "site_name": "Site A - High-Rise Building",
        "ai_confidence_threshold": 0.85,
        "crack_sensitivity": "High",
        "auto_flag_defects": True,
        "iot_sync_interval": 2,
        "mqtt_broker_url": "mqtt.constructvision.ai",
        "mqtt_port": 8883,
        "alert_email": "safety-compliance@constructvision.ai",
        "enable_sms_alerts": True,
        "enable_slack_webhook": False,
        "slack_webhook_url": "https://hooks.slack.com/services/...",
        "iso_compliance_mode": True
    }

# -----------------------------
# SETTINGS TABS
# -----------------------------
tab_ai, tab_iot, tab_alerts, tab_governance = st.tabs([
    "🤖 AI Model Calibration",
    "📡 IoT & Edge Gateway",
    "🚨 Alert & Notifications",
    "🛡️ Compliance & Export"
])

# -------------------------------------------------------------
# TAB 1: AI MODEL CALIBRATION
# -------------------------------------------------------------
with tab_ai:
    st.subheader("🎯 Computer Vision Model Calibration")
    st.caption("Fine-tune detection sensitivity and AI decision baselines for image/video analysis.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### 🔬 Defect & Crack Detection")
        ai_conf = st.slider(
            "Minimum AI Detection Confidence Threshold",
            min_value=0.50,
            max_value=0.99,
            value=st.session_state.config["ai_confidence_threshold"],
            step=0.01,
            help="Detections below this confidence level will be hidden or flagged for manual inspector review."
        )

        crack_sens = st.select_slider(
            "Concrete Surface Crack Sensitivity",
            options=["Low (Major Cracks >2mm)", "Medium (Standard >0.5mm)", "High (Micro-cracks >0.1mm)"],
            value="High (Micro-cracks >0.1mm)"
        )

        auto_flag = st.toggle(
            "Auto-Flag Critical Structural Defects",
            value=st.session_state.config["auto_flag_defects"],
            help="Automatically create an urgent review item when severe defects are detected."
        )

    with col2:
        st.markdown("##### 🦺 PPE & Worker Safety Monitoring")
        st.selectbox("Hard Hat & Vest Detection Engine", ["YOLOv8-X (High Precision)", "YOLOv8-N (Edge Optimized)"])
        st.number_input("Maximum Unsafe Zone Dwell Time (Seconds)", min_value=5, max_value=120, value=15)
        st.checkbox("Enable Automated Thermal Heat Stress Screening", value=True)

# -------------------------------------------------------------
# TAB 2: IOT & EDGE GATEWAY
# -------------------------------------------------------------
with tab_iot:
    st.subheader("📡 Edge Device & Telemetry Protocols")
    st.caption("Configure field edge hardware connections and telemetry streaming intervals.")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("##### ⚙️ MQTT Telemetry Server")
        broker_url = st.text_input("MQTT Broker Endpoint", value=st.session_state.config["mqtt_broker_url"])
        broker_port = st.number_input("Port (SSL/TLS)", value=st.session_state.config["mqtt_port"])
        sync_rate = st.select_slider("Sensor Data Sampling Interval", options=[1, 2, 5, 10, 30], value=2, format_func=lambda x: f"{x} sec")

    with c2:
        st.markdown("##### 📟 Active Site Node Registry")
        st.text_input("Active Gateway Mac Address", value="00:1A:2B:3C:4D:5E", disabled=True)
        st.selectbox("Site Location Deployment", ["Site A - High-Rise Building", "Site B - Cable Suspension Bridge", "Site C - Highway Paving Project"])
        st.success("🟢 Edge Gateway Status: **Connected & Synchronized**")

# -------------------------------------------------------------
# TAB 3: ALERT & NOTIFICATIONS
# -------------------------------------------------------------
with tab_alerts:
    st.subheader("🚨 Real-Time Emergency Escalation")
    st.caption("Define channels and contacts triggered when critical site parameters fail safety checks.")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("##### ✉️ Email & SMS Routing")
        alert_email = st.text_input("Primary Safety Engineer Email", value=st.session_state.config["alert_email"])
        enable_sms = st.checkbox("Send Instant SMS for Critical Structural Vibrations", value=st.session_state.config["enable_sms_alerts"])
        sms_phone = st.text_input("Emergency Contact Phone (+Country Code)", value="+1 (555) 019-2834")

    with col_b:
        st.markdown("##### 🔗 Webhooks & Enterprise Chat")
        enable_slack = st.toggle("Enable Webhook Alerts (Slack/MS Teams)", value=st.session_state.config["enable_slack_webhook"])
        webhook_url = st.text_input("Webhook Endpoint URL", value=st.session_state.config["slack_webhook_url"], disabled=not enable_slack)
        
        st.multiselect(
            "Trigger Notifications On:",
            ["Structural Vibration > Threshold", "High Concrete Temp / Cure Failure", "PPE Safety Non-Compliance", "Unrecognized Worker"],
            default=["Structural Vibration > Threshold", "High Concrete Temp / Cure Failure"]
        )

# -------------------------------------------------------------
# TAB 4: COMPLIANCE & EXPORT
# -------------------------------------------------------------
with tab_governance:
    st.subheader("🛡️ Regulatory Governance & Backup")
    st.caption("Manage ISO standards compliance and site config profiles.")

    iso_mode = st.toggle("Enforce ISO 19650 Building Information Modelling (BIM) Standards", value=st.session_state.config["iso_compliance_mode"])
    st.selectbox("Data Retention Policy", ["30 Days (Standard)", "90 Days (Enterprise)", "365 Days (Full Audit Log)"])

    st.divider()
    st.markdown("##### 📥 Configuration Backup & Management")

    current_config_json = json.dumps(st.session_state.config, indent=2)

    b1, b2 = st.columns(2)
    with b1:
        st.download_button(
            label="💾 Export Settings Configuration (JSON)",
            data=current_config_json,
            file_name=f"constructvision_config_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json",
            use_container_width=True
        )

    with b2:
        if st.button("🔄 Reset Settings to Factory Default", use_container_width=True):
            st.session_state.config = {
                "site_name": "Site A - High-Rise Building",
                "ai_confidence_threshold": 0.80,
                "crack_sensitivity": "Medium",
                "auto_flag_defects": True,
                "iot_sync_interval": 2,
                "mqtt_broker_url": "mqtt.constructvision.ai",
                "mqtt_port": 8883,
                "alert_email": "admin@constructvision.ai",
                "enable_sms_alerts": False,
                "enable_slack_webhook": False,
                "slack_webhook_url": "",
                "iso_compliance_mode": True
            }
            st.success("✅ Settings reset to factory defaults.")
            st.rerun()

# -----------------------------
# SAVE BAR (BOTTOM)
# -----------------------------
st.divider()

if st.button("💾 Save Settings", type="primary", use_container_width=True):
    # Update local state
    st.session_state.config["ai_confidence_threshold"] = ai_conf
    st.session_state.config["auto_flag_defects"] = auto_flag
    st.session_state.config["mqtt_broker_url"] = broker_url
    st.session_state.config["alert_email"] = alert_email
    st.session_state.config["enable_sms_alerts"] = enable_sms
    st.session_state.config["enable_slack_webhook"] = enable_slack
    st.session_state.config["iso_compliance_mode"] = iso_mode
    
    st.success("🎉 Settings updated and deployed to connected edge nodes successfully!")

st.caption("ConstructVision AI | Enterprise Governance & Configuration Module")
