import pandas as pd
import streamlit as st
from utils.pandas_exporter import export_data_to_snowflake, init_connection

URL = "https://data.cityofnewyork.us/api/views/enfh-gkve/rows.csv?accessType=DOWNLOAD"
VALID_TYPES = [
    "Triangle/Plaza",
    "Garden",
    "Neighborhood Park",
    "Jointly Operated Playground",
    "Playground",
    "Community Park",
    "Nature Area",
    "Recreation Field/Courts",
    "Strip",
]
COLUMNS = ["BOROUGH", "GISOBJID", "ACRES", "TYPECATEGORY", "multipolygon"]
BOROUGH_MAPPER = {
    "B": "057",
    "Q": "081",
    "X": "005",
    "M": "061",
    "R": "085",
}


def load_parks() -> pd.DataFrame:
    """Loads parks."""
    return pd.read_csv(URL, usecols=COLUMNS)


def transform_parks(parks: pd.DataFrame):
    """Returns filtered parks"""
    return (
        parks
        .assign(COUNTY_FIPS=lambda df: df["BOROUGH"].map(BOROUGH_MAPPER))
        .rename(columns={"multipolygon": "geometry"})
        .query("TYPECATEGORY.isin(@VALID_TYPES)")
        .drop(columns=["BOROUGH"])
    )


def main():
    parks = load_parks()
    parks = transform_parks(parks)
    conn = init_connection(**st.secrets["snowflake"])
    export_data_to_snowflake(conn, parks, "PUBLIC_PARKS")


if __name__ == "__main__":
    main()
