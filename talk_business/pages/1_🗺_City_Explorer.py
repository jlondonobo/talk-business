import json

import streamlit as st
from utils.columns import COLUMNS
from utils.load_local_data import load_nta_centroids
from utils.options import COUNTIES, METRICS
from utils.plots.histograms import plot_distribution_by_area
from utils.transformers.dissolve import (
    dissolve_business_count,
    dissolve_count,
    dissolve_weighted_average,
)
from utils.utils import load_css

st.set_page_config(
    page_title="City Explorer",
    layout="wide",
    page_icon="talk_business/assets/favicon.png"
)
load_css("talk_business/assets/explorer.css")

# Need to load this after setting page config
# else the page will crash due to not being first function ran
from utils.load_local_data import load_nta_centroids
from utils.names import get_county_name, get_nta_name
from utils.plots.blocks import plot_blocks_choropleth
from utils.sql.us_census_2020 import (
    get_bounding_box_points,
    get_main_stats,
    get_nta_shapes,
    get_parks,
    get_poi_count,
    get_simple_column,
    get_subway_stations,
)

st.markdown(
    """
    <h1 style="text-align: center;"> Explore New York City </h1>
    """,
    unsafe_allow_html=True
)

DISPLAY_COUNTIES = ["061", "047", "081", "005",  "085"]
with st.sidebar:
    counties = st.multiselect(
        "Choose the **boroughs** you want to explore", DISPLAY_COUNTIES, DISPLAY_COUNTIES[0], format_func=get_county_name
    )
    if not counties:
        st.warning("Please select at least one borough.")
        st.stop()

    level = st.radio(
        "Select an aggregation level",
        ["TRACT", "BLOCK"],
        format_func=lambda x: f"{x.title()}s",
        horizontal=True,
        help="Use **tracts** for easier exploration. Use **blocks** for more detail."
    )
    display_ntas = st.checkbox("Display neighborhood boundaries", value=False, help="Neighborhood names will show on hover.")

    maps = st.radio("How many characteristics do you want to explore?", [1, 2, 3], index=1, horizontal=True)

    st.markdown("Extended layers")
    activate_subway_stations = st.checkbox("Subway stations", value=False)
    activate_parks = st.checkbox("Parks", value=False)


def get_stat(counties: str, stat) -> int:
    main_stats = get_main_stats()   
    return main_stats.loc[counties, stat].sum()


col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(
        label="Population",
        value=f"{get_stat(counties, 'TOTAL_POPULATION'):,.0f}",
    )
    st.markdown("<p class='unit'>People</p>", unsafe_allow_html=True)
with col2:
    st.metric(
        label="Households",
        value=f"{get_stat(counties, 'TOTAL_HOUSEHOLDS'):,.0f}",
    )
    st.markdown("<p class='unit'>Households</p>", unsafe_allow_html=True)
with col3:
    st.metric(
        label="Potential spending",
        value=f"${get_stat(counties, 'TOTAL_INCOME') / 1_000_000_000:,.0f} Billion",
    )
    st.markdown("<p class='unit'>USD</p>", unsafe_allow_html=True)
with col4:
    st.metric(
        label="Points of interest",
        value=f"{get_stat(counties, 'TOTAL_PLACES'):,.0f}",
    )
    st.markdown("<p class='unit'>Places</p>", unsafe_allow_html=True)


area, centroid = get_bounding_box_points(counties)

if display_ntas:
    nta_shapes = json.loads(get_nta_shapes(counties).to_json())
else:
    nta_shapes = None


zoom = 12
if area > 260_000_000:
    zoom = 10
if area > 1_000_000_000:
    zoom = 9


