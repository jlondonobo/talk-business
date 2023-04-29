import json

import streamlit as st

st.set_page_config(
    page_title="🌆 Neighborhood Explorer",
    layout="wide",
)
from utils.flows import distributions
from utils.names import get_county_name, get_nta_name
from utils.plots.blocks import plot_blocks_choropleth
from utils.sql import neighborhood_explorer as ne
from utils.transformers import dissolve

DISPLAY_COUNTIES = ["061", "081", "005", "047", "085"]

# Sidebar
with st.sidebar:
    county_select = st.radio(
        "County", DISPLAY_COUNTIES, 0, format_func=get_county_name, horizontal=True
    )

    nta_options = ne.get_available_nta_list(county_select)["NTA_CODE"].to_list()

    nta_select = st.selectbox("Neighborhood", nta_options, 0, format_func=get_nta_name)

    share = (
        st.radio("Distribution display", ["Percentage", "Total"], horizontal=True)
        == "Percentage"
    )
    compare_county = st.checkbox("Compare with county", value=False)


st.markdown(
    f"""
    <h1> 🌆 Neighborhood Explorer </h1>
    <h2> {get_nta_name(nta_select)} - {get_county_name(county_select)} County </h2>
    """,
    unsafe_allow_html=True,
)

STATISTICS = ne.fetch_neighborhood_statistics()


def statistic(nta_code: str, statistic: str) -> float:
    return ne.neighborhood_stat(STATISTICS, nta_code, statistic)


col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
        label="Population",
        value=f"{statistic(nta_select, 'POPULATION')/ 1000:,.0f}K",
    )
    st.markdown("People")
with col2:
    spending = statistic(nta_select, 'TOTAL_INCOME')
    if spending > 999_999_999:
        value = f"${spending / 1_000_000_000:,.1f}"
        ammount = "Billion"
    else:
        value = f"{spending / 1_000_000:,.0f}"  
        ammount = "Million"

    st.metric(
        label="Potential yearly spending",
        value=f"{value} {ammount}"
    )
    st.markdown("USD")

with col3:
    st.metric(
        label="Average gross monthly rent",
        value=f"${statistic(nta_select, 'AVG_RENT'):,.0f}",
        help="Gross rent includes monthly rent and any services such as internet, energy, and water."
    )
    st.markdown("USD")


col1, col2 = st.columns(2)
with col1:
    st.markdown("### Neighborhood Persona")

# Map
with col2:
    shapes = ne.get_nta_geoms()
    shape = shapes.query("NTA_CODE == @nta_select").assign(
        COUNTY=get_county_name(county_select), NTA_NAME=get_nta_name(nta_select)
    )
    centroid = shape["geometry"].values[0].centroid

    county_geom = ne.fetch_county_geoms(county_select)
    county_geom = dissolve.dissolve_simple(county_geom, "COUNTY_FIPS")["geometry"].to_json()
    county_geom = json.loads(county_geom)

    plot = plot_blocks_choropleth(
        shape,
        "NTA_CODE",
        None,
        center={"lat": centroid.y, "lon": centroid.x},
        uichange=True,
        zoom=10,
    )
    plot.update_traces(
        marker_opacity=0.5,
        marker_line_width=1,
        marker_line_color="black",   
    )
    plot.update_layout(
        height=200,
        mapbox_layers=[
            dict(
                sourcetype="geojson",
                source=county_geom,
                color="#303030",
                type="line",
                line=dict(width=1),
            )
        ],
    )
    st.plotly_chart(plot, use_container_width=True)


st.markdown("## Neighborhood details")
tab1, tab2, tab3 = st.tabs(["Demographic", "Economic", "Other"])

with tab1:
    # Age
    age_plot = distributions.plot_age_dist(
        county_select,
        nta_select,
        share,
        compare_county,
    )
    st.plotly_chart(age_plot, use_container_width=True)

    # Todo: Gender

    # Race
    race_plot = distributions.plot_race_dist(
        county_select,
        nta_select,
        share,
        compare_county,
    )
    st.plotly_chart(race_plot, use_container_width=True)

with tab2:
    # Income
    income_plot = distributions.plot_family_income_dist(
        county_select,
        nta_select,
        share,
        compare_county,
    )
    income_plot.update_layout(hovermode="x")
    st.plotly_chart(income_plot, use_container_width=True)

    # Rent
    rent_plot = distributions.plot_rent_dist(
        county_select,
        nta_select,
        share,
        compare_county,
    )
    st.plotly_chart(rent_plot, use_container_width=True)

    # Occupation
    occupation_plot = distributions.plot_occupation_dist(
        county_select,
        nta_select,
        share,
        compare_county,
    )
    st.plotly_chart(occupation_plot, use_container_width=True)


with tab3:
    # Todo: People per home

    # Enrollment
    enrollemnt_plot = distributions.plot_enrollment_dist(
        county_select,
        nta_select,
        share,
        compare_county,
    )
    st.plotly_chart(enrollemnt_plot, use_container_width=True)
