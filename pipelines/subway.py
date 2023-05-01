from typing import Union

import geopandas as gpd
import pandas as pd
import streamlit as st
from thefuzz import process
from utils.pandas_exporter import export_data_to_snowflake, init_connection, run_query


def load_subway_stations() -> pd.DataFrame:
    """Loads subway station entrances."""
    data = pd.read_csv("https://data.cityofnewyork.us/api/views/kk4q-3rt2/rows.csv?accessType=DOWNLOAD")
    data = data.assign(
        geometry=lambda x: gpd.GeoSeries.from_wkt(x["the_geom"], crs="EPSG:4326"),
        station_name=lambda x: x["NAME"].str.replace(r'(\d+)(st|nd|rd|th)', r"\1", regex=True),
        lines=lambda x: x["LINE"].str.replace(r"-. Express", "", regex=True),
    )
    data = data.drop(columns=["the_geom"])
    return (
        gpd.GeoDataFrame(data)
        .assign(
             station_latitude=lambda x: x["geometry"].y,
            station_longitude=lambda x: x["geometry"].x,
        )
    )


def load_ridership():
    """Loads average weekday ridership by station."""
    data = pd.read_excel("https://new.mta.info/document/91476", sheet_name="Avg Weekday", skiprows=1)
    return (
        data
        .dropna(subset="Boro")
        .rename(columns={"Station (alphabetical by borough)": "station_name", 2019: "ridership"})
        .filter(["station_name", "ridership"])
        .assign(lines=lambda x: x["station_name"].str.extract(r"\((.+?)\)")[0].str.split(",").apply(lambda y: "-".join(sorted(y))))
    )


def clean_names(col: str) -> str:
    """Utility to clean column names."""
    return col.lower().replace(" ", "_")


def load_nta_geoms(conn) -> gpd.GeoDataFrame:
    """Loads NTA geometries."""
    query = "SELECT * FROM PERSONAL.PUBLIC.NTA_GEOGRAPHY"
    return run_query(conn, query)


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


def fuzzy_match(val: str, options: pd.Series, threshold: int = 90) -> Union[str, None]:
    """Returns fuzzy match of val from options."""
    res = process.extractOne(val, options, score_cutoff=threshold)
    if res is not None:
        return res[0]


def fuzzy_match_series_station_names(
    original: pd.Series,
    canonical: pd.Series
) -> pd.Series:
    """
    Returns fuzzy match of original from canonical.
    """
    return original.apply(lambda x: fuzzy_match(x, canonical, 80))


def main():
    conn = init_connection(**st.secrets["snowflake"])

    stations = load_subway_stations()
    ridership = load_ridership()
    
    canonical_ridership = (
        ridership
        .assign(
            clean_name=lambda x: x["station_name"].str.replace(r"\(.*\)", "", regex=True).str.replace("St.", "St", regex=False),
            station_match=lambda x: fuzzy_match_series_station_names(x["clean_name"], stations["station_name"]),
        )
        .filter(["station_match", "lines", "ridership"])
    )

    stations_with_ridership = (
        stations
        .merge(
            canonical_ridership,
            how="left",
            left_on=["station_name", "lines"],
            right_on=["station_match", "lines"],
        )
    )

    ntas = load_nta_geoms(conn)
    ntas = transform_ntas(ntas)
    complete_stations = attach_nta_code(stations_with_ridership, ntas)
    complete_stations = (
        complete_stations
        .filter(["lines", "station_name", "station_latitude", "station_longitude", "county_fips", "nta_code", "ridership"])
    )
    export_data_to_snowflake(conn, complete_stations, "SUBWAY_STATIONS")


if __name__ == "__main__":
    main()

