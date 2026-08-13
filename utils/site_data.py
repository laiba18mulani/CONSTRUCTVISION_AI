import streamlit as st

DEFAULT_SITE_DATA = {
    "site_id": "SOL-2026-001",
    "site_name": "Solapur Transit & Commercial Complex",
    "latitude": 17.65992,
    "longitude": 75.90639,
    "address": "Hotgi Road, Near Solapur Airport Sector 4, Solapur, Maharashtra 413003",
    "calib_mm_per_px": 0.5,
    "inspections": [
        {
            "id": "INSP-001",
            "date": "2026-01-15 10:30:00",
            "month": "January",
            "health_score": 88,
            "status": "SAFE",
            "source": "Site Survey Camera 1",
            "defects": [
                {
                    "type": "Surface Hairline Crack",
                    "location": "Beam B2 - East Column Line",
                    "length_mm": 120.0,
                    "width_mm": 0.8,
                    "severity": "LOW",
                    "confidence": 0.92,
                    "estimated": True
                }
            ]
        }
    ],
    "iot_sensors": {
        "tilt_x_deg": 0.12,
        "tilt_y_deg": 0.08,
        "strain_microstrain": 245.0,
        "vibration_mm_s": 1.4,
        "moisture_pct": 14.2,
        "mode": "SIMULATED"
    }
}

def init_site_state():
    if "site_record" not in st.session_state:
        st.session_state.site_record = DEFAULT_SITE_DATA

def get_current_health():
    rec = st.session_state.site_record
    if not rec["inspections"]:
        return 100, "SAFE"
    latest = rec["inspections"][-1]
    return latest["health_score"], latest["status"]

# 🟢 THIS WAS MISSING:
def add_inspection_record(insp_dict):
    if "site_record" not in st.session_state:
        init_site_state()
    st.session_state.site_record["inspections"].append(insp_dict)
    