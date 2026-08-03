import streamlit as st

st.set_page_config(page_title="Material Library", layout="wide")

st.title("📚 Residential Construction Material Library")

materials = {

"Cement":{
"Purpose":"Binding Material",
"Grades":"33,43,53",
"Life":"50+ Years",
"Uses":"Foundation, Beam, Slab, Column",
"Cost":"₹380-450 / Bag"
},

"Sand":{
"Purpose":"Fine Aggregate",
"Grades":"Zone I-IV",
"Life":"Permanent",
"Uses":"Concrete & Plaster",
"Cost":"₹60-90 / Cubic ft"
},

"Aggregate":{
"Purpose":"Coarse Aggregate",
"Grades":"20mm,10mm",
"Life":"Permanent",
"Uses":"Concrete",
"Cost":"₹70-100 / Cubic ft"
},

"Steel":{
"Purpose":"Reinforcement",
"Grades":"Fe415,Fe500,Fe550",
"Life":"75 Years",
"Uses":"Beam,Column,Slab",
"Cost":"₹60-70 / Kg"
},

"Bricks":{
"Purpose":"Wall Construction",
"Grades":"Class A",
"Life":"100 Years",
"Uses":"Walls",
"Cost":"₹8-15 / Brick"
},

"Concrete":{
"Purpose":"Structural Member",
"Grades":"M20,M25,M30",
"Life":"75 Years",
"Uses":"Beam,Column,Slab",
"Cost":"₹6500-8500 / m³"
},

"Tiles":{
"Purpose":"Floor Finish",
"Grades":"Vitrified,Ceramic",
"Life":"25 Years",
"Uses":"Flooring",
"Cost":"₹45-180 / sq.ft"
},

"Paint":{
"Purpose":"Surface Finish",
"Grades":"Interior,Exterior",
"Life":"7 Years",
"Uses":"Walls",
"Cost":"₹180-450 / Litre"
}

}

material = st.selectbox("Select Material", list(materials.keys()))

st.subheader(material)

col1,col2=st.columns(2)

with col1:
    st.metric("Purpose",materials[material]["Purpose"])
    st.metric("Grades",materials[material]["Grades"])
    st.metric("Life",materials[material]["Life"])

with col2:
    st.metric("Uses",materials[material]["Uses"])
    st.metric("Approx Cost",materials[material]["Cost"])

st.success("✔ AI Material Database Ready")
