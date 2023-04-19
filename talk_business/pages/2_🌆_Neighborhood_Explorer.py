import plotly.express as px
import streamlit as st

# Read the data
# Plot the data
# Include plot in layout

st.set_page_config(
    page_title="🌆 Neighborhood Explorer",
    layout="wide",
)
from utils.sql import neighborhood_explorer as ne

st.markdown("# 🌆 Negihborhood Explorer")


nta_list = ne.get_nta_list()

county = st.radio("County", nta_list["COUNTYFIPS"].unique(), 0, horizontal=True)

ntas = nta_list.query("COUNTYFIPS == @county")["NTANAME"].unique()

nta = st.selectbox("Negihborhood", ntas, 0)

# AGE_GROUPS
AGE_CATEGORY = {
    "00-05": "Children",
    "05-10": "Children",
    "10-14": "Adolescents",
    "15-19": "Adolescents",
    "20-24": "Young Adults",
    "25-29": "Young Adults",
    "30-34": "Adults",
    "35-39": "Adults",
    "40-44": "Adults",
    "45-49": "Adults",
    "50-54": "Adults",
    "55-59": "Adults",
    "60-64": "Older adults",
    "65-69": "Older adults",
    "70-74": "Older adults",
    "75-79": "Older adults",
    "80-84": "Older adults",
    "85-100": "Older adults",
}


age_groups = ne.get_distribution("AGE_GROUPS", nta).assign(age_category=lambda df: df["AGE_GROUPS"].map(AGE_CATEGORY))
age_histogram = px.bar(age_groups, x="AGE_GROUPS", y="population", color="age_category", text_auto=",.0f")
age_histogram.update_layout(xaxis_type="category")
st.plotly_chart(age_histogram, use_container_width=True)
