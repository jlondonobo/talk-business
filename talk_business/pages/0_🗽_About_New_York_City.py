import geopandas as gpd
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from st_click_detector import click_detector
from utils.names import get_county_name
from utils.plots.about import plot_highlighted_choropleth
from utils.utils import load_css

load_dotenv()

st.set_page_config(
    page_title="About New York City",
    layout="wide",
    page_icon="talk_business/assets/favicon.png",
)
load_css("talk_business/assets/about.css")


def clickable_borough(county: str):
    return f'<a style="color: #7c9dc0;" href="" id="{county}">{get_county_name(county)}</a>'


st.markdown("# About New York City")


st.markdown(
    """
    New York is the **world's most renowned hub of cultural integration** 🌐. 
    With a strong financial and a media presence, the city has traditionally been a 
    highly desirable location for growing businesses. Every day, more than 9 million people from diverse cultures, ages, and ethnicities 
    go about their lives, interacting with stores, restaurants, and other 
    businesses. 

    New york has an advantageous coastal location, exceptional infrastructure, and good quality of life. 
    Business is made simple thanks to a highly educated workforce, and ease of access to capital. 
    
    As of 2022, the city had 2.3 million registered small businesses 👩‍💼 with 13% founded by Hispanic entrepreneurs. Now it's your time to join.
    """
)

st.markdown(
    """
    <img width="100%" height="500px" style="border-radius: 10px;margin-bottom: 10px; object-fit: cover;" src="https://images.unsplash.com/photo-1557211300-9991249b466a?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1742&q=80"></img>
    """,
    unsafe_allow_html=True
)


content = f"""
    <p>New York City is divided into 5 boroughs:
    {clickable_borough("061")},
    {clickable_borough("047")},
    {clickable_borough("081")},
    {clickable_borough("005")} and
    {clickable_borough("085")}.
    Each has a unique character and history.</p>
"""

clicked = click_detector(content)

st.info("Click the name of a **borough** to learn more about it", icon="💡")

EXTERNAL = {
    "061": {"population": 1_629_153, "density": 74_781, "per_capita_income": 128_000_000_000 / 1_629_153}, # manhattan
    "047": {"population": 2_576_771, "density": 39_438, "per_capita_income": 94_000_000_000 / 2_576_771}, # Brooklyn
    "081": {"population": 2_270_976, "density": 22_125, "per_capita_income": 76_000_000_000 / 2_270_976}, # Queens
    "005": {"population": 1_427_056, "density": 34_920, "per_capita_income": 32_000_000_000 / 1_427_056}, # Bronx
    "085": {"population": 475_596, "density": 8_618, "per_capita_income": 18_000_000_000 / 475_596}, # Staten Island
}
EXTERNAL = pd.DataFrame.from_dict(EXTERNAL, orient="index")


@st.cache_data
def get_geometries_with_data():
    data = gpd.read_file("talk_business/local_data/counties")
    data = data.merge(EXTERNAL, left_on="COUNTYFP", right_index=True)
    data = data.assign(name=data["COUNTYFP"].map(get_county_name))
    return data


geoms = get_geometries_with_data()


def weighted_average(data, weights):
    return (data * weights).sum() / weights.sum()

TOTAL_POPULATION = geoms["population"].sum()
TOTAL_DENSITY = 29_095
PER_CAPITA_INCOME = weighted_average(geoms["per_capita_income"], geoms["population"])

geoms_stats = geoms[["population", "density", "per_capita_income", "COUNTYFP"]].set_index("COUNTYFP")

TEXTS = {
    "061": "Manhattan is the business and financial hub of the city, with many of the world's largest corporations and financial institutions located in it. The borough has a vibrant nightlife, with many bars and restaurants that cater to the after-work crowd. It also has many high-end shopping districts, such as Fifth Avenue and Madison Avenue.",
    "047": "Brooklyn is the most populous borough and is known for its hipster culture, street art, and trendy restaurants. It is home to popular neighborhoods such as Williamsburg, Park Slope, and Brooklyn Heights. Brooklyn also has many parks and beaches, including Prospect Park and Coney Island. Brooklyn has a thriving startup and creative community, with many tech startups, advertising agencies, and media companies based in the borough. ",
    "081": "Queens is the largest borough in terms of area and is one of the most diverse counties in the United States. It is home to many ethnic enclaves, including Chinatown, Little India, and Astoria (known for its Greek community). Queens is also home to JFK International Airport and LaGuardia Airport, and many tech companies, such as Uber and JetBlue, and offers affordable office space compared to Manhattan and Brooklyn.",
    "005": "The Bronx is located north of Manhattan and is known for its cultural landmarks such as the Bronx Zoo, the New York Botanical Garden, and Yankee Stadium. It is also known for its hip-hop culture and its contribution to the birth of the genre. The Bronx is also home to several industrial zones, such as the Hunts Point Food Distribution Center, which is one of the largest food distribution centers in the world.",
    "085": "Staten Island is the least populated borough and is located south of Manhattan. It is known for its suburban feel and is often referred to as the 'forgotten borough'.",
}
st.markdown(f"""<h4 style="padding-bottom: 0px;">{get_county_name(clicked) if clicked else "New York City"}</h4>""", unsafe_allow_html=True)

if clicked:
    st.markdown(TEXTS[clicked])

st.markdown(
    f"""
    <ul>
    <li><i>Total population: <b>{geoms_stats.at[clicked, "population"] if clicked else TOTAL_POPULATION:,}</b></i>
    <li><i>Density: <b>{geoms_stats.at[clicked, "density"] if clicked else TOTAL_DENSITY:,}</b> pop./mi<sup>2</sup></i>
    <li><i>Per capita income: <b>${geoms_stats.at[clicked, "per_capita_income"] if clicked else PER_CAPITA_INCOME:,.0f} USD</b></i>
    </ul>
    """,
    unsafe_allow_html=True,
)

plot = plot_highlighted_choropleth(
    geoms,
    clicked,    
    "COUNTYFP",
    center={"lat": 40.73, "lon": -73.93},
    selected_color="#7c9dc0",
    customdata=["name", "population", "density", "per_capita_income"],
)
st.plotly_chart(plot, use_container_width=True)