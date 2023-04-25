import geopandas as gpd
import pandas as pd
import streamlit as st
from utils.pandas_exporter import export_data_to_snowflake, init_connection, run_query

URL = (
    "https://data.ny.gov/api/views/i9wp-a4ja/rows.csv?accessType=DOWNLOAD&sorting=true"
)
COLS = [
    "Line",
    "Station Name",
    "Station Latitude",
    "Station Longitude",
]


def clean_names(col: str) -> str:
    """Utility to clean column names."""
    return col.lower().replace(" ", "_")


def load_subway_stations() -> pd.DataFrame:
    """Loads subway station entrances."""
    return pd.read_csv(URL, usecols=COLS)


def load_nta_geoms(conn) -> gpd.GeoDataFrame:
    """Loads NTA geometries."""
    query = "SELECT * FROM PERSONAL.PUBLIC.NTA_GEOGRAPHY"
    return run_query(conn, query)


def transform_subway_stations(data: pd.DataFrame) -> gpd.GeoDataFrame:
    """Get only one location per station."""
    return (
        data
        .rename(columns=clean_names)
        .drop_duplicates(
            subset=["station_name", "station_latitude", "station_longitude"]
        )
        .assign(
            geometry=lambda x: gpd.points_from_xy(x["station_longitude"], x["station_latitude"])
        )
        .pipe(gpd.GeoDataFrame, crs="EPSG:4326")
    )


def transform_ntas(ntas: pd.DataFrame) -> gpd.GeoDataFrame:
    """Returns NTA geometries ready to be joined to subway stations."""
    return (
        ntas
        .rename(columns=clean_names)
        .assign(geometry=lambda x: gpd.GeoSeries.from_wkt(x["geometry"]))
        .pipe(gpd.GeoDataFrame, crs="EPSG:4326")
    )


def attach_nta_code(
    stations: gpd.GeoDataFrame, nta_geoms: gpd.GeoDataFrame
) -> pd.DataFrame:
    return (
        stations
        .sjoin(nta_geoms, how="left")
        .drop(columns=["index_right", "geometry"])
    )


def main():
    conn = init_connection(**st.secrets["snowflake"])
    stations = load_subway_stations()
    unique_stations = transform_subway_stations(stations)

    ntas = load_nta_geoms(conn)
    ntas = transform_ntas(ntas)
    complete_stations = attach_nta_code(unique_stations, ntas)

    export_data_to_snowflake(conn, complete_stations, "SUBWAY_STATIONS")


if __name__ == "__main__":
    main()
