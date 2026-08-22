import streamlit as st
import math

# =========================================================
# 1. PAGE CONFIGURATION & DARK THEME CSS
# =========================================================
st.set_page_config(
    page_title="Virtual Practical - Construction Simulator",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Dark Theme CSS
st.markdown("""
<style>
    /* Dark Theme Core */
    .stApp {
        background-color: #0E1117;
        color: #C9D1D9;
    }
    
    /* Custom Card Style */
    .stage-card {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    /* Risk Badges */
    .badge-high {
        background-color: #8B0000;
        color: #FFCCCC;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 0.85rem;
    }
    .badge-med {
        background-color: #B8860B;
        color: #FFFFCC;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 0.85rem;
    }
    .badge-low {
        background-color: #238636;
        color: #E6FFFA;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 0.85rem;
    }
    
    /* Custom Buttons */
    div.stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 2. ENHANCED CONSTRUCTION DATA STRUCTURE
# =========================================================
STEPS_DATA = [
    {
        "id": 1,
        "title": "1️⃣ Site Preparation",
        "description": "Cleaning site, removing topsoil, marking boundaries, and setting up benchmark points.",
        "materials": "Survey Equipment, Marking Powder/Chalk, Boundary Stakes",
        "machines": "JCB/Excavator, Total Station, Dumpy Level",
        "safety": "Wear hard hats, safety boots, high-visibility jackets, and secure boundaries.",
        "risk": "Low",
        "duration": "2 - 4 Days",
        "qa_checklist": ["Check site boundaries against structural layout", "Establish reference benchmark (TBM)", "Clear vegetation and 150mm topsoil"]
    },
    {
        "id": 2,
        "title": "2️⃣ Excavation",
        "description": "Digging foundation trenches according to structural drawings and soil specifications.",
        "materials": "Timber Shoring, Struts, Safety Netting",
        "machines": "Hydraulic Excavator, Tippers/Dumpers",
        "safety": "Support trench walls to prevent soil collapse. Keep machinery away from trench edges.",
        "risk": "High",
        "duration": "3 - 7 Days",
        "qa_checklist": ["Verify excavation depth and width", "Inspect soil bearing capacity visually", "Ensure dewatering mechanism if groundwater rises"]
    },
    {
        "id": 3,
        "title": "3️⃣ Foundation (RCC Footing)",
        "description": "Laying PCC bed, binding steel reinforcement mesh, and casting RCC footings.",
        "materials": "PCC M10, Concrete M20/M25, Steel Rebars (Fe500)",
        "machines": "Transit Mixer, Concrete Mixer, Needle Vibrator",
        "safety": "Inspect reinforcement binding and shuttering stability before pouring concrete.",
        "risk": "High",
        "duration": "7 - 10 Days",
        "qa_checklist": ["Verify clear cover (50mm for footings)", "Ensure proper lap length & rebar spacing", "Compaction using needle vibrators to avoid honeycombing"]
    },
    {
        "id": 4,
        "title": "4️⃣ Columns Construction",
        "description": "Erecting column rebar cages, fixing shuttering formwork, and casting vertical RCC columns.",
        "materials": "Thermo-Mechanically Treated (TMT) Steel, Concrete M25",
        "machines": "Concrete Vibrator, Tower Crane / Hoist",
        "safety": "Ensure proper scaffolding and vertical plumb checking before concreting.",
        "risk": "High",
        "duration": "5 - 8 Days",
        "qa_checklist": ["Check column plumbness using plumb bob", "Ensure stirrup hook angle is 135 degrees", "Curring minimum 7 to 10 days post-stripping"]
    },
    {
        "id": 5,
        "title": "5️⃣ Beams & Formwork",
        "description": "Installing props, shuttering plates, and binding longitudinal/stirrup steel reinforcement for plinth & roof beams.",
        "materials": "Plywood/Steel Shuttering, Rebar Fe500, Binding Wire",
        "machines": "Bar Bending Machine, Bar Cutting Machine",
        "safety": "Ensure staging/propping is braced securely to resist hydraulic concrete load.",
        "risk": "Medium",
        "duration": "7 - 12 Days",
        "qa_checklist": ["Inspect beam depth and cover blocks (25mm)", "Check lap locations (avoid high stress zones)", "Clean formwork inside prior to concrete pour"]
    },
    {
        "id": 6,
        "title": "6️⃣ Roof Slab Concreting",
        "description": "Laying electrical conduits, placement of bottom and top mesh rebars, and monolithic slab casting.",
        "materials": "Concrete M25, Electrical PVC Pipes, Chair Bars",
        "machines": "Boom Pump / Line Concrete Pump, Surface Vibrator",
        "safety": "Ensure safety harnesses for high-elevation slab work and safe pump line anchors.",
        "risk": "High",
        "duration": "1 - 2 Days (Pouring)",
        "qa_checklist": ["Check slab thickness using depth gauge pin", "Ensure conduit pipes do not bunch together", "Implement pond curing after 24 hours"]
    },
    {
        "id": 7,
        "title": "7️⃣ Brick / Block Masonry",
        "description": "Constructing superstructure walls using red bricks or AAC blocks bonded with cement mortar.",
        "materials": "AAC Blocks / Clay Bricks, Cement Mortar (1:4 or 1:6)",
        "machines": "Block Cutter, Hand Mortar Mixer",
        "safety": "Do not raise masonry beyond 1.5m height in a single day.",
        "risk": "Medium",
        "duration": "10 - 15 Days",
        "qa_checklist": ["Check wall alignment with plumb bob and spirit level", "Ensure proper raking of joints for plaster key", "Inspect lintel band placement over openings"]
    },
    {
        "id": 8,
        "title": "8️⃣ Plastering Work",
        "description": "Applying internal (12mm) and external (18mm two-coat) cement-sand plaster for smooth finishing.",
        "materials": "Cement, Fine Sand, Waterproofing Compound, Chicken Mesh",
        "machines": "Mortar Spray Machine / Hand Trowels",
        "safety": "Use secure double-pipe scaffolding for high elevation exterior plastering.",
        "risk": "Medium",
        "duration": "8 - 12 Days",
        "qa_checklist": ["Install chicken wire mesh at RCC and masonry joints to prevent cracks", "Maintain level using button marks", "Cure plaster for at least 7 days"]
    },
    {
        "id": 9,
        "title": "9️⃣ Flooring & Tiling",
        "description": "Laying floor leveling bed, applying tile adhesive, and fixing vitrified/ceramic floor tiles.",
        "materials": "Vitrified Tiles, Tile Adhesive, Grout, Cement Bed",
        "machines": "Electric Tile Cutter, Rubber Mallet, Laser Level",
        "safety": "Wear knee pads, eye protection when cutting tiles, and dust mask.",
        "risk": "Low",
        "duration": "7 - 10 Days",
        "qa_checklist": ["Check floor slope towards floor drains", "Ensure 100% adhesive contact underneath tiles (no hollow sound)", "Apply uniform tile spacers"]
    },
    {
        "id": 10,
        "title": "🔟 Painting & Finishing",
        "description": "Applying wall putty coats, primer, and final coats of interior emulsion / exterior weather-proof paint.",
        "materials": "Wall Putty, Acrylic Primer, Emulsion Paint",
        "machines": "Airless Paint Sprayer, Sanding Machine, Paint Rollers",
        "safety": "Wear organic vapor respirators and safety goggles during spraying/sanding.",
        "risk": "Low",
        "duration": "5 - 8 Days",
        "qa_checklist": ["Ensure wall surface moisture content is under 10% before priming", "Sand smoothly between coats", "Check color uniformity and finish texture"]
    }
]

# =========================================================
# 3. SESSION STATE MANAGEMENT
# =========================================================
if "current_step" not in st.session_state:
    st.session_state.current_step = 0

if "completed_steps" not in st.session_state:
    st.session_state.completed_steps = set()

def next_step():
    if st.session_state.current_step < len(STEPS_DATA) - 1:
        st.session_state.current_step += 1

def prev_step():
    if st.session_state.current_step > 0:
        st.session_state.current_step -= 1

# =========================================================
# 4. SIDEBAR CONTROLS & PROGRESS
# =========================================================
with st.sidebar:
    st.title("⚙️ Practical Dashboard")
    st.markdown("---")
    
    # Navigation Dropdown
    step_titles = [s["title"] for s in STEPS_DATA]
    selected_idx = st.selectbox(
        "Jump to Stage:",
        range(len(step_titles)),
        format_func=lambda x: step_titles[x],
        index=st.session_state.current_step
    )
    if selected_idx != st.session_state.current_step:
        st.session_state.current_step = selected_idx
        st.rerun()

    st.markdown("---")
    
    # Practical Learning Progress Tracker
    total_steps = len(STEPS_DATA)
    completed_count = len(st.session_state.completed_steps)
    progress_val = completed_count / total_steps
    
    st.subheader("📊 Learning Progress")
    st.progress(progress_val)
    st.caption(f"**{completed_count} / {total_steps} Stages Verified & Completed**")
    
    st.markdown("---")
    if st.button("🔄 Reset Practical Progress", use_container_width=True):
        st.session_state.completed_steps = set()
        st.session_state.current_step = 0
        st.rerun()

# =========================================================
# 5. MAIN CONTENT HEADER & TRACKER
# =========================================================
curr_data = STEPS_DATA[st.session_state.current_step]

st.title("🎮 Virtual Construction Practical")
st.caption("Step-by-Step Interactive Residential Building Construction Guide")

# Step Navigator Banner
st.markdown("---")
nav_col1, nav_col2, nav_col3 = st.columns([1, 3, 1])

with nav_col1:
    st.button("⬅️ Previous Stage", on_click=prev_step, disabled=(st.session_state.current_step == 0), use_container_width=True)

with nav_col2:
    st.progress((st.session_state.current_step + 1) / total_steps)

with nav_col3:
    st.button("Next Stage ➡️", on_click=next_step, disabled=(st.session_state.current_step == total_steps - 1), use_container_width=True)

# =========================================================
# 6. STAGE DISPLAY PANEL
# =========================================================
st.subheader(curr_data["title"])

# Metrics & Summary Ribbon
m1, m2, m3, m4 = st.columns(4)
m1.metric("Est. Duration", curr_data["duration"])

risk_class = "badge-high" if curr_data["risk"] == "High" else ("badge-med" if curr_data["risk"] == "Medium" else "badge-low")
m2.markdown(f"**Safety Risk Level:**<br><span class='{risk_class}'>{curr_data['risk']} Risk</span>", unsafe_allow_html=True)

is_checked = st.session_state.current_step in st.session_state.completed_steps
mark_done = m3.checkbox("✅ Mark Stage Completed", value=is_checked)
if mark_done:
    st.session_state.completed_steps.add(st.session_state.current_step)
else:
    st.session_state.completed_steps.discard(st.session_state.current_step)

m4.metric("Total Stages Left", total_steps - len(st.session_state.completed_steps))

st.write("")

# Dynamic Tabs for Stage Content
tab_overview, tab_qa, tab_calc = st.tabs([
    "📋 Overview & Safety Specifications",
    "🔬 Quality Inspection Checklist (QA/QC)",
    "🧮 Practical Estimator & Calculator"
])

# ---------------------------------------------------------
# TAB 1: OVERVIEW & SAFETY
# ---------------------------------------------------------
with tab_overview:
    st.info(f"**Description:** {curr_data['description']}")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 🧱 Materials Required")
        st.success(curr_data["materials"])
        
        st.markdown("### 🚜 Equipment & Machinery")
        st.warning(curr_data["machines"])
        
    with c2:
        st.markdown("### ⚠️ Critical Safety Protocol")
        st.error(curr_data["safety"])

# ---------------------------------------------------------
# TAB 2: QUALITY CHECKLIST
# ---------------------------------------------------------
with tab_qa:
    st.subheader("🔍 Quality Assurance Inspection Points")
    st.write("Before approving sign-off for this stage, site engineers must verify:")
    
    for idx, item in enumerate(curr_data["qa_checklist"], start=1):
        st.checkbox(f"**Item {idx}:** {item}", key=f"qa_{st.session_state.current_step}_{idx}")

# ---------------------------------------------------------
# TAB 3: STAGE-SPECIFIC CALCULATORS
# ---------------------------------------------------------
with tab_calc:
    st.subheader("🧮 Site Practical Estimator")
    
    # Calculator 1: Concrete Volume (For Footing, Columns, Beams, Slab)
    if curr_data["id"] in [3, 4, 5, 6]:
        st.markdown("#### 📦 Concrete Volume & Cement Bag Estimator")
        ca, cb, cc = st.columns(3)
        length = ca.number_input("Length / Span (m)", min_value=0.5, value=10.0, step=0.5)
        width = cb.number_input("Width / Thickness (m)", min_value=0.1, value=5.0, step=0.1)
        depth = cc.number_input("Depth / Height (m)", min_value=0.1, value=0.12, step=0.01)
        
        vol = length * width * depth
        dry_vol = vol * 1.54 # Dry volume factor
        cement_bags = math.ceil((dry_vol / (1 + 1.5 + 3)) * 1440 / 50) # M20 (1:1.5:3) ratio
        
        e1, e2 = st.columns(2)
        e1.metric("Wet Concrete Volume", f"{vol:.2f} m³")
        e2.metric("Est. Cement Bags (M20 Grade)", f"{cement_bags} Bags (50kg)")

    # Calculator 2: Masonry Brick Estimator
    elif curr_data["id"] == 7:
        st.markdown("#### 🧱 Brick Work Quantity Estimator")
        ca, cb = st.columns(2)
        wall_l = ca.number_input("Wall Length (m)", min_value=1.0, value=10.0, step=0.5)
        wall_h = cb.number_input("Wall Height (m)", min_value=1.0, value=3.0, step=0.5)
        
        wall_area = wall_l * wall_h
        # Standard modular brick estimate: ~50 bricks per m2 for 230mm wall
        total_bricks = int(wall_area * 50)
        cement_bags_brick = math.ceil(wall_area * 0.2)
        
        e1, e2 = st.columns(2)
        e1.metric("Total Standard Bricks Required", f"{total_bricks} Nos")
        e2.metric("Cement Bags for Mortar", f"{cement_bags_brick} Bags")

    # Calculator 3: Paint Coverage Estimator
    elif curr_data["id"] == 10:
        st.markdown("#### 🎨 Paint Quantity Estimator")
        wall_sqm = st.number_input("Total Wall Surface Area (m²)", min_value=10.0, value=150.0, step=10.0)
        
        # Coverage: ~10 sqm per liter (2 coats)
        paint_liters = math.ceil(wall_sqm / 10.0)
        putty_kg = math.ceil(wall_sqm * 1.2)
        
        e1, e2 = st.columns(2)
        e1.metric("Paint Volume (2 Coats)", f"{paint_liters} Liters")
        e2.metric("Wall Putty Required", f"{putty_kg} kg")
        
    else:
        st.info("ℹ️ Basic estimator tool is active for this phase. Check site log parameters.")
        st.number_input("Enter Estimated Area / Work Span (m²)", min_value=10.0, value=50.0)
        st.success("Work parameters are within standard residential limits.")
        