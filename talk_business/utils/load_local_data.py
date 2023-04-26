import pandas as pd
import streamlit as st


@st.cache_data()
def load_nta_centroids(county_fips: list[str]):
    data = pd.read_parquet("talk_business/local_data/nta_centroids.parquet")
    return data.query("COUNTY_FIPS in @county_fips")