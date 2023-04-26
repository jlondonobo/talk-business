import streamlit as st
from utils.pandas_exporter import init_connection, run_query


def fetch_nta_centroids(conn):
    query = """
    WITH name_mapper AS (
        SELECT DISTINCT NTA_NAME, NTA_CODE, COUNTY_FIPS
        FROM PERSONAL.PUBLIC.NTA_MAPPER
    ),
    centroids AS (
        SELECT COUNTY_FIPS, NTA_CODE, ST_CENTROID(to_geography(geometry)) as geom, NTA_NAME
        FROM PERSONAL.PUBLIC.NTA_GEOGRAPHY
        LEFT JOIN name_mapper USING(NTA_CODE)
    )

    SELECT COUNTY_FIPS, NTA_CODE, NTA_NAME, ST_Y(geom) AS LAT, ST_X(geom) AS LON
    FROM centroids;
    """
    return run_query(conn, query)


def main():
    conn = init_connection(**st.secrets["snowflake"])
    centroids = fetch_nta_centroids(conn)
    centroids.to_parquet("talk_business/local_data/nta_centroids.parquet")


if __name__ == "__main__":
    main()
