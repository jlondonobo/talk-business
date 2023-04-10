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
