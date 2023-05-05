import streamlit as st
from st_click_detector import click_detector
from utils.names import get_county_name
from utils.utils import load_css

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
    
    As of 2022 the city had 2.3 million registered small businesses 👩‍💼 with 13% founded by hispanic entrepreneurs. Now it's your time to join.
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


