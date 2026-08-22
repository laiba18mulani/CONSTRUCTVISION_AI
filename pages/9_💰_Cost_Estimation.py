import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from datetime import datetime

# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Cost Estimation & Billing | CONSTRUCTVISION AI",
    page_icon="💰",
    layout="wide"
)

# =========================================================
# 2. AUTOMATIC LOCATION DETECTOR (Wi-Fi / IP)
# =========================================================
@st.cache_data(ttl=600)
def detect_location():
    try:
        response = requests.get("http://ip-api.com/json/", timeout=3)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                city = data.get("city", "")
                region = data.get("regionName", "")
                country = data.get("country", "")
                return f"{city}, {region}, {country}"
    except Exception:
        pass
    return "Solapur, Maharashtra, India"

auto_location = detect_location()

# =========================================================
# 3. HEADER & CONTROLS
# =========================================================
st.title("💰 AI Repair Cost Estimator & Bill Generator")
st.caption("IS 456 & DSR (Delhi Schedule of Rates) aligned structural repair estimation.")
st.divider()

# Input Configuration Cards
col_left, col_right = st.columns(2)

with col_left:
    with st.container(border=True):
        st.subheader("🏗️ Defect & Site Parameters")
        c1, c2 = st.columns(2)
        with c1:
            damage = st.selectbox("Damage Type", ["Hairline Crack", "Deep Crack", "Corrosion", "Spalling", "Leakage"])
            area = st.number_input("Damage Area (sq.ft)", min_value=1.0, value=25.0, step=5.0)
        with c2:
            urgency = st.selectbox("Urgency Level", ["Standard (1.0x)", "High Priority (1.2x)", "Emergency (1.5x)"])
            city_tier = st.selectbox("Location Tier", ["Tier 1 City (Mumbai/Delhi/Bangalore)", "Tier 2 City", "Tier 3 / Rural"])

with col_right:
    with st.container(border=True):
        st.subheader("📋 Invoice & Project Details")
        c3, c4 = st.columns(2)
        with c3:
            # UPDATED: Customizable Client & Project Name fields
            client_name = st.text_input("Client Name", "Apex Structural Engineers & Co.")
            project_name = st.text_input("Project Name", "Sunrise Heights Tower B")
            invoice_id = st.text_input("Invoice ID", "INV-202608090442")
        with c4:
            # UPDATED: Customizable Lead Engineer field
            engineer_name = st.text_input("Engineer / Inspector", "Er. Structural Auditor")
            current_loc = st.text_input("📍 Live Site Location (Wi-Fi Auto)", value=auto_location)
            gst_rate = st.selectbox("GST Tax Rate (%)", [18, 12, 5, 0], index=0)

# =========================================================
# 4. CALCULATIONS DATABASE
# =========================================================
material_db = {
    "Hairline Crack": {"rate": 375, "item": "Crack Sealant Polymer", "unit": "Liters", "coverage_sqft": 15},
    "Deep Crack": {"rate": 900, "item": "Low Viscosity Epoxy Injection Resin", "unit": "Kg", "coverage_sqft": 8},
    "Corrosion": {"rate": 1200, "item": "Anti-Corrosion Zinc Primer & Coating", "unit": "Liters", "coverage_sqft": 10},
    "Spalling": {"rate": 1500, "item": "Polymer Modified Mortar (PMM)", "unit": "Bags (25kg)", "coverage_sqft": 5},
    "Leakage": {"rate": 600, "item": "Crystalline Waterproof Slurry", "unit": "Kg", "coverage_sqft": 12}
}

urgency_mult = 1.5 if "Emergency" in urgency else (1.2 if "High" in urgency else 1.0)
mat_spec = material_db[damage]
qty_required = round(area / mat_spec["coverage_sqft"], 2)

calc_mat_cost = round(area * mat_spec["rate"], 2)
calc_scaffold = round(area * 80 * urgency_mult, 2)
calc_labour = 5625.0

# =========================================================
# 5. TAB CREATION
# =========================================================
tab_summary, tab_bill, tab_materials = st.tabs([
    "📊 Cost Summary & Analytics", 
    "📄 Interactive Tax Invoice / BOQ", 
    "🛠️ Material Consumption Calculator"
])

# ---------------------------------------------------------
# TAB 1: SUMMARY & ANALYTICS
# ---------------------------------------------------------
with tab_summary:
    st.subheader("📊 Estimated Cost Overview")
    
    base_subtotal = calc_mat_cost + calc_labour + calc_scaffold
    base_gst = round(base_subtotal * (gst_rate / 100), 2)
    base_total = base_subtotal + base_gst

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Material Cost", f"₹ {calc_mat_cost:,.2f}")
    m2.metric("Labour Charges", f"₹ {calc_labour:,.2f}")
    m3.metric("Scaffolding & Safety", f"₹ {calc_scaffold:,.2f}")
    m4.metric(f"GST ({gst_rate}%)", f"₹ {base_gst:,.2f}")
    m5.metric("Grand Total", f"₹ {base_total:,.2f}")

    st.write("")
    col_chart, col_highlights = st.columns([1.2, 1])

    with col_chart:
        with st.container(border=True):
            st.markdown("#### 📈 Cost Distribution")
            fig = go.Figure(data=[go.Pie(
                labels=['Materials', 'Labour', 'Scaffolding & Safety', f'GST ({gst_rate}%)'],
                values=[calc_mat_cost, calc_labour, calc_scaffold, base_gst],
                hole=.4,
                marker_colors=['#00F2FE', '#3B82F6', '#F59E0B', '#10B981']
            )])
            fig.update_layout(template="plotly_dark", height=320, margin=dict(l=10, r=10, t=20, b=10))
            st.plotly_chart(fig, use_container_width=True)

    with col_highlights:
        with st.container(border=True):
            st.markdown("#### 🔍 Structural Inspection Summary")
            st.write(f"• **Detected Location:** {current_loc}")
            st.write(f"• **Primary Material:** {mat_spec['item']}")
            st.write(f"• **Estimated Material Qty:** {qty_required} {mat_spec['unit']}")
            st.write(f"• **Urgency Factor:** {urgency}")
            st.write(f"• **City Tier Category:** {city_tier}")

