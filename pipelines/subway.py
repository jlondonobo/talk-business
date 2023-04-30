import re
from typing import Union

import geopandas as gpd
import pandas as pd
import streamlit as st
from thefuzz import process
from utils.pandas_exporter import export_data_to_snowflake, init_connection, run_query

LOCATIONS_URL = "https://data.ny.gov/api/views/i9wp-a4ja/rows.csv?accessType=DOWNLOAD&sorting=true"
ROUTES = [
    'route1',
    'route2',
    'route3',
    'route4',
    'route5',
    'route6',
    'route7',
    'route8',
    'route9',
    'route10',
    'route11'
]


RIDERSHIP_URL = "https://new.mta.info/document/91476"
NUMBER_SUFFIXES = {1: "st", 2: "nd", 3: "rd"}


def load_ridership():
    """Loads average weekday ridership by station."""
    return pd.read_excel(RIDERSHIP_URL, sheet_name="Avg Weekday", skiprows=1)


def clean_names(col: str) -> str:
    """Utility to clean column names."""
    return col.lower().replace(" ", "_")


def routes_to_list(stations: pd.DataFrame) -> pd.Series:
    """Converts routes to list of routes."""
    return stations[ROUTES].apply(lambda x: set([v for v in x if str(v) != "nan"]), axis=1)


def load_subway_stations() -> pd.DataFrame:
    """Loads subway station entrances."""
    return pd.read_csv(LOCATIONS_URL)


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
            routes=lambda x: routes_to_list(x),
            geometry=lambda x: gpd.points_from_xy(x["station_longitude"], x["station_latitude"])
        )
        .reset_index(drop=True)
        .filter(["station_name", "routes", "geometry", "station_latitude", "station_longitude"])
        .pipe(gpd.GeoDataFrame, crs="EPSG:4326")
    )


def preprocess_station_name(name: str) -> str:
    """Preprocess staiton names."""
    clean_name = re.sub(r"\(.*\)", "", name).replace("St.", "St")

    # st_num = re.findall(r"(\d+)", clean_name)
    # if st_num:
    #     for num in st_num:
    #         last_num = int(num[-1])
    #         suffix = NUMBER_SUFFIXES.get(last_num, "th")
    #         clean_name = clean_name.replace(num, f"{num}{suffix}")
    return clean_name


def transform_ridership(ridership: pd.DataFrame) -> pd.DataFrame:
    """Preprocesses ridership data."""
    return (
        ridership
        .dropna(subset="Boro")
        .rename(columns={"Station (alphabetical by borough)": "station_name", 2019: "ridership"})
        .filter(["station_name", "ridership"])
        # .assign(station_name=lambda x: x["station_name"].apply(preprocess_station_name))
        .groupby("station_name")
        ["ridership"]
        .sum()
        .reset_index()
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
    return original.apply(lambda x: fuzzy_match(x, canonical, 90))


def add_station_name_match(
    ridership: pd.DataFrame,
    station_names: pd.Series
) -> pd.Series:
    """Adds station match to ridership for merger with locations."""
    station_names_simple = station_names.str.replace(r'(\d+)(st|nd|rd|th)', r"\1", regex=True)
    return (
        ridership
        .assign(
            station_name_match=lambda df: fuzzy_match_series_station_names(df["station_name"], station_names_simple)
        )
    )


def main():
    conn = init_connection(**st.secrets["snowflake"])

    stations = load_subway_stations()
    unique_stations = transform_subway_stations(stations)

    ridership = load_ridership()
    t_ridership = transform_ridership(ridership)
    matched_ridership = add_station_name_match(t_ridership, unique_stations["station_name"])
    matched_ridership.to_clipboard(index=False)


    ntas = load_nta_geoms(conn)
    ntas = transform_ntas(ntas)
    complete_stations = attach_nta_code(unique_stations, ntas)

    export_data_to_snowflake(conn, complete_stations, "SUBWAY_STATIONS")


if __name__ == "__main__":
    main()



MANUAL_MATCHES = {
    "111st St": "111th St",
}





