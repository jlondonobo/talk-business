import io
import shutil
from zipfile import ZipFile

import geopandas as gpd
import requests
import streamlit as st
from utils.pandas_exporter import export_data_to_snowflake, init_connection


def load_geoms():
    """Geometries for NTAs in NYC."""
    NTA_GEOM_URL = "https://s-media.nyc.gov/agencies/dcp/assets/files/zip/data-tools/bytes/nynta2020_23a.zip"
    r = requests.get(NTA_GEOM_URL)
    with ZipFile(io.BytesIO(r.content)) as f:
        f.extractall(".shapes")
    gdf = gpd.read_file(".shapes/nynta2020_23a/nynta2020.shp")
    shutil.rmtree(".shapes")
    return gdf


def main():
    geoms = load_geoms()
    geoms = geoms.filter(["NTA2020", "geometry"])
    geoms = geoms.to_wkt().rename(lambda x: x.upper(), axis=1)

    conn = init_connection(**st.secrets["snowflake"])
    export_data_to_snowflake(conn, geoms, "NTA_GEOGRAPHY")


if __name__ == "__main__":
    main()