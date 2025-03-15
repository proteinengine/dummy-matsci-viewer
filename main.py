import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(
    page_title="Materials Explorer",
    layout="wide"
)

st.title("Interactive Materials Property Explorer")
st.sidebar.header("Filters")

@st.cache_data
def load_data():
    df = pd.DataFrame({
        'material_id': [f'mp-{i}' for i in range(1, 101)],
        'formula': np.random.choice(['Fe2O3', 'TiO2', 'SiO2', 'Al2O3', 'ZnO'], 100),
        'band_gap': np.random.uniform(0, 5, 100),
        'density': np.random.uniform(2, 10, 100),
        'energy_above_hull': np.random.uniform(0, 1, 100),
        'formation_energy': np.random.uniform(-5, 0, 100)
    })
    return df

data = load_data()

elements = st.sidebar.multiselect(
    "Filter by elements",
    options=['Fe', 'Ti', 'Si', 'Al', 'Zn', 'O'],
    default=['Fe', 'Ti']
)

min_band_gap, max_band_gap = st.sidebar.slider(
    "Band Gap Range (eV)",
    min_value=0.0, max_value=5.0, value=(0.0, 5.0), step=0.1
)

filtered_data = data[
    (data['band_gap'] >= min_band_gap) &
    (data['band_gap'] <= max_band_gap)
]

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Material Properties Visualization")
    
    x_property = st.selectbox("X-axis Property", ["band_gap", "density", "formation_energy"])
    y_property = st.selectbox("Y-axis Property", ["density", "band_gap", "formation_energy"])
    
    fig = px.scatter(
        filtered_data, 
        x=x_property, 
        y=y_property, 
        color="formula",
        hover_name="material_id",
        title=f"{y_property.replace('_', ' ').title()} vs {x_property.replace('_', ' ').title()}"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Material Details")
    
    formula_search = st.text_input("Search by chemical formula", "")
    
    if formula_search:
        results = data[data['formula'].str.contains(formula_search, case=False)]
        if not results.empty:
            st.write(f"Found {len(results)} materials containing '{formula_search}'")
            material = st.selectbox("Select a material", results['material_id'])
            
            st.write("### Properties")
            selected_material = data[data['material_id'] == material].iloc[0]
            for prop in ['formula', 'band_gap', 'density', 'formation_energy']:
                st.write(f"**{prop.replace('_', ' ').title()}:** {selected_material[prop]}")
        else:
            st.write(f"No materials found containing '{formula_search}'")

st.subheader("Materials Data")
st.dataframe(filtered_data.head(10))