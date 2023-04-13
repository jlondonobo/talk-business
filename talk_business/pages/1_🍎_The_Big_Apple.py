import streamlit as st
from utils.columns import GROUPED_COUNTS, GROUPED_STATS, STATS
from utils.options import COUNTIES, METRICS
from utils.plots.blocks import plot_blocks_choropleth
from utils.plots.histograms import plot_distribution_by_area

st.set_page_config(
    page_title="The Big Apple",
    layout="wide",
)

# Need to load this after setting page config
# else the page will crash due to not being first function ran
from utils.loaders.census import get_simple_column, get_statistics, get_total_population

st.markdown("# Provisional title")

counties = st.multiselect("Select a county", COUNTIES, COUNTIES[0])
metric = st.selectbox("Select a metric", list(METRICS.keys()), format_func=METRICS.get)

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

# Get Data
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
    data = get_simple_column(
        counties, GROUPED_COUNTS[metric][variant], colname, agg_type
    )


map = plot_blocks_choropleth(data, "CENSUS_BLOCK_GROUP", colname.upper())
st.plotly_chart(map, use_container_width=True)

histogram = plot_distribution_by_area(data, colname.upper())
st.plotly_chart(histogram, use_container_width=True)

