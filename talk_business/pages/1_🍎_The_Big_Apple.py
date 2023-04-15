import streamlit as st
from utils.columns import COLUMNS
from utils.options import COUNTIES, METRICS
from utils.plots.blocks import plot_blocks_choropleth
from utils.plots.histograms import plot_distribution_by_area

st.set_page_config(
    page_title="The Big Apple",
    layout="wide",
)

# Need to load this after setting page config
# else the page will crash due to not being first function ran
from utils.sql.us_census_2020 import (
    get_bounding_box_points,
    get_simple_column,
    get_statistics,
    get_total_population,
)

st.markdown("# Provisional title")

counties = st.multiselect(
    "Choose the counties you want to explore", COUNTIES, COUNTIES[0]
)

summary_statistics = get_statistics(counties)

## plot map
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(
        label="Total population 👪",
        value=f"{summary_statistics.at[0, 'TOTAL_POP']:,.0f}",
    )
with col2:
    st.metric(
        label="Mean age 🎂",
        value=f"{summary_statistics.at[0, 'WEIGHTED_AVG_AGE']:.0f}",
    )
with col3:
    st.metric(
        label="Percentage female population 👩",
        value=f"{summary_statistics.at[0, 'FEMALE_PERCENT']:.1%}",
    )
with col4:
    st.metric(
        label="Mean per-capita income (12mo.) 💰",
        value=f"${summary_statistics.at[0, 'WEIGHTED_AVG_PER_CAPITA_INCOME']:,.0f}",
    )


metric = st.selectbox("Select a metric", list(METRICS.keys()), format_func=METRICS.get)
# Get Data
if metric in ["TOTAL_POPULATION", "DENSITY_POP_SQMILE"]:
    data = get_total_population(counties)
    cname = metric

elif COLUMNS[metric]["type"] == "METRIC":
    data = get_simple_column(counties, metric)
    cname = metric

elif COLUMNS[metric]["type"] == "SEGMENTED_STATISTIC":
    variant = st.radio(
        "Select a variant", list(COLUMNS[metric]["segments"].keys()), index=0
    )
    data = get_simple_column(counties, metric, variant)
    cname = f"{metric}-{variant}"

elif COLUMNS[metric]["type"] == "SEGMENTED_COUNT":
    col1, col2 = st.columns(2)
    with col1:
        variant = st.selectbox(
            "Select a variant", list(COLUMNS[metric]["segments"].keys()), index=0
        )
    with col2:
        agg_type = st.radio(
            "Aggregation", ["TOTAL", "PERCENTAGE"], index=0, horizontal=True
        )
    data = get_simple_column(counties, metric, variant, agg_type)
    cname = f"{metric}-{variant}"


area, centroid = get_bounding_box_points(counties)

zoom = 12
if area > 260_000_000:
    zoom = 11
if area > 1_000_000_000:
    zoom = 10

map = plot_blocks_choropleth(
    data,
    "CENSUS_BLOCK_GROUP",
    cname,
    center={"lat": centroid.y, "lon": centroid.x},
    zoom=zoom,
)
st.plotly_chart(map, use_container_width=True)

histogram = plot_distribution_by_area(data, cname)
st.plotly_chart(histogram, use_container_width=True)
