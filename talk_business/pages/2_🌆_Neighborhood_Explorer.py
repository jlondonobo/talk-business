import streamlit as st

st.set_page_config(
    page_title="🌆 Neighborhood Explorer",
    layout="wide",
)
from utils.flows import distributions
from utils.names import get_county_name, get_nta_name
from utils.plots.blocks import plot_blocks_choropleth
from utils.sql import neighborhood_explorer as ne

DISPLAY_COUNTIES = ["005", "047", "061", "081", "085"]

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


col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(
        label="Population",
        value=f"{statistic(nta_select, 'POPULATION')/ 1000:,.0f}K",
    )
    st.markdown("People")
with col2:
    st.metric(
        label="Total income",
        value=f"${statistic(nta_select, 'TOTAL_INCOME') / 1_000_000:,.0f}",
    )
    st.markdown("Million dollars")

with col3:
    st.metric(
        label="Density",
        value=f"{statistic(nta_select, 'POP_DENSITY') / 1000:,.0f}K",
    )
    st.markdown("People / sq. mi.")
with col4:
    st.metric(
        label="Area",
        value=f"{statistic(nta_select, 'AREA'):.2f}",
    )
    st.markdown("sq. mi.")
    

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Neighborhood Persona")

with col2:
    shapes = ne.get_nta_geoms()
    shape = shapes.query("NTA_CODE == @nta_select").assign(
        COUNTY=get_county_name(county_select), NTA_NAME=get_nta_name(nta_select)
    )
    centroid = shape["geometry"].values[0].centroid
    plot = plot_blocks_choropleth(
        shape,
        "NTA_CODE",
        None,
        center={"lat": centroid.y, "lon": centroid.x},
        uichange=True,
        zoom=10,
    )
    plot.update_traces(
        marker_opacity=0.5, marker_line_width=1, marker_line_color="black"
    )
    plot.update_layout(height=200)
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
