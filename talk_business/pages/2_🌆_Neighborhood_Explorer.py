import streamlit as st

# Read the data
# Plot the data
# Include plot in layout

st.set_page_config(
    page_title="🌆 Neighborhood Explorer",
    layout="wide",
)
from utils.flows import distributions
from utils.names import get_county_name, get_nta_name
from utils.plots.blocks import plot_blocks_choropleth
from utils.sql import neighborhood_explorer as ne

st.markdown("# 🌆 Neighborhood Explorer")

DISPLAY_COUNTIES = ["005", "047", "061", "081", "085"]

with st.sidebar:
    share = (
        st.radio("Distribution display", ["Share", "Total"], horizontal=True) == "Share"
    )
    compare_county = st.checkbox("Compare with county", value=False)


col1, col2 = st.columns(2)

with col1:
    county_select = st.radio(
        "County", DISPLAY_COUNTIES, 0, format_func=get_county_name, horizontal=True
    )

    nta_options = (
        ne.get_available_nta_list(county_select)["NTA_CODE"].to_list()
    )

    nta_select = st.selectbox(
        "Neighborhood", nta_options, 0, format_func=get_nta_name
    )
with col2:
    shapes = ne.get_nta_geoms()
    shape = (
        shapes
        .query("NTA_CODE == @nta_select")
        .assign(
            COUNTY=get_county_name(county_select),
            NTA_NAME=get_nta_name(nta_select))
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
    plot.update_traces(marker_opacity=0.5, marker_line_width=1, marker_line_color="black")
    plot.update_layout(height=200)
    st.plotly_chart(plot, use_container_width=True)


tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["Age", "Income", "Rent", "Race", "Occupation", "Enrollment"]
)

with tab1:
    age_plot = distributions.plot_age_dist(
        county_select,
        nta_select,
        share,
        compare_county,
    )
    st.plotly_chart(age_plot, use_container_width=True)

with tab2:
    income_plot = distributions.plot_family_income_dist(
        county_select,
        nta_select,
        share,
        compare_county,
    )
    income_plot.update_layout(hovermode="x")
    st.plotly_chart(income_plot, use_container_width=True)

with tab3:
    rent_plot = distributions.plot_rent_dist(
        county_select,
        nta_select,
        share,
        compare_county,
    )
    st.plotly_chart(rent_plot, use_container_width=True)

with tab4:
    race_plot = distributions.plot_race_dist(
        county_select,
        nta_select,
        share,
        compare_county,
    )
    st.plotly_chart(race_plot, use_container_width=True)

with tab5:
    occupation_plot = distributions.plot_occupation_dist(
        county_select,
        nta_select,
        share,
        compare_county,
    )
    st.plotly_chart(occupation_plot, use_container_width=True)

with tab6:
    enrollemnt_plot = distributions.plot_enrollment_dist(
        county_select,
        nta_select,
        share,
        compare_county,
    )
    st.plotly_chart(enrollemnt_plot, use_container_width=True)
