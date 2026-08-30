import json
import math
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# =========================================================
# 1. PAGE CONFIGURATION & DARK GLASS UI THEME
# =========================================================
st.set_page_config(
    page_title="Civil Engineering Material Library & Mix Design | CONSTRUCTVISION AI",
    page_icon="🧱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Dark Glass UI CSS
st.markdown("""
<style>
    /* Glowing Dark Background */
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
    .dark-card, .metric-box {
        background: rgba(13, 20, 32, 0.78) !important;
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
    .material-badge {
        background: rgba(37, 99, 235, 0.25);
        color: #60A5FA;
        border: 1px solid #2563EB;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 8px;
    }
    .badge-cyan { background: rgba(56, 189, 248, 0.2); color: #38BDF8; border: 1px solid #0284C7; padding: 4px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 700; }
    .badge-green { background: rgba(16, 185, 129, 0.2); color: #6EE7B7; border: 1px solid #10B981; padding: 4px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 700; }
    .badge-orange { background: rgba(249, 115, 22, 0.2); color: #FDBA74; border: 1px solid #F97316; padding: 4px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 700; }

    /* Custom Streamlit Buttons */
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
# 2. SESSION STATE & CROSS-MODULE LINKAGE
# =========================================================
if "selected_component" not in st.session_state:
    st.session_state.selected_component = "Foundation Footing"

inspection_payload = st.session_state.get("latest_inspection", None)

# Auto-mapping components to relevant material categories
component_material_map = {
    "Foundation Footing (F-01)": "Concrete",
    "Foundation Footing": "Concrete",
    "RCC Support Columns (C-12)": "Concrete",
    "Column-04": "Concrete",
    "Flexural Beam Span (B-04)": "Structural Steel",
    "Beam-01": "Structural Steel",
    "Floor Slab Soffit (S-09)": "Concrete",
    "Slab-02": "Concrete",
    "Brick Masonry Wall (W-02)": "Masonry",
}

default_search = component_material_map.get(st.session_state.selected_component, "")

# =========================================================
# 3. COMPREHENSIVE CIVIL MATERIALS DATABASE
# =========================================================
BASE_PATH = Path("assets/materials/images")
BASE_PATH.mkdir(parents=True, exist_ok=True)

PRESET_MATERIALS = [
    {
        "id": "m25_concrete",
        "name": "M25 Structural Concrete",
        "category": "Concrete",
        "strength_mpa": 25.0,
        "density_kg_m3": 2450,
        "elastic_modulus_gpa": 25.0,
        "carbon_kg_co2_m3": 340,
        "fire_rating_hrs": 4,
        "cost_rating": "$$$",
        "code_std": "IS 456:2000 / Eurocode 2",
        "description": "Standard reinforced concrete mix for slabs, beams, and residential RCC columns."
    },
    {
        "id": "m40_concrete",
        "name": "M40 High-Performance Concrete",
        "category": "Concrete",
        "strength_mpa": 40.0,
        "density_kg_m3": 2550,
        "elastic_modulus_gpa": 31.6,
        "carbon_kg_co2_m3": 440,
        "fire_rating_hrs": 4,
        "cost_rating": "$$$$",
        "code_std": "IS 456:2000 / ACI 318",
        "description": "Heavy structural concrete for high-rise columns, bridge piers, and prestressed elements."
    },
    {
        "id": "fe500_steel",
        "name": "Fe500 TMT Steel Rebar",
        "category": "Metals",
        "strength_mpa": 500.0,
        "density_kg_m3": 7850,
        "elastic_modulus_gpa": 200.0,
        "carbon_kg_co2_m3": 1850,
        "fire_rating_hrs": 2,
        "cost_rating": "$$$$",
        "code_std": "IS 1786 / ASTM A615",
        "description": "High-yield strength deformed thermo-mechanically treated bars for tensile reinforcement."
    },
    {
        "id": "epoxy_grout",
        "name": "Low-Viscosity Epoxy Injection Grout",
        "category": "Repair Resins",
        "strength_mpa": 65.0,
        "density_kg_m3": 1400,
        "elastic_modulus_gpa": 12.5,
        "carbon_kg_co2_m3": 280,
        "fire_rating_hrs": 1,
        "cost_rating": "$$$$$",
        "code_std": "IS 456 Cl 12.3 / ASTM C881",
        "description": "Solvent-free structural epoxy resin for pressure grouting shear and flexural micro-cracks (<0.30mm)."
    },
    {
        "id": "polymer_mortar",
        "name": "Polymer Modified Structural Mortar",
        "category": "Repair Mortars",
        "strength_mpa": 35.0,
        "density_kg_m3": 2100,
        "elastic_modulus_gpa": 18.0,
        "carbon_kg_co2_m3": 210,
        "fire_rating_hrs": 3,
        "cost_rating": "$$$",
        "code_std": "EN 1504-3 / IS 516",
        "description": "Fiber-reinforced mortar engineered for repairing spalling zones and restoring exposed steel rebar cover."
    },
    {
        "id": "fly_ash_brick",
        "name": "Fly Ash Clay Bricks",
        "category": "Masonry",
        "strength_mpa": 7.5,
        "density_kg_m3": 1700,
        "elastic_modulus_gpa": 3.5,
        "carbon_kg_co2_m3": 120,
        "fire_rating_hrs": 4,
        "cost_rating": "$$",
        "code_std": "IS 12894:2002",
        "description": "Eco-friendly industrial fly ash masonry units for load-bearing walls and infill partitions."
    },
    {
        "id": "aac_block",
        "name": "Autoclaved Aerated Concrete (AAC) Blocks",
        "category": "Masonry",
        "strength_mpa": 4.0,
        "density_kg_m3": 600,
        "elastic_modulus_gpa": 1.8,
        "carbon_kg_co2_m3": 75,
        "fire_rating_hrs": 4,
        "cost_rating": "$$",
        "code_std": "IS 2185 Part 3",
        "description": "Ultra-lightweight thermal insulating blocks for partition walls, reducing building dead load."
    },
    {
        "id": "frp_wrap",
        "name": "Carbon Fiber (CFRP) Structural Wrap",
        "category": "Composite Wrap",
        "strength_mpa": 3400.0,
        "density_kg_m3": 1600,
        "elastic_modulus_gpa": 230.0,
        "carbon_kg_co2_m3": 620,
        "fire_rating_hrs": 1,
        "cost_rating": "$$$$$",
        "code_std": "ACI 440.2R / IS 15988",
        "description": "High-tensile carbon fiber reinforced polymer sheet for external column confinement and shear strengthening."
    }
]

@st.cache_data
def load_materials_dynamically(base_path: Path):
    materials = list(PRESET_MATERIALS)
    existing_ids = {m["id"] for m in materials}

    if base_path.exists():
        for folder in base_path.iterdir():
            if folder.is_dir() and folder.name not in existing_ids:
                meta_file = folder / "metadata.json"
                if meta_file.exists():
                    try:
                        with open(meta_file, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            if data:
                                materials.append(data)
                    except Exception:
                        pass
    return materials

MATERIALS_DATA = load_materials_dynamically(BASE_PATH)

# =========================================================
# 4. MATERIAL MODAL DIALOG COMPONENT
# =========================================================
try:
    @st.dialog("🔬 Technical Material Specification", width="large")
    def show_material_modal(item, image_path, text_content):
        col1, col2 = st.columns([1, 1.2])

        with col1:
            if image_path and Path(image_path).exists():
                st.image(str(image_path), use_container_width=True)
            else:
                # Synthetic procedural material badge preview
                st.markdown(f"""
                <div class="dark-card" style="text-align:center; padding: 40px !important;">
                    <h1 style="font-size:54px; margin:0;">🧱</h1>
                    <h3 class="accent-cyan" style="margin:10px 0 0 0;">{item['name']}</h3>
                    <span class="material-badge">{item['category']}</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"• **Governing Standard:** `{item.get('code_std', 'IS 456')}`")
            st.markdown(f"• **Material ID Tag:** `{item['id']}`")
            st.markdown(f"• **Cost Rating:** <span class='accent-orange'>{item.get('cost_rating', '$$')}</span>", unsafe_allow_html=True)

        with col2:
            st.markdown(f"<h2 class='accent-cyan' style='margin-top:0;'>{item['name']}</h2>", unsafe_allow_html=True)
            st.write(f"**Description:** {item.get('description', 'Standard structural material specification.')}")
            st.divider()

            m_c1, m_c2 = st.columns(2)
            with m_c1:
                st.write(f"• **Characteristic Strength ($f_k$):** {item.get('strength_mpa', 'N/A')} MPa")
                st.write(f"• **Elastic Modulus ($E$):** {item.get('elastic_modulus_gpa', 'N/A')} GPa")
            with m_c2:
                st.write(f"• **Unit Density ($\rho$):** {item.get('density_kg_m3', 'N/A')} kg/m³")
                st.write(f"• **Carbon Footprint:** {item.get('carbon_kg_co2_m3', 'N/A')} kg CO₂e/m³")

            st.markdown("##### **Engineering Application & Field Notes:**")
            st.markdown(text_content)

        st.divider()
        st.download_button(
            label="📥 Download Official Technical Specification Datasheet (.TXT)",
            data=f"TECHNICAL SPECIFICATION: {item['name']}\nID: {item['id']}\nCategory: {item['category']}\nCode Standard: {item.get('code_std', 'IS 456')}\nCompressive Strength: {item.get('strength_mpa')} MPa\nDensity: {item.get('density_kg_m3')} kg/m3\nCarbon Intensity: {item.get('carbon_kg_co2_m3')} kg CO2e/m3\n\nNOTES:\n{text_content}",
            file_name=f"Datasheet_{item['id']}.txt",
            mime="text/plain",
            key=f"modal_dl_{item['id']}",
            use_container_width=True
        )
except AttributeError:
    def show_material_modal(item, image_path, text_content):
        st.info(f"📄 **{item['name']} Specs:** {text_content}")

# =========================================================
# 5. SIDEBAR SEARCH & FILTERS
# =========================================================
with st.sidebar:
    st.markdown("### 🧱 **Material Library Controls**")
    st.caption("IS / Eurocode Civil Specification Catalog")
    st.divider()

    search_term = st.text_input("🔍 Search Material or Keyword:", value=default_search)

    categories = ["All"] + sorted(list(set(item["category"] for item in MATERIALS_DATA)))
    selected_category = st.selectbox("Filter by Structural Category:", categories)

    st.divider()
    st.markdown("#### 🔗 Linked Inspection Target")
    st.caption(f"• **Active 3D Member:** `{st.session_state.selected_component}`")
    if inspection_payload:
        st.caption(f"• **Audit Verdict:** `{inspection_payload.get('verdict', 'CRITICAL')}`")
        st.caption(f"• **Peak Crack:** `{inspection_payload.get('max_crack_width_mm', 0.0):.2f} mm`")

    st.divider()
    st.caption("Department of Civil Engineering © 2026")

# Filter materials based on search term and category
filtered_materials = [
    mat for mat in MATERIALS_DATA
    if (search_term.lower() in mat["name"].lower() or search_term.lower() in mat["id"].lower() or search_term.lower() in mat["category"].lower())
    and (selected_category == "All" or mat["category"] == selected_category)
]

# =========================================================
# 6. DASHBOARD HEADER & LOCATION SYNCHRONIZATION
# =========================================================
st.title("🧱 Civil Engineering Material Library & Mix Design Engine")
st.caption("Standard structural material specifications, IS 10262 concrete mix proportioning, and embodied carbon auditing.")

# Active Sync Banner
st.markdown(f"""
<div class="dark-card" style="padding: 12px 20px !important; margin-bottom: 20px !important;">
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
        <div>
            <span class="badge-cyan">📍 ACTIVE 3D MEMBER FOCUS</span>
            <span style="font-weight:700; font-size:16px; margin-left:10px;">{st.session_state.selected_component}</span>
        </div>
        <div style="font-size:13px; color:#94A3B8;">
            <b>Recommended Category:</b> <span class="accent-cyan">{component_material_map.get(st.session_state.selected_component, 'Concrete / Steel')}</span> | 
            <b>Catalog Total:</b> <span class="accent-green">{len(MATERIALS_DATA)} Items</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Top Metrics
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f"""
    <div class="dark-card">
        <span style="font-size:11px; color:#94A3B8; text-transform:uppercase;">Total Library Items</span>
        <h2 class="accent-cyan" style="margin:4px 0 0 0;">{len(MATERIALS_DATA)} Specs</h2>
    </div>
    """, unsafe_allow_html=True)
with m2:
    st.markdown(f"""
    <div class="dark-card">
        <span style="font-size:11px; color:#94A3B8; text-transform:uppercase;">Filtered View</span>
        <h2 class="accent-orange" style="margin:4px 0 0 0;">{len(filtered_materials)} Items</h2>
    </div>
    """, unsafe_allow_html=True)
with m3:
    st.markdown(f"""
    <div class="dark-card">
        <span style="font-size:11px; color:#94A3B8; text-transform:uppercase;">Categories</span>
        <h2 class="accent-green" style="margin:4px 0 0 0;">{len(categories)-1} Types</h2>
    </div>
    """, unsafe_allow_html=True)
with m4:
    st.markdown(f"""
    <div class="dark-card">
        <span style="font-size:11px; color:#94A3B8; text-transform:uppercase;">Governing Standards</span>
        <h3 style="margin:4px 0 0 0; color:#FFFFFF;">IS 456 / IS 10262</h3>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# =========================================================
# 7. MAIN INTERACTIVE TABS
# =========================================================
tab_grid, tab_mix, tab_compare, tab_admin = st.tabs([
    "📚 Material Catalog Grid",
    "🧮 Concrete Mix Design (IS 10262)",
    "⚖️ Multi-Material Comparison",
    "➕ Add New Material Spec"
])

# ---------------- TAB 1: CATALOG GRID ----------------
with tab_grid:
    st.markdown("### 📚 Structural Material Catalog")
    st.caption("Click 'Detailed Specs' to view characteristic strength, code standards, and download technical datasheets.")

    if not filtered_materials:
        st.info("ℹ️ No material specifications match your search or filter criteria.")
    else:
        grid_cols = st.columns(3)

        for i, item in enumerate(filtered_materials):
            mat_id = item["id"]
            mat_name = item["name"]
            category = item["category"]
            folder = BASE_PATH / mat_id

            image_path = None
            for ext in [".jpg", ".jpeg", ".png", ".webp"]:
                candidate = folder / f"{mat_id}{ext}"
                if candidate.exists():
                    image_path = candidate
                    break

            info_path = folder / "info.txt"
            text_content = item.get("description", "Standard civil engineering material specification.")
            if info_path.exists():
                try:
                    with open(info_path, "r", encoding="utf-8") as f:
                        text_content = f.read()
                except Exception:
                    pass

            with grid_cols[i % 3]:
                st.markdown(f"""
                <div class="dark-card">
                    <span class="material-badge">{category}</span>
                    <h3 style="font-size:18px; margin:4px 0 8px 0;" class="accent-cyan">{mat_name}</h3>
                    <p style="margin:2px 0;"><b>Characteristic Strength:</b> {item.get('strength_mpa', 'N/A')} MPa</p>
                    <p style="margin:2px 0;"><b>Unit Density:</b> {item.get('density_kg_m3', 'N/A')} kg/m³</p>
                    <p style="margin:2px 0;"><b>Carbon Intensity:</b> <span class="accent-orange">{item.get('carbon_kg_co2_m3', 'N/A')} kg CO₂e/m³</span></p>
                    <p style="margin:2px 0;"><b>Standard:</b> {item.get('code_std', 'IS 456')}</p>
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"🔍 Detailed Specs: {mat_name[:16]}...", key=f"btn_{mat_id}", use_container_width=True):
                    show_material_modal(item, image_path, text_content)

# ---------------- TAB 2: IS 10262 MIX DESIGN ENGINE ----------------
with tab_mix:
    st.markdown("### 🧮 IS 10262 Concrete Mix Design & Carbon Calculator")
    st.caption("Standard wet-to-dry concrete volume conversion, ingredient mass proportioning, and embodied carbon footprint auditing.")

    col_mix1, col_mix2 = st.columns([1.1, 1])

    with col_mix1:
        st.markdown('<div class="dark-card">', unsafe_allow_html=True)
        st.markdown("#### **Target Mix Parameters**")

        mix_grade = st.selectbox(
            "Concrete Design Grade:",
            ["M15 (1 : 2 : 4)", "M20 (1 : 1.5 : 3)", "M25 (1 : 1 : 2)", "M30 (High-Performance)", "M35 (Structural Column)", "M40 (Prestressed Member)"],
            index=2
        )

        target_volume_m3 = st.number_input("Target Wet Concrete Volume ($m^3$):", min_value=0.5, max_value=1000.0, value=15.0, step=0.5)
        wc_ratio = st.slider("Water-Cement Ratio ($w/c$):", min_value=0.35, max_value=0.60, value=0.45, step=0.01)
        fly_ash_pct = st.slider("Fly Ash Replacement Buffer (%):", min_value=0, max_value=35, value=15, step=5)
        slump_mm = st.slider("Target Workability Slump (mm):", min_value=25, max_value=175, value=75, step=25)

        st.markdown("</div>", unsafe_allow_html=True)

    # Calculation logic for IS 10262
    dry_vol = target_volume_m3 * 1.54  # 54% volume expansion factor for dry aggregate voids

    if "M15" in mix_grade:
        ratio_sum = 1 + 2 + 4
        c_part, s_part, a_part = 1, 2, 4
        carbon_per_m3 = 280
    elif "M20" in mix_grade:
        ratio_sum = 1 + 1.5 + 3
        c_part, s_part, a_part = 1, 1.5, 3
        carbon_per_m3 = 310
    elif "M25" in mix_grade:
        ratio_sum = 1 + 1 + 2
        c_part, s_part, a_part = 1, 1, 2
        carbon_per_m3 = 340
    elif "M30" in mix_grade:
        ratio_sum = 1 + 0.8 + 1.6
        c_part, s_part, a_part = 1, 0.8, 1.6
        carbon_per_m3 = 380
    elif "M35" in mix_grade:
        ratio_sum = 1 + 0.7 + 1.4
        c_part, s_part, a_part = 1, 0.7, 1.4
        carbon_per_m3 = 410
    else:  # M40
        ratio_sum = 1 + 0.6 + 1.2
        c_part, s_part, a_part = 1, 0.6, 1.2
        carbon_per_m3 = 440

    raw_cement_kg = ((c_part / ratio_sum) * dry_vol) * 1440
    fly_ash_kg = round(raw_cement_kg * (fly_ash_pct / 100.0), 1)
    net_cement_kg = round(raw_cement_kg - fly_ash_kg, 1)
    cement_bags = math.ceil(net_cement_kg / 50.0)

    sand_m3 = round((s_part / ratio_sum) * dry_vol, 2)
    sand_kg = round(sand_m3 * 1600, 1)

    agg_m3 = round((a_part / ratio_sum) * dry_vol, 2)
    agg_kg = round(agg_m3 * 1550, 1)

    water_liters = round((net_cement_kg + fly_ash_kg) * wc_ratio, 0)
    admixture_liters = round((net_cement_kg + fly_ash_kg) * 0.008, 1)

    # Carbon reduction calculation from fly ash
    base_carbon = target_volume_m3 * carbon_per_m3
    saved_carbon = (fly_ash_kg * 0.82)
    net_carbon_tons = round((base_carbon - saved_carbon) / 1000.0, 2)

    with col_mix2:
        st.markdown('<div class="dark-card">', unsafe_allow_html=True)
        st.markdown("#### **Calculated Material Takeoff**")
        st.markdown(f"• **OPC Cement Required:** <span class='accent-cyan'>{cement_bags} Bags</span> ({net_cement_kg:,.1f} kg)", unsafe_allow_html=True)
        if fly_ash_pct > 0:
            st.markdown(f"• **Fly Ash Buffer ({fly_ash_pct}%):** <span class='accent-green'>{fly_ash_kg:,.1f} kg</span>", unsafe_allow_html=True)
        st.markdown(f"• **Fine Aggregate (River Sand):** {sand_m3} $m^3$ ({sand_kg:,.0f} kg)")
        st.markdown(f"• **Coarse Aggregate (20mm Gravel):** {agg_m3} $m^3$ ({agg_kg:,.0f} kg)")
        st.markdown(f"• **Mixing Water Volume:** {water_liters:,.0f} Liters ($w/c = {wc_ratio:.2f}$)")
        st.markdown(f"• **Superplasticizer Admixture:** {admixture_liters} Liters")
        st.divider()
        st.markdown(f"• **Embodied Carbon Intensity:** <span class='accent-orange'>{net_carbon_tons} Metric Tons $CO_2e$</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Detailed Mix DataFrame Table
    mix_df = pd.DataFrame([
        {"Ingredient Item": "Ordinary Portland Cement (OPC 53)", "Quantity": f"{net_cement_kg:,.1f} kg ({cement_bags} Bags)", "Unit Rate (₹)": "380 / Bag", "Est. Cost (₹)": cement_bags * 380},
        {"Ingredient Item": "Pozzolanic Fly Ash", "Quantity": f"{fly_ash_kg:,.1f} kg", "Unit Rate (₹)": "3.5 / kg", "Est. Cost (₹)": round(fly_ash_kg * 3.5, 2)},
        {"Ingredient Item": "Fine River Sand (Zone II)", "Quantity": f"{sand_m3} m³ ({sand_kg:,.0f} kg)", "Unit Rate (₹)": "1450 / m³", "Est. Cost (₹)": round(sand_m3 * 1450, 2)},
        {"Ingredient Item": "Coarse Gravel Aggregate (20mm)", "Quantity": f"{agg_m3} m³ ({agg_kg:,.0f} kg)", "Unit Rate (₹)": "1250 / m³", "Est. Cost (₹)": round(agg_m3 * 1250, 2)},
        {"Ingredient Item": "Polycarboxylate Superplasticizer", "Quantity": f"{admixture_liters} L", "Unit Rate (₹)": "120 / L", "Est. Cost (₹)": round(admixture_liters * 120, 2)}
    ])

    st.markdown("#### 📋 Ingredient Cost & Quantity Summary Table")
    st.dataframe(mix_df, use_container_width=True, hide_index=True)

# ---------------- TAB 3: MATERIAL COMPARISON MATRIX ----------------
with tab_compare:
    st.markdown("### ⚖️ Multi-Material Properties Comparison Matrix")
    st.caption("Side-by-side technical comparison and spider radar plot across structural materials.")

    selected_names = st.multiselect(
        "Select materials to compare side-by-side:",
        options=[m["name"] for m in MATERIALS_DATA],
        default=[MATERIALS_DATA[0]["name"], MATERIALS_DATA[2]["name"], MATERIALS_DATA[3]["name"]]
    )

    if selected_names:
        comp_items = [m for m in MATERIALS_DATA if m["name"] in selected_names]

        # Spider Radar Chart Comparison
        categories_radar = ['Compressive Strength', 'Unit Density', 'Elastic Modulus', 'Fire Resistance', 'Eco-Sustainability']

        fig_radar = go.Figure()

        for m in comp_items:
            # Normalize values to 0 - 100 scale for radar plot
            s_val = min(100, int(m.get('strength_mpa', 20) * 1.8))
            d_val = min(100, int(m.get('density_kg_m3', 2000) / 80.0))
            e_val = min(100, int(m.get('elastic_modulus_gpa', 20) * 2.5))
            f_val = m.get('fire_rating_hrs', 2) * 25
            c_val = max(10, 100 - int(m.get('carbon_kg_co2_m3', 300) / 10.0))

            fig_radar.add_trace(go.Scatterpolar(
                r=[s_val, d_val, e_val, f_val, c_val],
                theta=categories_radar,
                fill='toself',
                name=m['name']
            ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], color="#94A3B8"),
                angularaxis=dict(color="#FFFFFF")
            ),
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=380,
            margin=dict(l=40, r=40, t=30, b=30)
        )

        comp_col1, comp_col2 = st.columns([1.2, 1])

        with comp_col1:
            comparison_table = {
                "Specification Property": ["Category", "Characteristic Strength (MPa)", "Density (kg/m³)", "Elastic Modulus (GPa)", "Carbon Intensity (kg CO₂e/m³)", "Governing Standard"],
                **{m["name"]: [m["category"], f"{m.get('strength_mpa', 'N/A')} MPa", f"{m.get('density_kg_m3', 'N/A')} kg/m³", f"{m.get('elastic_modulus_gpa', 'N/A')} GPa", f"{m.get('carbon_kg_co2_m3', 'N/A')} kg", m.get("code_std", "IS 456")] for m in comp_items}
            }
            st.table(pd.DataFrame(comparison_table))

        with comp_col2:
            st.plotly_chart(fig_radar, use_container_width=True)

    else:
        st.info("ℹ️ Select at least one material above to render the side-by-side comparison matrix.")

# ---------------- TAB 4: ADMIN UPLOAD FORM ----------------
with tab_admin:
    st.markdown("### ➕ Add Custom Material Specification to Library")
    st.caption("Upload custom material properties, image texture assets, and JSON specification metadata.")

    with st.form("add_material_form", clear_on_submit=True):
        col_a, col_b = st.columns(2)
        with col_a:
            new_id = st.text_input("Material Identifier ID (e.g. timber_oak):").lower().strip().replace(" ", "_")
            new_name = st.text_input("Material Name (e.g. Structural Oak Timber):")
            new_category = st.selectbox("Structural Category:", ["Concrete", "Metals", "Masonry", "Repair Resins", "Repair Mortars", "Composite Wrap", "Timber", "Finishes"])
            new_strength = st.number_input("Characteristic Strength (MPa):", min_value=0.5, value=25.0, step=1.0)

        with col_b:
            new_density = st.number_input("Unit Density (kg/m³):", min_value=100, value=2400, step=50)
            new_modulus = st.number_input("Elastic Modulus (GPa):", min_value=0.1, value=25.0, step=1.0)
            new_code = st.text_input("Governing Code Standard:", "IS 883 / Eurocode 5")
            new_image = st.file_uploader("Upload Texture Photo (JPG/PNG):", type=["jpg", "png", "webp", "jpeg"])

        new_specs = st.text_area("Technical Specs & Engineering Guidelines (Markdown Supported):", "High-strength structural timber element for roof trusses and beam purlins.")

        submitted = st.form_submit_button("💾 Save Material to Local Registry", type="primary")

        if submitted:
            if not new_id or not new_name:
                st.error("⚠️ Please fill in both the Material Identifier ID and Material Name.")
            else:
                target_dir = BASE_PATH / new_id
                target_dir.mkdir(parents=True, exist_ok=True)

                if new_image:
                    ext = Path(new_image.name).suffix
                    with open(target_dir / f"{new_id}{ext}", "wb") as f:
                        f.write(new_image.getbuffer())

                meta_data = {
                    "id": new_id,
                    "name": new_name,
                    "category": new_category,
                    "strength_mpa": new_strength,
                    "density_kg_m3": new_density,
                    "elastic_modulus_gpa": new_modulus,
                    "code_std": new_code,
                    "description": new_specs
                }

                with open(target_dir / "metadata.json", "w", encoding="utf-8") as f:
                    json.dump(meta_data, f, indent=4)

                with open(target_dir / "info.txt", "w", encoding="utf-8") as f:
                    f.write(new_specs if new_specs else "No specs provided.")

                st.success(f"✅ Custom Material '{new_name}' saved successfully to registry!")
                st.cache_data.clear()
                st.rerun()

# =========================================================
# FOOTER
# =========================================================
st.write("")
st.divider()
st.markdown("""
<div style="text-align:center; padding:12px; color:#64748B; font-size:13px;">
    <b>CONSTRUCTVISION AI MATERIAL ENGINE</b> | IS 10262 & Civil Material Specifications<br>
    Developed by <b>Ritika Bhumkar</b> & <b>Laiba Mulani</b> | Department of Civil Engineering © 2026
</div>
""", unsafe_allow_html=True)
                                                                         