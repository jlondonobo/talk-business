import streamlit as st
from utils.utils import app_base_config, load_css

app_base_config()
load_css("talk_business/assets/hello.css")

st.markdown(
    """
    <div class=title>
        <div style=" justify-content: center;">
            <h1 style="text-align: center; padding: 5px;">Talk Business</h1>
            <p style="text-align: center;"><i>Grow your business in New York City. Connect with your audience through data.</i></p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown(
        '<p class="attribution">A visual exploration platform by <a href="https://twitter.com/jlondonobo">Jose Londono</a></p>',
        unsafe_allow_html=True,
    )
    
    st.markdown(
        '<p class="attribution">Learn how to use it with the <a href="https://youtu.be/4tWG5e6-olU">walkthrough</a></p>',
        unsafe_allow_html=True,
    )
    
    # st.markdown(
    #     '<p class="icon-attribution">Statue of Liberty icon created by <a href="https://www.flaticon.com/free-icons/statue-of-liberty" title="statue of liberty icons">Freepik - Flaticon</a></footer>',
    #     unsafe_allow_html=True,
    # )

with st.expander("What is Talk Business?"):
    st.markdown(
        """
        - **Talk Business** is a visual exploration platform designed to help you **grow your business** in New York City. 🗽🇺🇸
        - Open a new store, focus your marketing efforts, and create campaigns that reach your target audience.
        """
    )

with st.expander("How can I use Talk Business?"):
    st.markdown(
        """
        You can use Talk Business in any way that fits your needs! However, we suggest the following approach:
        <ol>
        <li> Go to the <a href='/City_Explorer'>🗺 City Explorer</a> and discover patterns that matter to your business.
        <li> Use different variable combinations and create a list of potential neighborhoods.
        <li> Go to <a href='/Neighborhood_Drill_Down'>🏙 Neighborhood Drill Down</a> and find detailed neighborhood information to help you guide your decision.
        </ol>
    """,
    unsafe_allow_html=True
    )
with st.expander("What is Talk Business' offer?"):
    st.markdown(
        """
        Take 5 minutes to explore Talk Business and get:

        ✅ An initial idea of where you should open your next store, backed by data.

        ✅ Actionable target audience insights to power up your next marketing campaign.

        ✅ Personalized maps that fit your specific business needs.
        """
    )

# Logo color: #a9a9a9
with st.expander("What are the **data sources** powering Talk Business?"):
    st.markdown(
        """
        <div style="display: flex; align-items: center; justify-content: center; width: 100%;">
            <div class="card">
                <a href="https://app.snowflake.com/marketplace/listing/GZSNZ2UNN0/safegraph-us-open-census-data-neighborhood-insights-free-dataset">
                    <div class="logo-wrapper">
                        <object class="logo" data="https://svgshare.com/i/sh6.svg" type="image/svg+xml"></object>
                    </div>
                </a>
                <div class="text">
                    <p class="h3"> US Open Census Data </p>
                    <p class="p"> SafeGraph<br>(Snowflake Marketplace)</p>
                    <p class="dataset-description"> 2020 US Census data with 7,500+ demographic attributes available at a block level. </p>
                </div>
            </div>
            <div class="card">
                <a href="https://app.snowflake.com/marketplace/listing/GZT0ZHT9NV1/foursquare-foursquare-places-new-york-city-sample">
                    <div class="logo-wrapper">
                        <object class="logo" data="https://svgshare.com/i/sh5.svg" type="image/svg+xml"></object>
                    </div>
                </a>
                <div class="text">
                    <p class="h3"> New York City Places </p>
                    <p class="p"> Foursquare<br>(Snowflake Marketplace)</p>
                    <p class="dataset-description"> Details of 300,000 places in New York City. Refreshed every day. </p>
                </div>
            </div>
            <div class="card">
                <a href="https://data.cityofnewyork.us/Transportation/Subway-Stations/arq3-7z49">
                    <div class="logo-wrapper">
                        <object class="logo" data="https://svgshare.com/i/sjM.svg" type="image/svg+xml"></object>
                    </div>
                </a>
                <div class="text">
                    <p class="h3"> NYC Subway Locations & Ridership </p>
                    <p class="p"> MTA </p>
                    <p class="dataset-description"> NYC's 473 Subway station locations and daily ridership. </p>
                </div>
            </div>
            <div class="card">
                <a href="https://www.nyc.gov/site/planning/data-maps/open-data/census-download-metadata.page">
                    <div class="logo-wrapper">
                        <object class="logo" data="https://svgshare.com/i/siW.svg" type="image/svg+xml"></object>
                    </div>
                </a>
                <div class="text">
                    <p class="h3"> Neighborhood Tabulation Areas </p>
                    <p class="p"> NYC Department of City Planning </p>
                    <p class="dataset-description"> Geographic boundaries for NYC neighborhoods</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
