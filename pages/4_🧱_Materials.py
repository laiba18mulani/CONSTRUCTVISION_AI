import streamlit as st
import json
import pandas as pd
from pathlib import Path

# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Material Library",
    page_icon="🧱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# 2. CUSTOM CSS (DARK THEME & CARDS)
# =========================================================
st.markdown("""
<style>
    /* Dark Theme Base Adjustments */
    .stApp {
        background-color: #0E1117;
        color: #E0E0E0;
    }
    
    /* Highlight Cards */
    div[data-testid="column"] {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 15px;
        transition: border-color 0.3s ease;
    }
    
    div[data-testid="column"]:hover {
        border-color: #238636;
    }
    
    /* Custom Badge */
    .material-badge {
        background-color: #238636;
        color: white;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. DATA LOADER & BASE SETUP
# =========================================================
BASE_PATH = Path("assets/materials/images")
BASE_PATH.mkdir(parents=True, exist_ok=True)

DEFAULT_MATERIALS = [
    {"id": "cement", "name": "Cement", "category": "Binders"},
    {"id": "sand", "name": "Fine Sand", "category": "Aggregates"},
    {"id": "steel", "name": "Structural Steel", "category": "Metals"},
    {"id": "brick", "name": "Clay Brick", "category": "Masonry"},
    {"id": "concrete", "name": "Concrete", "category": "Composite"},
    {"id": "paint", "name": "Protective Paint", "category": "Finishes"},
    {"id": "tiles", "name": "Ceramic Tiles", "category": "Finishes"}
]

@st.cache_data
def load_materials_dynamically(base_path: Path):
    materials = list(DEFAULT_MATERIALS)
    existing_ids = {m["id"] for m in materials}
    
    if base_path.exists():
        for folder in base_path.iterdir():
            if folder.is_dir() and folder.name not in existing_ids:
                meta_file = folder / "metadata.json"
                if meta_file.exists():
                    try:
                        with open(meta_file, "r", encoding="utf-8") as f:
                            data = json.load(f)
                    except Exception:
                        data = None
                else:
                    data = {
                        "id": folder.name,
                        "name": folder.name.replace("_", " ").title(),
                        "category": "Uncategorized"
                    }
                if data:
                    materials.append(data)
    return materials

MATERIALS_DATA = load_materials_dynamically(BASE_PATH)

# =========================================================
# 4. MODAL DIALOG COMPONENT
# =========================================================
@st.dialog("🔬 Technical Material Specification", width="large")
def show_material_modal(item, image_path, text_content):
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if image_path:
            st.image(str(image_path), use_container_width=True)
        else:
            st.warning("⚠️ Image file not found.")
            
        st.markdown(f"**Category:** `{item['category']}`")
        st.markdown(f"**Material ID:** `{item['id']}`")
        
    with col2:
        st.title(item["name"])
        st.markdown(text_content)
        
    st.divider()
    st.download_button(
        label="📥 Download Official Datasheet",
        data=text_content,
        file_name=f"{item['id']}_specifications.txt",
        mime="text/plain",
        key=f"modal_dl_{item['id']}"
    )

# =========================================================
# 5. SIDEBAR SEARCH & FILTERS
# =========================================================
st.sidebar.title("🔍 Search & Filter")

search_term = st.sidebar.text_input("Search Materials", placeholder="e.g., Cement, Steel...")

categories = ["All"] + sorted(list(set(item["category"] for item in MATERIALS_DATA)))
selected_category = st.sidebar.selectbox("Filter by Category", categories)

# Filter logic
filtered_materials = [
    mat for mat in MATERIALS_DATA
    if (search_term.lower() in mat["name"].lower() or search_term.lower() in mat["id"].lower())
    and (selected_category == "All" or mat["category"] == selected_category)
]

# =========================================================
# 6. HEADER & METRICS
# =========================================================
st.title("🧱 Civil Engineering Material Library")
st.caption("Interactive catalog of essential construction materials with specs and technical sheets.")
st.divider()

m1, m2, m3 = st.columns(3)
m1.metric("Total Items", len(MATERIALS_DATA))
m2.metric("Filtered View", len(filtered_materials))
m3.metric("Categories", len(categories) - 1)

st.write("")

# =========================================================
# 7. MAIN INTERACTIVE TABS
# =========================================================
tab_grid, tab_compare, tab_admin = st.tabs([
    "📚 Catalog Grid", 
    "⚖️ Material Comparison", 
    "➕ Add New Material"
])

# ---------------------------------------------------------
# TAB 1: CATALOG GRID
# ---------------------------------------------------------
with tab_grid:
    if not filtered_materials:
        st.info("No materials match your current search/filter criteria.")
    else:
        cols = st.columns(3)
        
        for i, item in enumerate(filtered_materials):
            mat_id = item["id"]
            mat_name = item["name"]
            category = item["category"]
            folder = BASE_PATH / mat_id
            
            # Find image path
            image_path = None
            for ext in [".jpg", ".jpeg", ".png", ".webp"]:
                candidate = folder / f"{mat_id}{ext}"
                if candidate.exists():
                    image_path = candidate
                    break

            # Read info text
            info_path = folder / "info.txt"
            text_content = "No extra specifications provided."
            if info_path.exists():
                try:
                    with open(info_path, "r", encoding="utf-8") as f:
                        text_content = f.read()
                except Exception as e:
                    text_content = f"Error reading file: {e}"

            with cols[i % 3]:
                st.markdown(f'<span class="material-badge">{category}</span>', unsafe_allow_html=True)
                st.subheader(mat_name)

                if image_path:
                    st.image(str(image_path), use_container_width=True)
                else:
                    st.warning("⚠️ Image unavailable")

                if st.button("🔍 Detailed Specs", key=f"btn_{mat_id}", use_container_width=True):
                    show_material_modal(item, image_path, text_content)

# ---------------------------------------------------------
# TAB 2: COMPARISON MATRIX
# ---------------------------------------------------------
with tab_compare:
    st.subheader("⚖️ Material Properties Comparison Matrix")
    
    selected_names = st.multiselect(
        "Select materials to compare side-by-side:",
        options=[m["name"] for m in MATERIALS_DATA],
        default=[MATERIALS_DATA[0]["name"], MATERIALS_DATA[2]["name"]] if len(MATERIALS_DATA) >= 2 else []
    )
    
    if selected_names:
        comp_items = [m for m in MATERIALS_DATA if m["name"] in selected_names]
        
        comparison_data = {
            "Property": ["Category", "Compressive Strength (MPa)", "Density (kg/m³)", "Fire Rating", "Relative Cost"],
            **{
                m["name"]: [m["category"], "25 - 50", "2400", "Class A", "$$"]
                for m in comp_items
            }
        }
        st.table(comparison_data)
    else:
        st.info("Select at least one material above to compare.")

# ---------------------------------------------------------
# TAB 3: ADMIN UPLOAD FORM
# ---------------------------------------------------------
with tab_admin:
    st.subheader("➕ Add New Material to Library")
    
    with st.form("add_material_form", clear_on_submit=True):
        col_a, col_b = st.columns(2)
        with col_a:
            new_id = st.text_input("Material ID (e.g., timber)").lower().strip()
            new_name = st.text_input("Material Name (e.g., Structural Timber)")
        with col_b:
            new_category = st.selectbox("Category", ["Binders", "Aggregates", "Metals", "Masonry", "Composite", "Finishes", "Timber"])
            new_image = st.file_uploader("Upload Image", type=["jpg", "png", "webp", "jpeg"])
            
        new_specs = st.text_area("Technical Specs (Markdown supported)")
        
        submitted = st.form_submit_button("💾 Save Material")
        
        if submitted:
            if not new_id or not new_name:
                st.error("Please fill in both Material ID and Material Name.")
            else:
                target_dir = BASE_PATH / new_id
                target_dir.mkdir(parents=True, exist_ok=True)
                
                # Save Image
                if new_image:
                    ext = Path(new_image.name).suffix
                    with open(target_dir / f"{new_id}{ext}", "wb") as f:
                        f.write(new_image.getbuffer())
                
                # Save metadata.json
                meta_data = {"id": new_id, "name": new_name, "category": new_category}
                with open(target_dir / "metadata.json", "w", encoding="utf-8") as f:
                    json.dump(meta_data, f, indent=4)

                # Save info.txt
                with open(target_dir / "info.txt", "w", encoding="utf-8") as f:
                    f.write(new_specs if new_specs else "No specs provided.")
                    
                st.success(f"Material '{new_name}' created successfully in `{target_dir}`!")
                st.cache_data.clear()
                st.rerun()
                