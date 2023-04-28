import streamlit as st
from utils.utils import app_base_config

app_base_config()

st.markdown(
    """

    <div style="background-image: url('https://images.unsplash.com/photo-1496588152823-86ff7695e68f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8bmV3JTIweW9yayUyMHNreWxpbmV8ZW58MHx8MHx8&w=1000&q=80'); border-radius: 10px; padding: 10px; background-size: 100%; background-position-y: 22%; margin: 30px auto;">
    <h1 style="text-align: center; padding: 5px;">Talk Business</h1>
    <h4 style="text-align: center; padding: 5px;"></h4>
    <h4 style="text-align: center; padding-top: 5px; padding-bottom:20px;">🏨🏙🏦</h4>
    <p style="text-align: center; padding-top: 5px; padding-bottom:20px;"><i>Understand New York City. Improve your reach through data.</i></p>
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

with st.expander("Where does Talk Business' data come from?"):
    st.markdown(
        """
        - **Demographic and economic data**: Demographic and economic insights are based on the US 2020 Census
        - **Neighbodhood divisions**: We use the latest Neighborhood Tabulation Areas (NTAs) from the NYC Department of City Planning.
        - **Subway stations**: Provided by the Metropolitan Transportation Authority (MTA).
        - **Parks**: We obtained parks and their shapes from the NYC Department of Parks and Recreation.
        """
    )