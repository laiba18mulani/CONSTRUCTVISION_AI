import altair as alt
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from modules.digital_twin.engine import TwinInputs, frame_members, frame_nodes, screening_results, telemetry

st.set_page_config(page_title="ConstructVision | Digital Twin", page_icon=":material/domain:", layout="wide")

st.session_state.setdefault("twin", TwinInputs())

with st.sidebar:
    st.title("ConstructVision")
    st.caption("Built environment intelligence")
    view = st.radio("Workspace", ["Command center", "Twin studio", "Capture & reconstruction", "Asset health", "Integration"], label_visibility="collapsed")
    st.space("medium")
    st.badge("LIVE TELEMETRY", icon=":material/sensors:", color="green")
    st.caption("Asset: CV-HQ-01 · Bengaluru")
    st.space("large")
    st.caption("Digital twin platform · v2.0")


def make_frame(inputs: TwinInputs, show_wind: bool = False):
    figure = go.Figure()
    for start, end, kind in frame_members(inputs):
        figure.add_trace(go.Scatter3d(x=[start[0], end[0]], y=[start[1], end[1]], z=[start[2], end[2]], mode="lines", line=dict(color="#42C9D9" if kind == "beam" else "#91E6DF", width=5 if kind == "column" else 3), hoverinfo="skip", showlegend=False))
    nodes = frame_nodes(inputs)
    figure.add_trace(go.Scatter3d(x=nodes.x, y=nodes.y, z=nodes.z, mode="markers", marker=dict(size=3, color="#F7B955"), name="Sensor-ready nodes", hovertemplate="X %{x:.1f} m<br>Y %{y:.1f} m<br>Z %{z:.1f} m<extra></extra>"))
    if show_wind:
        z = list(range(2, int(inputs.floors*inputs.storey_m), 4))
        figure.add_trace(go.Cone(x=[-3]*len(z), y=[inputs.bays_y*inputs.bay_m/2]*len(z), z=z, u=[inputs.wind_mps/5]*len(z), v=[0]*len(z), w=[0]*len(z), colorscale=[[0,"#507CFF"],[1,"#B5E7FF"]], showscale=False, sizemode="absolute", sizeref=.8, name="Wind vector"))
    figure.update_layout(height=570, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor="#07131F", plot_bgcolor="#07131F", scene=dict(bgcolor="#07131F", xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False), aspectmode="data", camera=dict(eye=dict(x=1.6,y=1.7,z=1.05))), legend=dict(font=dict(color="#EDF7FA")))
    return figure


def hero():
    st.title("A living model of your built asset")
    st.caption("Image reconstruction, instrumented structural monitoring and scenario testing—unified in one operational twin.")
    data = telemetry()
    current = data.iloc[-1]
    with st.container(horizontal=True):
        st.metric("Structural health", "92 / 100", "+0.7 this week", border=True, chart_data=data["strain_µε"].tail(14), chart_type="line")
        st.metric("Monitored channels", "48 / 52", "4 commissioning", border=True, chart_data=data["wind_mps"].tail(14), chart_type="line")
        st.metric("Active alerts", "02", "1 needs review", delta_color="inverse", border=True)
        st.metric("Last ingest", "18 sec", "MQTT gateway", border=True)
    left, right = st.columns([1.45, 1])
    with left:
        with st.container(border=True):
            st.subheader("Instrumented asset", help="Editable parametric structural frame. Not a reconstructed mesh.")
            st.plotly_chart(make_frame(st.session_state.twin, True), width="stretch", config={"displaylogo": False})
    with right:
        with st.container(border=True):
            st.subheader("Priority signals")
            st.warning("C-2 / level 01 — strain trend above baseline", icon=":material/trending_up:")
            st.info("Rainfall threshold approaching at foundation drain", icon=":material/water_drop:")
            st.success("North elevation camera capture is synchronized", icon=":material/check_circle:")
            st.subheader("Today’s operating context")
            st.metric("Wind speed", f"{current['wind_mps']:.1f} m/s")
            st.metric("Ambient temperature", f"{current['temperature_°C']:.1f} °C")


