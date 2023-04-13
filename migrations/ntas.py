import io
from zipfile import ZipFile

import geopandas as gpd
import pandas as pd
import requests
import snowflake.connector
import streamlit as st
from snowflake.connector import pandas_tools

MAPPER_URL = "https://www.nyc.gov/assets/planning/download/office/planning-level/nyc-population/census2020/nyc2020census_tract_nta_cdta_relationships.xlsx?r=092221"
NTA_GEOM_URL = "https://s-media.nyc.gov/agencies/dcp/assets/files/zip/data-tools/bytes/nynta2020_23a.zip"


def load_mapper():
    return (
        pd.read_excel(MAPPER_URL, usecols=["GEOID", "NTACode", "NTAName", "NTAAbbrev"])
        .rename(lambda x: x.upper(), axis="columns")
    )


def load_geoms():
    r = requests.get(NTA_GEOM_URL)
    with ZipFile(io.BytesIO(r.content)) as f:
        f.extractall(".shapes")
    # TODO: Remove .migrations folder inside function
    return gpd.read_file(".shapes/nynta2020_23a/nynta2020.shp")


def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )


def export_data_to_snowflake(conn, data):
    conn.cursor().execute("CREATE DATABASE IF NOT EXISTS PERSONAL")
    conn.cursor().execute("USE DATABASE PERSONAL")
    conn.cursor().execute("CREATE SCHEMA IF NOT EXISTS PUBLIC")
    conn.cursor().execute(
        "CREATE OR REPLACE TABLE "
        "NTA_MAPPER(GEOID string, NTACODE string, NTANAME string, NTAABBREV string)"
    )
    pandas_tools.write_pandas(
        conn, data, "NTA_MAPPER", database="PERSONAL", schema="PUBLIC"
    )


# Might only need mapper:
# https://docs.carto.com/data-and-analysis/analytics-toolbox-for-snowflake/sql-reference/transformations#st_concavehull
def main():
    mapper = load_mapper()
    conn = init_connection()
    export_data_to_snowflake(conn, mapper)


if __name__ == "__main__":
    main()