columns = st.columns(maps)
for index, col in enumerate(columns):
    metric = col.selectbox("Select a variable", list(METRICS.keys()), format_func=METRICS.get, index=index, key=index)

    id = "CENSUS_BLOCK_GROUP"
    if metric == "PLACES":
        col1, col2 = col.columns(2)
        with col1:
            category = st.selectbox(
                "Select a category",
                [
                    "Retail",
                    "Dining and Drinking",
                    "Business and Professional Services",
                    "Sports and Recreation",
                    "Health and Medicine",
                    "Community and Government",
                    "Arts and Entertainment",
                    "Landmarks and Outdoors",
                    "Travel and Transportation",
                ],
                index=0,
                key=f"{metric}-variant-{index}",
            )
        with col2:
            agg_type = st.radio(
                "Measurement",
                ["PERCENTAGE", "TOTAL"],
                index=0,
                format_func=lambda x: x.title(),
                horizontal=True,
                key=f"{metric}-agg_type-{index}",
            )
        data = get_poi_count(counties, category)
        data = (
            data
            .assign(
                COUNTY=lambda df: df["COUNTY_FIPS"].apply(get_county_name),
                NTA_NAME=lambda df: df["NTA_CODE"].apply(get_nta_name),
                TOTAL_COUNT=lambda df: df["TOTAL_COUNT"].astype(int).fillna(0),
                PERCENTAGE=lambda df: df["COUNT"] / df["TOTAL_COUNT"],
            )
        )
        cname = "COUNT" if agg_type == "TOTAL" else "PERCENTAGE"

        if level == "TRACT":
            if agg_type == "TOTAL":
                id = "TRACT_CODE"
                data = dissolve_business_count(data)
                data = data.assign(TRACT_CODE=lambda df: df["COUNTY_FIPS"] + df[id])
            elif agg_type == "PERCENTAGE":
                data = dissolve_business_count(data)
                data = data.assign(PERCENTAGE=lambda df: df["COUNT"] / df["TOTAL_COUNT"])
                id = "TRACT_CODE"
                data = data.assign(TRACT_CODE=lambda df: df["COUNTY_FIPS"] + df[id])

    elif COLUMNS[metric]["type"] == "COUNT_METRIC":
        data = get_simple_column(counties, metric)
        cname = metric
        if level == "TRACT":
            data = dissolve_count(data, cname)
            id = "TRACT_CODE"
            data = data.assign(TRACT_CODE=lambda df: df["COUNTY_FIPS"] + df[id])

    elif COLUMNS[metric]["type"] == "METRIC":
        data = get_simple_column(counties, metric)
        cname = metric
        if level == "TRACT":
            data = dissolve_weighted_average(data, "TRACT_CODE", cname, "TOTAL")
            id = "TRACT_CODE"
            data = data.assign(TRACT_CODE=lambda df: df["COUNTY_FIPS"] + df[id])

    elif COLUMNS[metric]["type"] == "SEGMENTED_METRIC":
        variant = col.radio(
            "Select a variant",
            list(COLUMNS[metric]["segments"].keys()),
            index=0,
            format_func=lambda x: x.replace("_", " ").title(),
            horizontal=True,
            key=f"{metric}-variant-{index}",
        )
        data = get_simple_column(counties, metric, variant)
        cname = f"{metric}-{variant}"
        if level == "TRACT":
            data = dissolve_weighted_average(data, "TRACT_CODE", cname, "TOTAL")
            id = "TRACT_CODE"
            data = data.assign(TRACT_CODE=lambda df: df["COUNTY_FIPS"] + df[id])


    elif COLUMNS[metric]["type"] == "SEGMENTED_COUNT":
        col1, col2 = col.columns(2)
        with col1:
            variant = st.selectbox(
                "Select a variant",
                list(COLUMNS[metric]["segments"].keys()),
                format_func=lambda x: x.replace("_", " ").title(),
                index=0,
                key=f"{metric}-variant-{index}",
            )
        with col2:
            agg_type = st.radio(
                "Measurement",
                ["PERCENTAGE", "TOTAL"],
                index=0,
                format_func=lambda x: x.title(),
                horizontal=True,
                key=f"{metric}-agg_type-{index}",
            )
        cname = f"{metric}-{variant}"
        data = get_simple_column(counties, metric, variant, agg_type)
        if level == "TRACT":
            if agg_type == "TOTAL":
                id = "TRACT_CODE"
                data = dissolve_count(data, cname)
                data = data.assign(TRACT_CODE=lambda df: df["COUNTY_FIPS"] + df[id])
            elif agg_type == "PERCENTAGE":
                data = dissolve_weighted_average(data, "TRACT_CODE", cname, "TOTAL")
                id = "TRACT_CODE"
                data = data.assign(TRACT_CODE=lambda df: df["COUNTY_FIPS"] + df[id])


    nta_labels = load_nta_centroids(counties)
    parks = None
    if activate_parks:
        parks = get_parks(counties)    

    map = plot_blocks_choropleth(
        data,
        id,
        cname,
        center={"lat": centroid.y, "lon": centroid.x},
        zoom=zoom,
        uichange=True,
        borders=nta_shapes,
        nta_centroids=nta_labels,
        parks=parks,
    )
    if activate_subway_stations:
        stations = get_subway_stations(counties)
        map.add_scattermapbox(
            "above",
            lat=stations["station_latitude"],
            lon=stations["station_longitude"],
            text=stations["station_name"],
            name="Subway stations",
            customdata=stations["ridership"].apply(lambda x: f"{x:,.0f}").replace("nan", "Statistic comming in the future..."),
            marker=dict(
                color="#3B7B9C",
                size=stations["ridership"].where(stations["ridership"].notna(), 8),
                sizemode="area",
                sizemin=8,
                sizeref=stations["ridership"].max() / 50 ** 2,
            ),
            opacity=0.8,
            hovertemplate=(
                'Station name: <b>%{text}</b><br>'
                'Avg. weekday passengers: <b>%{customdata}</b><extra></extra>'
            ),
            hoverlabel=dict(bgcolor="#2D3847"),
        )

    col.plotly_chart(map, use_container_width=True)
    histogram = plot_distribution_by_area(data, cname)
    col.plotly_chart(histogram, use_container_width=True)
