import streamlit as st
from utils.columns import COLUMNS
from utils.options import COUNTIES, METRICS
from utils.plots.blocks import plot_blocks_choropleth

st.set_page_config(
    page_title="The Big Apple",
    layout="wide",
)
from utils.loaders.census import get_simple_column, get_total_population

st.markdown("# Provisional title")

counties = st.multiselect("Select a county", COUNTIES, COUNTIES[0])
metric = st.selectbox("Select a metric", list(METRICS.keys()), format_func=METRICS.get)

if metric in ["TOTAL_POPULATION", "DENSITY_POP_SQMILE"]:
    population = get_total_population(counties)

    map = plot_blocks_choropleth(population, "CENSUS_BLOCK_GROUP", metric)
    st.plotly_chart(map, use_container_width=True)

else:
    variant = st.radio("Select a variant", list(COLUMNS[metric].keys()), index=0)
    colname = f"{metric}_{variant}"

    data = get_simple_column(counties, COLUMNS[metric][variant], colname)
    
    map = plot_blocks_choropleth(data, "CENSUS_BLOCK_GROUP", colname.upper())
    st.plotly_chart(map, use_container_width=True)