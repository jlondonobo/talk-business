import streamlit as st
from utils.options import COUNTIES
from utils.plots.blocks import plot_blocks_choropleth

st.set_page_config(
    page_title="The Big Apple",
    layout="wide",
)
from utils.loaders.census import get_total_population

st.markdown("# Provisional title")

counties = st.multiselect("Select a county", COUNTIES, COUNTIES)
population = get_total_population(counties)

map = plot_blocks_choropleth(population, "CENSUS_BLOCK_GROUP", "TOTAL_POPULATION")
st.plotly_chart(map, use_container_width=True)
