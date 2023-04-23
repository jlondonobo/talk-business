import streamlit as st

# Read the data
# Plot the data
# Include plot in layout

st.set_page_config(
    page_title="🌆 Neighborhood Explorer",
    layout="wide",
)
from utils.flows import distributions
from utils.plots.blocks import plot_blocks_choropleth
from utils.sql import neighborhood_explorer as ne

st.markdown("# 🌆 Negihborhood Explorer")

COUNTIES = {
    "005": "Bronx",
    "047": "Kings",
    "061": "New York",
    "081": "Queens",
    "085": "Richmond",
}

with st.sidebar:
    share = st.radio("Distribution display", ["Share", "Total"], horizontal=True) == "Share"
    compare_with_county = st.checkbox("Compare with county", value=True)


col1, col2 = st.columns(2)

with col1:
    county_select = st.radio(
        "County", list(COUNTIES.keys()), 0, format_func=COUNTIES.get, horizontal=True
    )

    nta_options = (
        ne.get_nta_list(county_select).set_index("NTA_CODE")["NTA_NAME"].to_dict()
    )

    nta_select = st.selectbox(
        "Negihborhood", list(nta_options.keys()), 0, format_func=nta_options.get
    )
with col2:
    shapes = ne.get_nta_geoms()
    shape = shapes.query("NTA_CODE == @nta_select")
    centroid = shape["geometry"].values[0].centroid
    plot = plot_blocks_choropleth(
        shape, "NTA_CODE", None, center={"lat": centroid.y, "lon": centroid.x}, uichange=True, zoom=10,
    )
    plot.update_traces(marker_opacity=0.5)
    st.plotly_chart(plot, use_container_width=True)


tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["Age", "Income", "Rent", "Race", "Occupation", "Enrollment"]
)

with tab1:
    plot = distributions.plot_distribution("AGE_GROUPS", nta_select, share)
    st.plotly_chart(plot, use_container_width=True)

with tab2:
    plot = distributions.plot_distribution("FAMILY_INCOME_GROUPS", nta_select, share)
    st.plotly_chart(plot, use_container_width=True)

with tab3:
    plot = distributions.plot_distribution("RENT_GROUPS", nta_select, share)
    st.plotly_chart(plot, use_container_width=True)

with tab4:
    plot = distributions.plot_distribution("RACE_GROUPS", nta_select, share)
    st.plotly_chart(plot, use_container_width=True)

with tab5:
    plot = distributions.plot_distribution("OCCUPATION_GROUPS", nta_select, share)
    st.plotly_chart(plot, use_container_width=True)

with tab6:
    plot = distributions.plot_distribution("ENROLLMENT_GROUPS", nta_select, share)
    st.plotly_chart(plot, use_container_width=True)
