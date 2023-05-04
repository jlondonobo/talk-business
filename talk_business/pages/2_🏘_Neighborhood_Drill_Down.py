import json

import pandas as pd
import streamlit as st
from utils.utils import load_css

st.set_page_config(
    page_title="Neighborhood Drill Down",
    layout="wide",
    page_icon="talk_business/assets/favicon.png",
)
load_css("talk_business/assets/neighborhoods.css")


from utils.flows import distributions
from utils.names import get_county_name, get_nta_name
from utils.plots.blocks import plot_blocks_choropleth
from utils.plots.neighborhood import treemap
from utils.sql import neighborhood_explorer as ne
from utils.transformers import dissolve
from utils.transformers import neighborhood as ntransform

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
    <h1> Neighborhood Drilldown </h1>
    <div class='subtitle'><h2>📍 {get_nta_name(nta_select)} 📍</h2><h3>{get_county_name(county_select)} County</h5></div>
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
    st.markdown("<p class='unit'>People</p>", unsafe_allow_html=True)
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
    st.markdown("<p class='unit'>USD</p>", unsafe_allow_html=True)

with col3:
    avg_rent = statistic(nta_select, 'AVG_RENT')
    st.metric(
        label="Average gross monthly rent",
        value=f"${avg_rent:,.0f}",
        help="Gross rent includes monthly rent and any services such as internet, energy, and water."
    )
    st.markdown("<p class='unit'>USD</p>", unsafe_allow_html=True)


def potential_spending_tag(spending):
    if spending > 1_999_999_999:
        return "Top spending potential"


def price_tag(rent_price: float):
    if rent_price > 1_999:
        return "Luxury neighborhood"
    elif rent_price <= 1_000:
        return "Affordable neighborhood"


def race_tag(race_data: pd.DataFrame):
    if race_data["pop_share"].max() > 0.6:
        max_group = race_data["pop_share"].idxmax()

        if max_group == "👩🏼👨🏻 White":
            return "Mostly white population"
        elif max_group == "👨🏾👩🏾 Black or African American":
            return "Mostly african-american population"
        elif max_group == "👲🏻 Asian":
            return "Mostly asian population"


def subway_tag(subway_count: int):
    if subway_count > 3:
        return "High subway access"
    elif subway_count == 0:
        return "No subway access"
    else:
        return "Subway access"


def compile_tags(tags: list) -> str:
    return " ".join([f"<div class='tag'>{tag}</div>" for tag in tags])

# Machete
race = ne.get_distribution("RACE_GROUPS", nta_select)
race = ntransform.transform_race(race).set_index("RACE_GROUPS")
suway_count = ne.get_nta_subway_station_count(nta_select)


TAGS = []
TAGS.append(potential_spending_tag(spending))
TAGS.append(price_tag(avg_rent))
TAGS.append(race_tag(race))
TAGS.append(subway_tag(suway_count))
TAGS = [tag for tag in TAGS if tag is not None]

col1, col2 = st.columns(2)
with col1:
    st.markdown("#### Neighborhood personality")
    st.markdown(
        f"""
        <div class="tag-list">
            {compile_tags(TAGS)}
        </div>
        """,
        unsafe_allow_html=True,
    )

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
        mapbox_style="mapbox://styles/jlondonobo/clh3uciej019a01pa6tas2286",
    )
    st.plotly_chart(plot, use_container_width=True)


st.markdown("#### Neighborhood details")
tab1, tab2, tab3 = st.tabs(["Demographic", "Economic", "Places"])

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
    # Places
    treemap_data = ne.get_neighborhood_treemap_data(nta_select)
    treemap_data = treemap_data.fillna("Other")

    treemap_plot = treemap(treemap_data, get_nta_name(nta_select))
    st.plotly_chart(treemap_plot, use_container_width=True)

    # # Enrollment
    # enrollemnt_plot = distributions.plot_enrollment_dist(
    #     county_select,
    #     nta_select,
    #     share,
    #     compare_county,
    # )
    # st.plotly_chart(enrollemnt_plot, use_container_width=True)
