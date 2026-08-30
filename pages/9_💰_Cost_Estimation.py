from datetime import datetime
import json
import math
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st

st.set_page_config(
    page_title="AI Repair Cost Estimation & BOQ | CONSTRUCTVISION AI",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Glowing Dark Radial Background */
    .stApp {
        background: radial-gradient(circle at 50% -20%, #172437 0%, #080D14 60%, #03060A 100%) !important;
        color: #E2E8F0;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Hide Streamlit Default UI Elements */
    #MainMenu, footer, header {
        visibility: hidden;
    }

    /* Dark Glass Cards & Containers */
    .dark-card, .metric-box, .invoice-box {
        background: rgba(13, 20, 32, 0.82) !important;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.09) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        margin-bottom: 18px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        transition: all 0.3s ease;
    }
    .dark-card:hover {
        border-color: rgba(56, 189, 248, 0.4) !important;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.15);
        transform: translateY(-2px);
    }

    /* Typography & Neon Accents */
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
    .badge-paid { background: rgba(16, 185, 129, 0.25); color: #6EE7B7; border: 1px solid #10B981; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; }
    .badge-pending { background: rgba(239, 68, 68, 0.25); color: #FCA5A5; border: 1px solid #EF4444; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; }
    .badge-warning { background: rgba(249, 115, 22, 0.25); color: #FDBA74; border: 1px solid #F97316; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; }

    /* Streamlit Buttons */
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

gps_info = st.session_state.get("selected_location_info", {
    "site_code": "CV-RES-01",
    "label": "Navi Peth Commercial Center",
    "lat": 17.6599,
    "lon": 75.9064,
    "road": "Rupa Bhavani Road",
    "type": "Commercial High-Rise",
    "risk_score": 88
})

inspection_data = st.session_state.get("latest_inspection", None)

@st.cache_data(ttl=600)
def detect_location():
    try:
        res = requests.get("http://ip-api.com/json/", timeout=3)
        if res.status_code == 200 and res.json().get("status") == "success":
            data = res.json()
            return f"{data.get('city')}, {data.get('regionName')}, {data.get('country')}"
    except Exception:
        pass
    return "Solapur, Maharashtra, India"

auto_loc = detect_location()

RATE_CARD = {
    "Flexural & Shear Cracks": {"mat": "Low Viscosity Epoxy Injection Grout", "rate": 950, "cov": 8, "unit": "sq.ft"},
    "Concrete Spalling & Rebar Exposure": {"mat": "Polymer Modified Structural Mortar", "rate": 1650, "cov": 5, "unit": "sq.ft"},
    "Honeycombing & Aggregate Voids": {"mat": "Non-Shrink Micro-Concrete Grout", "rate": 850, "cov": 10, "unit": "sq.ft"},
    "Masonry Joint Separation": {"mat": "Polymer Polymerized Sealant Mortar", "rate": 450, "cov": 15, "unit": "sq.ft"},
    "Corrosion & Rebar Rusting": {"mat": "Zinc-Rich Anti-Corrosion Primer", "rate": 1250, "cov": 12, "unit": "sq.ft"},
    "Efflorescence & Seepage Leakage": {"mat": "Crystalline Waterproofing Slurry", "rate": 650, "cov": 14, "unit": "sq.ft"}
}

with st.sidebar:
    st.markdown("### 💰 **Estimation Controls**")
    st.caption("DSR 2026 Schedule Rates & Contingency Risk Settings")
    st.divider()

    inflation_buffer = st.slider("Material Inflation Buffer (%):", min_value=0, max_value=25, value=8, step=1)
    contingency_pct = st.slider("Unforeseen Risk Contingency (%):", min_value=0, max_value=30, value=10, step=1)

    st.divider()
    st.markdown("#### 🎲 Monte Carlo Risk Simulator")
    num_simulations = st.selectbox("Simulation Iterations:", [500, 1000, 2500, 5000], index=1)
    
    st.divider()
    st.markdown("#### 🔗 Cross-Module Links")
    if st.button("🔬 Go to AI Inspection", use_container_width=True):
        st.toast("Redirecting to 5_🔬_AI_Inspection.py...")
    if st.button("🏗️ View 3D Building Twin", use_container_width=True):
        st.toast("Syncing BOQ to 7_🏗️_3D_Building.py...")

    st.caption("Department of Civil Engineering © 2026")

st.title("💰 AI Repair Cost Estimation & BOQ Generator")
st.caption("Automated Bill of Quantities (BOQ), Monte Carlo budget risk forecasting, and GST-compliant tax invoicing engine.")

if inspection_data:
    st.markdown(f"""
    <div class="dark-card" style="padding: 14px 20px !important; margin-bottom: 20px !important;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
            <div>
                <span class="badge-blue">⚡ AI INSPECTION PAYLOAD SYNCED</span>
                <span style="font-weight:700; font-size:16px; margin-left:10px;">{inspection_data.get('site_code', gps_info.get('site_code', 'CV-SITE'))}: {inspection_data.get('location', gps_info.get('label', 'Solapur Field Site'))}</span>
            </div>
            <div style="font-size:13px; color:#94A3B8;">
                <b>Detected Anomalies:</b> <span class="accent-cyan">{inspection_data.get('total_defects', 0)} Defects</span> | 
                <b>Peak Opening:</b> <span class="accent-orange">{inspection_data.get('max_crack_width_mm', 0.0):.2f} mm</span> | 
                <b>Audit Verdict:</b> <span style="color:#EF4444; font-weight:700;">{inspection_data.get('verdict', 'CRITICAL')}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.info("ℹ️ Running in **Autonomous Estimation Mode**. To import live defect coordinates, run an audit in **5_🔬_AI_Inspection.py**.")

col_left, col_right = st.columns([1.1, 1])

with col_left:
    st.markdown('<div class="dark-card">', unsafe_allow_html=True)
    st.markdown("### 🏗️ Defect Scope & Rate Card Setup")
    
    selected_defect_type = st.selectbox(
        "Target Defect Category:",
        options=list(RATE_CARD.keys()),
        index=0
    )
    
    col_area, col_urgency = st.columns(2)
    with col_area:
        default_area = 45.0 if not inspection_data else float(inspection_data.get("total_defects", 2) * 22.5)
        repair_area_sqft = st.number_input("Estimated Repair Area (sq.ft):", min_value=1.0, max_value=5000.0, value=default_area, step=5.0)
    with col_urgency:
        urgency_factor = st.selectbox(
            "Urgency / Safety Factor:",
            ["Standard Operational (1.0x)", "High Priority Shoring (1.25x)", "Emergency Structural Hazard (1.50x)"],
            index=1 if (inspection_data and inspection_data.get("max_crack_width_mm", 0) > 0.3) else 0
        )
    
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="dark-card">', unsafe_allow_html=True)
    st.markdown("### 📋 Client & Invoice Metadata")
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        client_name = st.text_input("Client / Developer Name:", "Solapur Smart Infrastructure Ltd")
        invoice_no = st.text_input("Invoice / BOQ Ref No:", f"INV-{gps_info.get('site_code','SITE')}-{datetime.now().strftime('%m%d%H%M')}")
        payment_status = st.selectbox("Payment Status:", ["Pending", "Paid", "Partial Advance"], index=0)
    with col_c2:
        project_name = st.text_input("Project Site Tag:", f"{gps_info.get('site_code','CV-SITE')}: {gps_info.get('label','Solapur Field Site')}")
        engineer_name = st.text_input("Lead Structural Engineer:", "Er. Ritika Bhumkar & Er. Laiba Mulani")
        gst_rate = st.selectbox("Applicable GST Rate (%):", [18, 12, 5, 0], index=0)

    st.markdown("</div>", unsafe_allow_html=True)

urgency_mult = 1.50 if "Emergency" in urgency_factor else (1.25 if "High" in urgency_factor else 1.00)
rate_info = RATE_CARD[selected_defect_type]

base_mat_rate = rate_info["rate"] * (1 + inflation_buffer / 100.0)
mat_qty_units = math.ceil(repair_area_sqft / rate_info["cov"])
base_mat_cost = round(repair_area_sqft * base_mat_rate, 2)
base_labour_cost = round(repair_area_sqft * 185.0 * urgency_mult, 2)
scaffold_access_cost = round(repair_area_sqft * 65.0, 2)
quality_testing_cost = round(base_mat_cost * 0.05, 2)

base_subtotal = base_mat_cost + base_labour_cost + scaffold_access_cost + quality_testing_cost
contingency_amount = round(base_subtotal * (contingency_pct / 100.0), 2)
total_estimated_base = base_subtotal + contingency_amount

st.divider()
st.markdown("### 📊 Budget Estimation Summary & Financial Metrics")

col_kpi1, col_kpi2, col_kpi3, col_kpi4, col_kpi5 = st.columns(5)

with col_kpi1:
    st.markdown(f"""
    <div class="dark-card">
        <span style="font-size:11px; color:#94A3B8; text-transform:uppercase;">Material Supply</span>
        <h3 class="accent-cyan" style="margin:4px 0 0 0;">₹{base_mat_cost:,.0f}</h3>
        <span style="font-size:11px; color:#94A3B8;">{mat_qty_units} Units ({rate_info['mat'][:18]}...)</span>
    </div>
    """, unsafe_allow_html=True)

with col_kpi2:
    st.markdown(f"""
    <div class="dark-card">
        <span style="font-size:11px; color:#94A3B8; text-transform:uppercase;">Labor & Operations</span>
        <h3 class="accent-orange" style="margin:4px 0 0 0;">₹{base_labour_cost:,.0f}</h3>
        <span style="font-size:11px; color:#94A3B8;">Factor: {urgency_mult:.2f}x</span>
    </div>
    """, unsafe_allow_html=True)

with col_kpi3:
    st.markdown(f"""
    <div class="dark-card">
        <span style="font-size:11px; color:#94A3B8; text-transform:uppercase;">Access & Scaffolding</span>
        <h3 style="margin:4px 0 0 0; color:#FFFFFF;">₹{scaffold_access_cost:,.0f}</h3>
        <span style="font-size:11px; color:#94A3B8;">₹65.0 / sq.ft</span>
    </div>
    """, unsafe_allow_html=True)

with col_kpi4:
    st.markdown(f"""
    <div class="dark-card">
        <span style="font-size:11px; color:#94A3B8; text-transform:uppercase;">Contingency Reserve</span>
        <h3 class="accent-green" style="margin:4px 0 0 0;">₹{contingency_amount:,.0f}</h3>
        <span style="font-size:11px; color:#94A3B8;">{contingency_pct}% Risk Buffer</span>
    </div>
    """, unsafe_allow_html=True)

with col_kpi5:
    st.markdown(f"""
    <div class="dark-card">
        <span style="font-size:11px; color:#94A3B8; text-transform:uppercase;">Estimated Base Total</span>
        <h2 class="accent-cyan" style="margin:4px 0 0 0;">₹{total_estimated_base:,.0f}</h2>
        <span style="font-size:11px; color:#94A3B8;">Excluding {gst_rate}% GST</span>
    </div>
    """, unsafe_allow_html=True)

tab_boq, tab_risk, tab_invoice, tab_sourcing = st.tabs([
    "📋 Itemized BOQ Schedule",
    "🎲 Monte Carlo Risk Simulator",
    "📄 GST Tax Invoice & Export",
    "📦 Material Supply Takeoff"
])

with tab_boq:
    st.markdown("### 📋 Itemized Bill of Quantities (BOQ) Schedule")
    st.caption("DSR 2026 standard civil engineering rate schedule with editable quantities.")

    default_boq_items = [
        {
            "Item No": "BOQ-01",
            "Description": f"Supply & Application of {rate_info['mat']} ({selected_defect_type})",
            "Quantity": float(repair_area_sqft),
            "Unit": "sq.ft",
            "Rate (₹)": float(base_mat_rate),
            "Amount (₹)": float(base_mat_cost)
        },
        {
            "Item No": "BOQ-02",
            "Description": "Surface Chipping, High-Pressure Water Jet Cleaning & Substrate Prep",
            "Quantity": float(repair_area_sqft),
            "Unit": "sq.ft",
            "Rate (₹)": round(65.0 * urgency_mult, 2),
            "Amount (₹)": round(repair_area_sqft * 65.0 * urgency_mult, 2)
        },
        {
            "Item No": "BOQ-03",
            "Description": "Skilled Concrete Injection Grouting & Structural Skilled Labor",
            "Quantity": float(repair_area_sqft),
            "Unit": "sq.ft",
            "Rate (₹)": round(120.0 * urgency_mult, 2),
            "Amount (₹)": round(repair_area_sqft * 120.0 * urgency_mult, 2)
        },
        {
            "Item No": "BOQ-04",
            "Description": "Erection of Structural Steel Scaffolding & Safety Netting",
            "Quantity": float(repair_area_sqft),
            "Unit": "sq.ft",
            "Rate (₹)": 65.0,
            "Amount (₹)": float(scaffold_access_cost)
        },
        {
            "Item No": "BOQ-05",
            "Description": "Quality Assurance Testing (Core Extraction / Tell-Tale Monitoring)",
            "Quantity": 1.0,
            "Unit": "job",
            "Rate (₹)": float(quality_testing_cost),
            "Amount (₹)": float(quality_testing_cost)
        }
    ]

    edited_boq = st.data_editor(
        default_boq_items,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Rate (₹)": st.column_config.NumberColumn("Rate (₹)", format="₹ %.2f"),
            "Amount (₹)": st.column_config.NumberColumn("Amount (₹)", format="₹ %.2f")
        },
        key="boq_editor_table"
    )

    boq_subtotal = sum(row.get("Amount (₹)", 0.0) for row in edited_boq)
    boq_gst = round(boq_subtotal * (gst_rate / 100.0), 2)
    boq_grand_total = round(boq_subtotal + boq_gst, 2)

    col_b1, col_b2 = st.columns([2, 1])
    with col_b2:
        st.markdown(f"""
        <div class="dark-card">
            <p><b>BOQ Subtotal:</b> <span style="float:right;">₹ {boq_subtotal:,.2f}</span></p>
            <p><b>Contingency ({contingency_pct}%):</b> <span style="float:right;">₹ {contingency_amount:,.2f}</span></p>
            <p><b>GST Tax ({gst_rate}%):</b> <span style="float:right;">₹ {boq_gst:,.2f}</span></p>
            <hr style="border-color:rgba(255,255,255,0.1);">
            <h3 class="accent-cyan" style="margin:0;">Grand Total: <span style="float:right;">₹ {boq_grand_total:,.2f}</span></h3>
        </div>
        """, unsafe_allow_html=True)

with tab_risk:
    st.markdown("### 🎲 Monte Carlo Budget Risk & Confidence Simulator")
    st.caption(f"Simulates {num_simulations:,} statistical budget iterations considering material price volatility, labor delays, and inflation.")

    np.random.seed(42)
    # Monte Carlo sampling around base estimate
    mat_sim = np.random.normal(loc=base_mat_cost, scale=base_mat_cost * 0.12, size=num_simulations)
    labour_sim = np.random.normal(loc=base_labour_cost, scale=base_labour_cost * 0.18, size=num_simulations)
    scaffold_sim = np.random.normal(loc=scaffold_access_cost, scale=scaffold_access_cost * 0.08, size=num_simulations)
    contingency_sim = np.random.uniform(0.05, 0.20, size=num_simulations) * (mat_sim + labour_sim + scaffold_sim)

    total_cost_simulations = mat_sim + labour_sim + scaffold_sim + contingency_sim
    total_cost_simulations = np.maximum(base_subtotal * 0.8, total_cost_simulations)

    p10_budget = np.percentile(total_cost_simulations, 10)
    p50_budget = np.percentile(total_cost_simulations, 50)
    p90_budget = np.percentile(total_cost_simulations, 90)

    fig_mc = px.histogram(
        total_cost_simulations,
        nbins=40,
        title=f"Monte Carlo Cost Distribution ({num_simulations:,} Iterations)",
        labels={"value": "Total Repair Cost (₹)"},
        color_discrete_sequence=["#38BDF8"],
        template="plotly_dark"
    )
    fig_mc.add_vline(x=p10_budget, line_dash="dash", line_color="#10B981", annotation_text=f"P10 (Optimistic): ₹{p10_budget:,.0f}")
    fig_mc.add_vline(x=p50_budget, line_dash="solid", line_color="#38BDF8", annotation_text=f"P50 (Median Target): ₹{p50_budget:,.0f}")
    fig_mc.add_vline(x=p90_budget, line_dash="dash", line_color="#EF4444", annotation_text=f"P90 (Conservative Limit): ₹{p90_budget:,.0f}")

    fig_mc.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=360)
    st.plotly_chart(fig_mc, use_container_width=True)

    col_mc1, col_mc2, col_mc3 = st.columns(3)
    with col_mc1:
        st.markdown(f"""
        <div class="dark-card">
            <span style="font-size:11px; color:#10B981; font-weight:bold;">P10 OPTIMISTIC BUDGET</span>
            <h3 class="accent-green" style="margin:4px 0 0 0;">₹{p10_budget:,.0f}</h3>
            <span style="font-size:11px; color:#94A3B8;">10% Probability of Exceeding</span>
        </div>
        """, unsafe_allow_html=True)
    with col_mc2:
        st.markdown(f"""
        <div class="dark-card">
            <span style="font-size:11px; color:#38BDF8; font-weight:bold;">P50 MEDIAN TARGET</span>
            <h3 class="accent-cyan" style="margin:4px 0 0 0;">₹{p50_budget:,.0f}</h3>
            <span style="font-size:11px; color:#94A3B8;">50% Most Likely Cost Baseline</span>
        </div>
        """, unsafe_allow_html=True)
    with col_mc3:
        st.markdown(f"""
        <div class="dark-card">
            <span style="font-size:11px; color:#EF4444; font-weight:bold;">P90 CONSERVATIVE LIMIT</span>
            <h3 class="accent-red" style="margin:4px 0 0 0;">₹{p90_budget:,.0f}</h3>
            <span style="font-size:11px; color:#94A3B8;">Recommended Client Sanction Budget</span>
        </div>
        """, unsafe_allow_html=True)

with tab_invoice:
    st.markdown('<div class="invoice-box">', unsafe_allow_html=True)

    inv_col1, inv_col2 = st.columns([2, 1])
    with inv_col1:
        st.markdown("<h2 class='accent-cyan' style='margin:0;'>TAX INVOICE / BILL OF QUANTITIES</h2>", unsafe_allow_html=True)
        st.write("**CONSTRUCTVISION AI PVT LTD** | GSTIN: `27AAAAA0000A1Z5`")
        st.write(f"<b>Site Location:</b> {auto_loc}", unsafe_allow_html=True)
    with inv_col2:
        st.markdown(f"### `{invoice_no}`")
        st.write(f"**Invoice Date:** {datetime.now().strftime('%d-%b-%Y')}")
        status_cls = "badge-paid" if payment_status == "Paid" else ("badge-warning" if payment_status == "Partial Advance" else "badge-pending")
        st.markdown(f"Status: <span class='{status_cls}'>{payment_status.upper()}</span>", unsafe_allow_html=True)

    st.divider()

    meta_col1, meta_col2 = st.columns(2)
    with meta_col1:
        st.markdown("**Billed To Client:**")
        st.write(f"• **Client Name:** {client_name}")
        st.write(f"• **Project Site:** {project_name}")
        st.write(f"• **Target Defect:** {selected_defect_type}")
    with meta_col2:
        st.markdown("**Inspected & Verified By:**")
        st.write(f"• **Structural Engineers:** {engineer_name}")
        st.write(f"• **GPS Location:** {gps_info.get('lat', 17.6599):.4f}° N, {gps_info.get('lon', 75.9064):.4f}° E")
        st.write("• **Governing Code:** IS 456 & DSR 2026 Compliant")

    st.write("")
    st.dataframe(pd.DataFrame(edited_boq), use_container_width=True, hide_index=True)

    st.write("")
    col_tot1, col_tot_summary = st.columns([2, 1])
    with col_tot_summary:
        st.write(f"**Subtotal:** ₹ {boq_subtotal:,.2f}")
        st.write(f"**GST Tax ({gst_rate}%):** ₹ {boq_gst:,.2f}")
        st.markdown(f"<h3 class='accent-green' style='margin:0;'>Grand Total: ₹ {boq_grand_total:,.2f}</h3>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    txt_bill = f"""================================================================================
TAX INVOICE — CONSTRUCTVISION AI STRUCTURAL AUDIT
================================================================================
Invoice No    : {invoice_no}
Invoice Date  : {datetime.now().strftime('%d-%b-%Y')}
Client Name   : {client_name}
Project Site  : {project_name}
Defect Scope  : {selected_defect_type} ({repair_area_sqft} sq.ft)
Location      : {gps_info.get('label', 'Solapur Site')} ({gps_info.get('lat', 17.6599):.4f}° N, {gps_info.get('lon', 75.9064):.4f}° E)
--------------------------------------------------------------------------------
BOQ Subtotal        : ₹ {boq_subtotal:,.2f}
Contingency Buffer  : ₹ {contingency_amount:,.2f}
GST Tax ({gst_rate}%)       : ₹ {boq_gst:,.2f}
GRAND TOTAL         : ₹ {boq_grand_total:,.2f}
Payment Status      : {payment_status.upper()}
--------------------------------------------------------------------------------
Lead Engineers : {engineer_name}
Generated by CONSTRUCTVISION AI Estimation Engine © 2026
================================================================================"""

    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(
            "📥 Download Formatted Invoice Text (.TXT)",
            data=txt_bill,
            file_name=f"Invoice_{invoice_no}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            use_container_width=True,
            type="primary"
        )
    with col_dl2:
        st.download_button(
            "💾 Export Itemized BOQ Schedule (.CSV)",
            data=pd.DataFrame(edited_boq).to_csv(index=False),
            file_name=f"BOQ_{invoice_no}_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )

with tab_sourcing:
    st.markdown("### 📦 Material Supply & Procurement Takeoff")
    st.caption("Calculated material requirements including reserve buffers for procurement teams.")

    m_col1, m_col2, m_col3, m_col4 = st.columns(4)

    with m_col1:
        st.metric("Primary Material", rate_info["mat"][:22])
    with m_col2:
        st.metric("Base Quantity Units", f"{mat_qty_units} Units")
    with m_col3:
        st.metric("Buffer Reserve (+15%)", f"{math.ceil(mat_qty_units * 1.15)} Units")
    with m_col4:
        st.metric("Coverage Yield", f"{rate_info['cov']} sq.ft / Unit")

    st.markdown("#### 🛒 Procurement Supplier Checklist")
    procurement_df = pd.DataFrame([
        {
            "Supply Item": rate_info["mat"],
            "Quantity": math.ceil(mat_qty_units * 1.15),
            "Unit": "Pails / Bags",
            "Est. Unit Price (₹)": round(base_mat_rate * rate_info["cov"], 2),
            "Total Supply Cost (₹)": round(math.ceil(mat_qty_units * 1.15) * base_mat_rate * rate_info["cov"], 2),
            "Availability": "In Stock (Solapur Vendor)"
        },
        {
            "Supply Item": "Structural Steel Rebar (Fe500)",
            "Quantity": round(repair_area_sqft * 0.4, 1),
            "Unit": "kg",
            "Est. Unit Price (₹)": 68.0,
            "Total Supply Cost (₹)": round(repair_area_sqft * 0.4 * 68.0, 2),
            "Availability": "Ready for Dispatch"
        },
        {
            "Supply Item": "Polymer Bonding Agent Slurry",
            "Quantity": math.ceil(repair_area_sqft / 45.0),
            "Unit": "Cans (5L)",
            "Est. Unit Price (₹)": 1450.0,
            "Total Supply Cost (₹)": math.ceil(repair_area_sqft / 45.0) * 1450.0,
            "Availability": "In Stock"
        }
    ])

    st.dataframe(procurement_df, use_container_width=True, hide_index=True)

st.write("")
st.divider()
st.markdown("""
<div style="text-align:center; padding:12px; color:#64748B; font-size:13px;">
    <b>CONSTRUCTVISION AI ESTIMATION & BILLING ENGINE</b> | Auto-Generated BOQ & Risk Management System<br>
    Developed by <b>Ritika Bhumkar</b> & <b>Laiba Mulani</b> | Department of Civil Engineering © 2026
</div>
""", unsafe_allow_html=True)
