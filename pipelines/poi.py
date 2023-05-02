import geopandas as gpd
import pandas as pd
import streamlit as st
from utils.pandas_exporter import export_data_to_snowflake, init_connection, run_query


def load_pois(conn) -> pd.DataFrame:
    """
    Queries points of interest from Snowflake.
    """
    query = """
        SELECT 
            NAME,
            LATITUDE,
            LONGITUDE,
            GET(GET(FSQ_CATEGORY_LABELS, 0), 0) as category,
            GET(GET(FSQ_CATEGORY_LABELS, 0), 1) as sub_category
        FROM FOURSQUARE_PLACES__NEW_YORK_CITY_SAMPLE.STANDARD.PLACES_US_NYC_STANDARD_SCHEMA
    """
    return run_query(conn, query)


def load_census_blocks(conn) -> pd.DataFrame:
    """
    Queries census blocks from Snowflake.
    """
    query = """
    SELECT COUNTY_FIPS, TRACT_CODE, CENSUS_BLOCK_GROUP, geometry
    FROM OPENCENSUSDATA.PUBLIC."2020_CBG_GEOMETRY_WKT"
    WHERE STATE_FIPS = '36' AND COUNTY_FIPS IN ('061', '047', '081', '005', '085') 
    """
    return run_query(conn, query)


# Transformations
def strip_quotations(pois: pd.DataFrame) -> pd.DataFrame:
    """
    Returns pois without quotation marks in CATEGORY.
    """
    return (
        pois
        .assign(
           CATEGORY=lambda df: df["CATEGORY"].str.replace('"', ''),
           SUB_CATEGORY=lambda df: df["SUB_CATEGORY"].str.replace('"', ''),
        )
    )


def pois_to_geo(pois: pd.DataFrame) -> gpd.GeoDataFrame:
    """
    Returns a GeoDataFrame with geometries from lat lon.
    """
    return (
        pois
        .assign(geometry=lambda df: gpd.points_from_xy(df.LONGITUDE, df.LATITUDE))
        .pipe(gpd.GeoDataFrame, crs="EPSG:4326")
    )


def blocks_to_geo(blocks: pd.DataFrame) -> gpd.GeoDataFrame:
    """
    Returns a GeoDataFrame with geometries from lat lon.
    """
    return (
        blocks
        .rename(columns={"GEOMETRY": "geometry"})
        .assign(geometry=lambda df: gpd.GeoSeries.from_wkt(df.geometry))
        .pipe(gpd.GeoDataFrame, crs="EPSG:4326")
    )


def add_census_block_to_pois(
    pois: gpd.GeoDataFrame,
    blocks: gpd.GeoDataFrame,
) -> pd.DataFrame:
    """
    Adds census block to each POI through a spatial join.
    """
    return pois.sjoin(blocks, how="left").drop(columns=["index_right", "geometry"])


def main():
    conn = init_connection(**st.secrets["snowflake"])

    pois = load_pois(conn)
    blocks = load_census_blocks(conn)

    clean_pois = strip_quotations(pois)

    geo_pois = pois_to_geo(clean_pois)
    geo_blocks = blocks_to_geo(blocks)

    geo_pois_with_blocks = (
        add_census_block_to_pois(geo_pois, geo_blocks)
        .dropna(subset=["CENSUS_BLOCK_GROUP"])
    )
    export_data_to_snowflake(conn, geo_pois_with_blocks, "POIS_WITH_BLOCKS")


if __name__ == "__main__":
    main()