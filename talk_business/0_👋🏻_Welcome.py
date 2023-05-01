import streamlit as st
from utils.utils import app_base_config, load_css

app_base_config()
load_css("talk_business/assets/hello.css")

st.markdown(
    """

    <div style="background-image: url('https://images.unsplash.com/photo-1496588152823-86ff7695e68f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8bmV3JTIweW9yayUyMHNreWxpbmV8ZW58MHx8MHx8&w=1000&q=80'); border-radius: 10px; padding: 75px; background-size: 100%; background-position-y: 22%; margin: 30px auto;">
        <div style=" justify-content: center;">
            <h1 style="text-align: center; padding: 5px;">Talk Business</h1>
            <p style="text-align: center;"><i>Grow your revenue in New York City. Improve your reach through data.</i></p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.expander("What is Talk Business?"):
    st.markdown(
        """
        - **Talk Business** is a tool designed to help you make decisions in New York City 🇺🇸.
        - Open a new store, direct your marketing efforts, and understand your current public though an easy-to-use interface.
        """
    )

with st.expander("How can I use Talk Business?"):
    st.markdown(
        """
        Talk Business is designed to be used in a two-step manner:
        <ol>
        <li> Visit the <a href='/City_explorer'>🗺 City explorer</a> and make yourself comfortable with New York. Understand population patterns, such as where the youngest population lives, and where are the most expensive houses.
        <li> Once you find a neighborhood you are interested in, visit the <a href='/Neighborhood_drilldown'>🏙 Neighborhood drilldown</a> and get into its fine details. Choose your next location with the help of precise income distributions data, age and race patterns, rent prices and many more statistics.
        </ol>
    """,
    unsafe_allow_html=True
    )
with st.expander("What is Talk Business' offer?"):
    st.markdown(
        """
        **Take 5 minutes to explore the City Explorer and the Neighborhood Drilldown and you will get**:

        ✅ Data-backed insights on where you should locate your next store in New York City

        ✅ A personalized detailed dashboard to understand neighborhoods where you operate

        ✅ Spatial insights to improve your geofenced marketing campaigns and increase your revenue $$
        """
    )

with st.expander("Who are our data partners?"):
    st.markdown(
        """
        <div style="display: flex; align-items: center; justify-content: center; width: 100%;">
            <div class="card">
                <a href="https://app.snowflake.com/marketplace/listing/GZSNZ2UNN0/safegraph-us-open-census-data-neighborhood-insights-free-dataset"><span class="link"></span></a>
                <div class="logo-wrapper">
                    <object class="logo" data="https://assets-global.website-files.com/5baafc2653bd67278f206724/6388bcfd03d0621161e4626d_SafeGraph%20Logo.svg" type="image/svg+xml"></object>
                </div>
                <div class="text">
                    <p class="h3"> US Open Census Data </p>
                    <p class="p"> SafeGraph </p>
                    <p class="dataset-description"> 2020 US Census data with 7,500+ demographic attributes available at the Census Block Group level. </p>
                </div>
            </div>
            <div class="card">
                <a href="https://data.cityofnewyork.us/Transportation/Subway-Stations/arq3-7z49"><span class="link"></span></a>
                <div class="logo-wrapper">
                    <object class="logo" data="https://upload.wikimedia.org/wikipedia/commons/3/3c/MTA_NYC_logo.svg" type="image/svg+xml"></object>
                </div>
                <div class="text">
                    <p class="h3"> NYC Subway Locations & Ridership </p>
                    <p class="p"> MTA </p>
                    <p class="dataset-description"> NYC's 473 Subway station locations & daily ridership. </p>
                </div>
            </div>
            <div class="card">
                <a href="https://www.nyc.gov/site/planning/data-maps/open-data/census-download-metadata.page"><span class="link"></span></a>
                <div class="logo-wrapper">
                    <object class="logo" data="https://svgshare.com/i/se9.svg" type="image/svg+xml"></object>
                </div>
                <div class="text">
                    <p class="h3"> Neighborhood Tabulation Areas </p>
                    <p class="p"> NYC Department of City Planning </p>
                    <p class="dataset-description"> Geographic boundaries for NYC neighborhoods, and mappings to tract IDs. </p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