def studio():
    st.title("Twin studio")
    st.caption("Edit the architectural frame, then run an auditable preliminary load screen. Solver-grade FEA/CFD jobs are routed through the integration layer.")
    with st.form("geometry"):
        a,b,c = st.columns(3)
        floors = a.number_input("Storeys", 1, 60, st.session_state.twin.floors)
        bays_x = b.number_input("X bays", 1, 20, st.session_state.twin.bays_x)
        bays_y = c.number_input("Y bays", 1, 20, st.session_state.twin.bays_y)
        bay_m = a.number_input("Bay length (m)", 3.0, 15.0, st.session_state.twin.bay_m, .5)
        storey_m = b.number_input("Storey height (m)", 2.4, 8.0, st.session_state.twin.storey_m, .1)
        concrete = c.number_input("Concrete f'c (MPa)", 15.0, 100.0, st.session_state.twin.concrete_mpa, 1.0)
        updated = st.form_submit_button("Apply geometry", type="primary", icon=":material/architecture:")
    if updated:
        old = st.session_state.twin
        st.session_state.twin = TwinInputs(int(floors), int(bays_x), int(bays_y), bay_m, storey_m, concrete, old.column_mm, old.beam_mm, old.wind_mps, old.rainfall_mm_h, old.flood_m, old.live_load_kpa)
    twin = st.session_state.twin
    control, model = st.columns([.8, 1.6])
    with control:
        with st.container(border=True):
            st.subheader("Scenario inputs")
            wind = st.slider("Wind speed (m/s)", 0, 80, int(twin.wind_mps))
            rain = st.slider("Rainfall intensity (mm/h)", 0, 250, int(twin.rainfall_mm_h))
            flood = st.slider("Flood depth (m)", 0.0, 5.0, twin.flood_m, .1)
            live = st.slider("Live load (kPa)", 1.0, 12.0, twin.live_load_kpa, .25)
            scenario = TwinInputs(twin.floors,twin.bays_x,twin.bays_y,twin.bay_m,twin.storey_m,twin.concrete_mpa,twin.column_mm,twin.beam_mm,wind,rain,flood,live)
            result = screening_results(scenario)
            st.metric("Peak utilization", f"{result['utilization']:.0%}", result["status"])
            st.metric("Wind pressure", f"{result['wind_kpa']:.2f} kPa")
            st.metric("Flood pressure at base", f"{result['flood_kpa']:.1f} kPa")
    with model:
        st.plotly_chart(make_frame(scenario, True), width="stretch", config={"displaylogo": False})
    st.warning("Screening only: gravity, simple beam bending, dynamic wind pressure and hydrostatic base pressure are shown for triage. A licensed engineer must approve design decisions; route models to validated FEA/CFD for project-grade analysis.", icon=":material/gpp_maybe:")


def capture():
    st.title("Capture & reconstruction")
    st.caption("Turn calibrated multi-view site imagery into a registered mesh, then align it to the editable structural model.")
    uploads = st.file_uploader("Upload overlapping building imagery", type=["jpg", "jpeg", "png", "tif"], accept_multiple_files=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Inputs received", len(uploads or []))
    c2.metric("Minimum capture target", "60 images")
    c3.metric("Coverage requirement", "≥ 70% overlap")
    with st.expander("Reconstruction pipeline", expanded=True, icon=":material/account_tree:"):
        st.markdown("1. Camera calibration and EXIF validation  \n2. Feature matching and sparse reconstruction  \n3. Dense cloud / mesh generation  \n4. Scale, georeference and QA  \n5. Register mesh against BIM / structural frame")
    if uploads and st.button("Queue reconstruction job", type="primary", icon=":material/play_arrow:"):
        st.toast("Capture package staged. Connect a COLMAP/OpenMVS worker to execute the reconstruction.")
    st.info("Three angled photos can support visual reference, but are not enough for dependable structural geometry or metric reconstruction. Capture an all-around, overlapping photo set with calibrated scale control before generating a decision-grade twin.", icon=":material/photo_camera:")


def health():
    st.title("Asset health")
    data = telemetry(24*30)
    period = st.segmented_control("Window", ["24 hours", "7 days", "30 days"], default="7 days")
    size = {"24 hours":24, "7 days":168, "30 days":720}[period]
    frame = data.tail(size)
    chart = alt.Chart(frame).transform_fold(["strain_µε", "tilt_mrad"], as_=["signal", "value"]).mark_line().encode(x=alt.X("time:T", title=None), y=alt.Y("value:Q", title="Sensor value"), color=alt.Color("signal:N", title=None), tooltip=["time:T", "signal:N", "value:Q"]).properties(height=360)
    st.altair_chart(chart, width="stretch")
    st.subheader("Sensor inventory")
    inventory = pd.DataFrame([["STR-C2-01", "Level 01 column", "Strain", "Online", 87], ["TILT-RF-03", "Roof frame", "Tilt", "Online", 91], ["WL-BASE-01", "Foundation drain", "Water level", "Attention", 64], ["ACC-C3-02", "Level 03 column", "Acceleration", "Online", 95]], columns=["Channel", "Location", "Type", "Status", "Data quality"])
    st.dataframe(inventory, hide_index=True, column_config={"Data quality": st.column_config.ProgressColumn(min_value=0, max_value=100, format="%d%%")})


def integration():
    st.title("Deployment & solver integrations")
    st.caption("Connect live field data and compute infrastructure without coupling the user experience to any one vendor.")
    with st.container(border=True):
        st.subheader("Field ingestion")
        st.code("mqtts://gateway.example.com/site/CV-HQ-01/telemetry\nPOST /api/v1/telemetry  { timestamp, sensor_id, value, unit, quality }")
        st.caption("Recommended: MQTT over TLS, device certificates, schema validation, immutable time-series storage and alert acknowledgement logs.")
    a,b = st.columns(2)
    with a:
        with st.container(border=True):
            st.subheader("Structural solver queue")
            st.write("OpenSees / CalculiX worker")
            st.badge("Not connected", color="orange")
            st.button("Configure solver endpoint", icon=":material/settings:")
    with b:
        with st.container(border=True):
            st.subheader("Environmental solver queue")
            st.write("OpenFOAM / CFD worker")
            st.badge("Not connected", color="orange")
            st.button("Configure CFD endpoint", icon=":material/air:")
    st.info("The visual wind vectors in Twin studio communicate load direction. Animated, physically correct air flow requires a CFD mesh, boundary conditions and a validated OpenFOAM/CFD job—not browser animation alone.", icon=":material/air:")


{"Command center": hero, "Twin studio": studio, "Capture & reconstruction": capture, "Asset health": health, "Integration": integration}[view]()