# ---------------------------------------------------------
# TAB 2: INTERACTIVE TAX INVOICE (NATIVE CLEAN UI)
# ---------------------------------------------------------
with tab_bill:
    # Tax Invoice Header Container
    with st.container(border=True):
        inv_head1, inv_head2 = st.columns([2, 1])
        with inv_head1:
            st.title("TAX INVOICE / BOQ")
            st.caption("CONSTRUCTVISION AI PLATFORM | GSTIN: 27AAAAA0000A1Z5")
        with inv_head2:
            st.subheader(f"🆔 {invoice_id}")
            st.caption(f"Date: {datetime.now().strftime('%d %b %Y')}")

        st.divider()

        b_col1, b_col2 = st.columns(2)
        with b_col1:
            st.markdown("**BILL TO:**")
            st.write(f"**Client:** {client_name}")
            st.write(f"**Project:** {project_name}")
            st.write(f"**Location:** {current_loc} ({city_tier})")

        with b_col2:
            st.markdown("**INSPECTED BY:**")
            st.write(f"**Lead Engineer:** {engineer_name}")
            st.write("**Certification:** Approved IS-456 Auditor")

    st.subheader("📝 Live Interactive Bill Items")
    
    initial_items = [
        {
            "#": 1,
            "Item Description": f"{mat_spec['item']} (Supply for {damage} repair)",
            "Qty / Area": f"{area} sq.ft",
            "Unit Rate (₹)": float(mat_spec['rate']),
            "Total (₹)": float(calc_mat_cost)
        },
        {
            "#": 2,
            "Item Description": "Skilled Structural Labour (Surface prep & application)",
            "Qty / Area": "Lump sum",
            "Unit Rate (₹)": float(calc_labour),
            "Total (₹)": float(calc_labour)
        },
        {
            "#": 3,
            "Item Description": "Safety Scaffolding & Height Access Setup",
            "Qty / Area": f"{area} sq.ft",
            "Unit Rate (₹)": float(round(80 * urgency_mult, 2)),
            "Total (₹)": float(calc_scaffold)
        }
    ]

    # Editable Live Data Frame
    edited_df = st.data_editor(
        pd.DataFrame(initial_items),
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Unit Rate (₹)": st.column_config.NumberColumn(format="₹ %.2f"),
            "Total (₹)": st.column_config.NumberColumn(format="₹ %.2f")
        },
        key="boq_editor"
    )

    # Dynamic totals calculation
    subtotal = edited_df["Total (₹)"].sum() if not edited_df.empty else 0.0
    gst_amt = round(subtotal * (gst_rate / 100), 2)
    grand_tot = subtotal + gst_amt

    # Totals Summary Display Card
    st.write("")
    sum_col1, sum_col2 = st.columns([2, 1])
    with sum_col2:
        with st.container(border=True):
            st.write(f"**Subtotal:** ₹ {subtotal:,.2f}")
            st.write(f"**GST ({gst_rate}%):** ₹ {gst_amt:,.2f}")
            st.subheader(f"Grand Total: ₹ {grand_tot:,.2f}")

    # Plain text invoice download button
    text_invoice = f"""CONSTRUCTVISION AI - TAX INVOICE
Invoice ID: {invoice_id} | Date: {datetime.now().strftime('%d %b %Y')}
Client: {client_name} | Project: {project_name}
Location: {current_loc}
Inspector: {engineer_name}

Subtotal   : ₹ {subtotal:,.2f}
GST ({gst_rate}%)  : ₹ {gst_amt:,.2f}
Grand Total: ₹ {grand_tot:,.2f}
"""
    st.download_button("💾 Download Plain Text Invoice", data=text_invoice, file_name=f"{invoice_id}.txt", mime="text/plain")

# ---------------------------------------------------------
# TAB 3: MATERIAL CONSUMPTION
# ---------------------------------------------------------
with tab_materials:
    with st.container(border=True):
        st.subheader("🛠️ Material Requirement Breakdown")
        st.info(f"Target Area: **{area} sq.ft** | Damage Type: **{damage}**")
        
        m_c1, m_c2, m_c3 = st.columns(3)
        m_c1.metric("Recommended Compound", mat_spec['item'])
        m_c2.metric("Calculated Requirement", f"{qty_required} {mat_spec['unit']}")
        m_c3.metric("Safety Reserve (+10%)", f"{round(qty_required * 1.1, 2)} {mat_spec['unit']}")

        st.divider()
        st.markdown("#### 🧪 Mixing & Application Guide")
        st.markdown(f"""
        - **Mixing Ratio:** Standard IS 456 prescribed ratio for `{mat_spec['item']}`.
        - **Pot Life:** 35 to 45 minutes at ambient temperature.
        - **Curing Duration:** Initial set in 4 hours; full curing in 24 hours.
        """)
        