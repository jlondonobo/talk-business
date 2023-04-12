from typing import Union

import geopandas as gpd
import pandas as pd
import snowflake.connector
import streamlit as st


# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )


conn = init_connection()


# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query, params=None):
    with conn.cursor() as cur:
        cur.execute(query, params)
        return cur.fetch_pandas_all()


def encode_list(param_list: list[str]) -> Union[str, tuple[str]]:
    """Sanitize a list of parameters for SQL injection."""
    num_params = len(param_list)
    if num_params > 1:
        return tuple(param_list)
    elif num_params == 1:
        return param_list[0]
    else:
        return ""


def to_gdf(df: pd.DataFrame) -> gpd.GeoDataFrame:
    """Convert a pandas dataframe to a geopandas dataframe."""
    df = df.rename(columns={"GEOMETRY": "geometry"})
    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.GeoSeries.from_wkt(df["geometry"]),
        crs="EPSG:4326",
    )
    return gdf


def get_total_population(
    county: list[str],
) -> gpd.GeoDataFrame:
    """Get the total population and population density for each county."""

    query = """
    SELECT 
        census_block_group,
        "B01001e1" AS total_population,
        "B01001e1" / (amount_land * 3.8610215854781257e-7) AS density_pop_sqmile,
        geometry
    FROM OPENCENSUSDATA.PUBLIC."2020_CBG_B01"
    LEFT JOIN OPENCENSUSDATA.PUBLIC."2020_CBG_GEOMETRY_WKT" USING (census_block_group)
    LEFT JOIN OPENCENSUSDATA.PUBLIC."2020_METADATA_CBG_GEOGRAPHIC_DATA" USING (census_block_group)
    WHERE census_block_group IN (
        SELECT census_block_group
        FROM OPENCENSUSDATA.PUBLIC."2020_CBG_GEOMETRY_WKT"
        WHERE state = 'NY' AND county IN (%(county)s)
    ) AND total_population > 10;
    """

    df = run_query(query, params={"county": encode_list(county)})
    return to_gdf(df)


def get_simple_column(
    county: list[str],
    column: str,
    varname: str = "VALUE",
) -> gpd.GeoDataFrame:
    query = f"""SELECT
        census_block_group,
        "{column}" as {varname},
        geometry
    FROM OPENCENSUSDATA.PUBLIC."2020_CBG_B01"
    LEFT JOIN OPENCENSUSDATA.PUBLIC."2020_CBG_GEOMETRY_WKT" USING (census_block_group)
    LEFT JOIN OPENCENSUSDATA.PUBLIC."2020_METADATA_CBG_GEOGRAPHIC_DATA" USING (census_block_group)
    WHERE census_block_group IN (
        SELECT census_block_group
        FROM OPENCENSUSDATA.PUBLIC."2020_CBG_GEOMETRY_WKT"
        WHERE state = 'NY' AND county IN (%(county)s)
    ) AND "B01001e1" > 10;
    """
    df = run_query(query, params={"county": encode_list(county)})
    return to_gdf(df)
