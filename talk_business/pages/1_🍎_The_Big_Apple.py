import streamlit as st
from utils.columns import GROUPED_COUNTS, GROUPED_STATS, STATS
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
    data = get_total_population(counties)
    colname = metric

elif metric in GROUPED_STATS:
    variant = st.radio("Select a variant", list(GROUPED_STATS[metric].keys()), index=0)
    colname = f"{metric}_{variant}"
    data = get_simple_column(counties, GROUPED_STATS[metric][variant], colname)

elif metric in GROUPED_COUNTS:
    variant = st.radio("Select a variant", list(GROUPED_COUNTS[metric].keys()), index=0)
    agg_type = st.radio("Aggregation", ["TOTAL", "PERCENTAGE"], index=0)
    colname = f"{metric}_{variant}_{agg_type}"    
    data = get_simple_column(counties, GROUPED_COUNTS[metric][variant], colname, agg_type)


map = plot_blocks_choropleth(data, "CENSUS_BLOCK_GROUP", colname.upper())
st.plotly_chart(map, use_container_width=True)