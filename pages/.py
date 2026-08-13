import streamlit as st
import pandas as pd
from datetime import datetime

DEFAULT_SITE_DATA = {
    "site_id": "SOL-2026-001",
    "site_name": "Solapur Transit & Commercial Complex",
    "latitude": 17.65992,
    "longitude": 75.90639,
    "address": "Hotgi Road, Near Solapur Airport Sector 4, Solapur, Maharashtra 413003",
    "calib_mm_per_px": 0.5, # Default reference scale calibration
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
        },
        {
            "id": "INSP-002",
            "date": "2026-02-18 14:15:00",
            "month": "February",
            "health_score": 82,
            "status": "SAFE",
            "source": "IP Camera Feed 02",
            "defects": [
                {
                    "type": "Flexural Concrete Crack",
                    "location": "Slab S1 - Under Span",
                    "length_mm": 240.0,
                    "width_mm": 1.5,
                    "severity": "MEDIUM",
                    "confidence": 0.89,
                    "estimated": True
                }
            ]
        },
        {
            "id": "INSP-003",
            "date": "2026-03-02 09:00:00",
            "month": "March",
            "health_score": 74,
            "status": "WARNING",
            "source": "Drone Survey Stream",
            "defects": [
                {
                    "type": "Shear Wall Shear Crack",
                    "location": "Core Wall Shear Zone W1",
                    "length_mm": 410.0,
                    "width_mm": 2.8,
                    "severity": "HIGH",
                    "confidence": 0.94,
                    "estimated": True
                },
                {
                    "type": "Efflorescence / Water Seepage",
                    "location": "Basement Wall B1",
                    "length_mm": 0.0,
                    "width_mm": 0.0,
                    "severity": "MEDIUM",
                    "confidence": 0.87,
                    "estimated": False
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
        "mode": "SIMULATED" # 'REAL' or 'SIMULATED'
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

def add_inspection_record(insp_dict):
    st.session_state.site_record["inspections"].append(insp_dict)
    
