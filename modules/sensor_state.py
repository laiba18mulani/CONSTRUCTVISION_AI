import streamlit as st
import pandas as pd

def get_shared_sensor_data():
    components_data = [
        {"Sensor_ID": "SN-FBG-101", "Name": "Foundation Pad", "Type": "Mass Concrete", "Sensor_Type": "Fiber Optic Strain (FBG)", "X": 5, "Y": 5, "Z": 0, "Base_Stress": 12, "Battery": 98, "RSSI": -62, "Lat": 18.5204, "Lon": 73.8567},
        {"Sensor_ID": "SN-ACC-102", "Name": "Column C1 (NW)", "Type": "RCC Column", "Sensor_Type": "3-Axis MEMS Accelerometer", "X": 2, "Y": 2, "Z": 1, "Base_Stress": 14, "Battery": 92, "RSSI": -58, "Lat": 18.5206, "Lon": 73.8565},
        {"Sensor_ID": "SN-STR-103", "Name": "Column C2 (NE)", "Type": "RCC Column", "Sensor_Type": "Piezoelectric Strain Gauge", "X": 8, "Y": 2, "Z": 1, "Base_Stress": 14, "Battery": 88, "RSSI": -65, "Lat": 18.5206, "Lon": 73.8569},
        {"Sensor_ID": "SN-ACC-104", "Name": "Column C3 (SW)", "Type": "RCC Column", "Sensor_Type": "3-Axis MEMS Accelerometer", "X": 2, "Y": 8, "Z": 1, "Base_Stress": 15, "Battery": 95, "RSSI": -60, "Lat": 18.5202, "Lon": 73.8565},
        {"Sensor_ID": "SN-STR-105", "Name": "Column C4 (SE)", "Type": "RCC Column", "Sensor_Type": "Piezoelectric Strain Gauge", "X": 8, "Y": 8, "Z": 1, "Base_Stress": 15, "Battery": 91, "RSSI": -67, "Lat": 18.5202, "Lon": 73.8569},
        {"Sensor_ID": "SN-INC-106", "Name": "Mid Column C1-Upper", "Type": "RCC Column", "Sensor_Type": "Wireless Inclinometer", "X": 2, "Y": 2, "Z": 5, "Base_Stress": 18, "Battery": 84, "RSSI": -71, "Lat": 18.5206, "Lon": 73.8565},
        {"Sensor_ID": "SN-INC-107", "Name": "Mid Column C2-Upper", "Type": "RCC Column", "Sensor_Type": "Wireless Inclinometer", "X": 8, "Y": 2, "Z": 5, "Base_Stress": 18, "Battery": 87, "RSSI": -69, "Lat": 18.5206, "Lon": 73.8569},
        {"Sensor_ID": "SN-AE-108", "Name": "Load Brick Wall", "Type": "AAC Masonry", "Sensor_Type": "Acoustic Emission Cracking", "X": 5, "Y": 2, "Z": 3, "Base_Stress": 9, "Battery": 79, "RSSI": -74, "Lat": 18.5205, "Lon": 73.8567},
        {"Sensor_ID": "SN-LAS-109", "Name": "Exterior Chajja", "Type": "Precast Slab", "Sensor_Type": "Laser Displacement", "X": 5, "Y": 0, "Z": 6, "Base_Stress": 6, "Battery": 96, "RSSI": -55, "Lat": 18.5207, "Lon": 73.8567},
        {"Sensor_ID": "SN-STR-110", "Name": "Roof Perimeter Beam", "Type": "RCC Beam", "Sensor_Type": "Piezoelectric Strain Gauge", "X": 5, "Y": 5, "Z": 8, "Base_Stress": 16, "Battery": 90, "RSSI": -63, "Lat": 18.5204, "Lon": 73.8567},
        {"Sensor_ID": "SN-FBG-111", "Name": "Main Roof Slab", "Type": "RCC Slab", "Sensor_Type": "Fiber Optic Strain (FBG)", "X": 5, "Y": 5, "Z": 9, "Base_Stress": 13, "Battery": 85, "RSSI": -59, "Lat": 18.5204, "Lon": 73.8567},
    ]
    df = pd.DataFrame(components_data)

    wind = st.session_state.get('wind', 35)
    seismic = st.session_state.get('seismic', 1.2)
    temp = st.session_state.get('temp', 30)

    df["Current_Stress_MPa"] = (df["Base_Stress"] + (wind * 0.12) + (seismic**2 * 1.6) + (abs(temp - 25) * 0.25)).round(2)
    df["Micro_Strain_ue"] = (df["Current_Stress_MPa"] * 42.5).round(1)
    df["Vibration_G"] = round(0.02 + (seismic * 0.15) + (wind * 0.003), 3)

    def evaluate_status(stress):
        if stress < 25:
            return "NORMAL", "#10B981"
        elif stress < 45:
            return "WARNING", "#F97316"
        else:
            return "CRITICAL", "#EF4444"

    res = df["Current_Stress_MPa"].apply(evaluate_status)
    df["Status"] = [r[0] for r in res]
    df["Status_Color"] = [r[1] for r in res]
    return df
