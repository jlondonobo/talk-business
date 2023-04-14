import streamlit as st
from utils.utils import app_base_config

app_base_config()

st.markdown(
    """
    <h1 style="text-align: center; padding: 5px;">Talk Business</h1>
    <h4 style="text-align: center; padding: 5px;"></h4>
    <h4 style="text-align: center; padding-top: 5px; padding-bottom:20px;">🏨🏙🏦</h4>
    <p style="text-align: center; padding-top: 5px; padding-bottom:20px;"><i>Understand New York City. Target ✨ your ✨ prospects.</i></p>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    ## About the data

    - NTAs: Neighborhood Tabulation Areas. We collected external data
    from the NYCs Department of City Planning to aggregate data into easty-to-understand
    neighborhoods. Neighbourhood statistics and analysis are easier to
    remeber, and thus more actionable, for geographic areas we are already
    familiar with. Census blocks and tracts are not well defined in a business context.

    [More info](https://www1.nyc.gov/site/planning/data-maps/open-data/districts-download-metadata.page)
    """
)
