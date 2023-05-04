from typing import Literal, Union

import geopandas as gpd
import pandas as pd
from pyproj import Geod
from shapely import Polygon
from shapely.geometry import box
from utils.columns import COLUMNS
from utils.sql.encoders import encode_list
from utils.sql.runner import run_query
from utils.transformers.geo import to_gdf


def get_simple_column(
    county_fips: list[str],
    column: str,
    variant: Union[str, None] = None,
    agg_type: Literal["TOTAL", "PERCENTAGE"] = "TOTAL",
) -> gpd.GeoDataFrame:
    meta = COLUMNS[column]
    table = meta["table"]

    if meta["type"] in ["METRIC", "COUNT_METRIC"]:
        column_selector = f"""
        "{meta["code"]}" as "{column}",
        "{meta["total"]}" as TOTAL
        """
    else:
        if agg_type == "TOTAL":
            column_selector = f"""
            "{meta["segments"][variant]}" as "{column}-{variant}",
            "{meta["total"]}" as TOTAL
            """

        elif agg_type == "PERCENTAGE":
            column_selector = f"""
            "{meta["segments"][variant]}" / "{meta["total"]}" as "{column}-{variant}",
            "{meta["total"]}" as TOTAL
        """

    add_population = " "
    if column == "PER_CAPITA_INCOME":
        add_population = """LEFT JOIN OPENCENSUSDATA.PUBLIC."2020_CBG_B01" USING (census_block_group)"""
    query = f"""SELECT
        census_block_group,
        county,
        c.COUNTY_FIPS,
        TRACT_CODE,
        {column_selector},
        NTA_NAME,
        geometry
    FROM OPENCENSUSDATA.PUBLIC."2020_CBG_{table}"
    LEFT JOIN OPENCENSUSDATA.PUBLIC."2020_CBG_GEOMETRY_WKT" AS c USING (census_block_group)
    {add_population}
    LEFT JOIN PERSONAL.PUBLIC.NTA_MAPPER AS nta ON nta.CENSUS_TRACT_2020=c.tract_code AND nta.COUNTY_FIPS=c.COUNTY_FIPS AND nta.STATE_FIPS=c.STATE_FIPS
    WHERE census_block_group IN (
        SELECT census_block_group
        FROM OPENCENSUSDATA.PUBLIC."2020_CBG_GEOMETRY_WKT"
        WHERE state = 'NY' AND COUNTY_FIPS IN (%(county_fips)s)
    ) AND "{table}001e1" > 10;
    """
    df = run_query(query, params={"county_fips": encode_list(county_fips)})
    return to_gdf(df)


def get_statistics(county_fips: list[str]) -> pd.DataFrame:
    """
    Returns four summary statistics for the selected counties.

    The statistics are:
    - Total population
    - Age weighted average
    - Percentage of female population
    - Per-capita income weighted average
    """
    query = """
    SELECT
        SUM("B01003e1") AS TOTAL_POP,
        SUM("B01002e1" * "B01003e1") / SUM("B01003e1") AS WEIGHTED_AVG_AGE,
        SUM("B01001e26") / SUM("B01001e1") AS FEMALE_PERCENT,
        SUM("B19301e1" * "B01003e1") / SUM("B01003e1") AS WEIGHTED_AVG_PER_CAPITA_INCOME
    FROM OPENCENSUSDATA.PUBLIC."2020_CBG_B01"
    LEFT JOIN OPENCENSUSDATA.PUBLIC."2020_CBG_B19" USING (census_block_group)
    WHERE census_block_group IN (
        SELECT census_block_group
        FROM OPENCENSUSDATA.PUBLIC."2020_CBG_GEOMETRY_WKT"
        WHERE state = 'NY' AND COUNTY_FIPS IN (%(county_fips)s)
    );
    """
    df = run_query(query, params={"county_fips": encode_list(county_fips)})
    return df


def get_bounding_box_points(county_fips: list[str]) -> tuple[float, Polygon]:
    query = """
    WITH geoms AS (
        SELECT st_collect(to_geography(geometry)) as g
        FROM OPENCENSUSDATA.PUBLIC."2020_CBG_GEOMETRY_WKT"
        WHERE state = 'NY' AND COUNTY_FIPS IN (%(county_fips)s)
    )

    SELECT st_xmin(g) as xmin, st_xmax(g) as xmax, st_ymin(g) as ymin, st_ymax(g) as ymax
    FROM geoms;
    """

    df = run_query(query, params={"county_fips": encode_list(county_fips)})
    xmin = df["XMIN"].values[0]
    xmax = df["XMAX"].values[0]
    ymin = df["YMIN"].values[0]
    ymax = df["YMAX"].values[0]
    envelope = box(xmin, ymin, xmax, ymax)

    geod = Geod(ellps="WGS84")
    area = abs(geod.geometry_area_perimeter(envelope)[0])
    return area, envelope.centroid


# Not going to be used yet.
COUNT_VARIABLES = """
    SELECT 
        TRACT_CODE,
        SUM("B01001e1") as variable,
        ST_COLLECT( as GEOMETRY)
    FROM OPENCENSUSDATA.PUBLIC."2020_CBG_B01"
    LEFT JOIN OPENCENSUSDATA.PUBLIC."2020_CBG_GEOMETRY_WKT" USING (census_block_group)
    WHERE census_block_group IN (
        SELECT census_block_group
        FROM OPENCENSUSDATA.PUBLIC."2020_CBG_GEOMETRY_WKT"
        WHERE state = 'NY' AND county IN ('New York County')
    ) AND "B01001e1" > 10
    GROUP BY TRACT_CODE;
"""


def get_nta_shapes(county_fips_collection: list[str]) -> gpd.GeoSeries:
    """
    Returns a GeoDataFrame containing the NTA polygons for the given counties.
    """
    query = """
    SELECT GEOMETRY
    FROM PERSONAL.PUBLIC.NTA_GEOGRAPHY
    WHERE COUNTY_FIPS IN (%(county_fips_collection)s);
    """
    df = run_query(
        query,
        params={"county_fips_collection": encode_list(county_fips_collection)}
    )
    return gpd.GeoSeries.from_wkt(df["GEOMETRY"], crs="EPSG:4326")


def get_subway_stations(county_fips_collection: list[str]):
    """Returns subway stations coordinates."""
    query = """
    SELECT *
    FROM PERSONAL.PUBLIC.SUBWAY_STATIONS
    WHERE "county_fips" IN (%(county_fips_collection)s);
    """
    return run_query(query, params={"county_fips_collection": encode_list(county_fips_collection)})


def get_parks(county_fips_collection: list[str]) -> gpd.GeoDataFrame:
    """
    Returns park polygons for specific county.
    """
    query = """
    SELECT *
    FROM PERSONAL.PUBLIC.PUBLIC_PARKS
    WHERE "COUNTY_FIPS" IN (%(county_fips_collection)s);
    """
    data = run_query(query, params={"county_fips_collection": encode_list(county_fips_collection)})
    return (
        data
        .assign(geometry=lambda df: gpd.GeoSeries.from_wkt(df["geometry"], crs="EPSG:4326"))
        .pipe(gpd.GeoDataFrame)
    )


def get_poi_count(
    county_fips: list[str],
    category: Union[str, None] = None,
) -> gpd.GeoDataFrame:
    query = """
    WITH pois AS (
        SELECT
            COUNTY_FIPS,
            TRACT_CODE,
            CENSUS_BLOCK_GROUP,
            CATEGORY,
            COUNT(*) as count,
            SUM(COUNT(*)) OVER(PARTITION BY COUNTY_FIPS, TRACT_CODE, CENSUS_BLOCK_GROUP) as total_count
        FROM PERSONAL.PUBLIC.POIS_WITH_BLOCKS
        GROUP BY (COUNTY_FIPS, TRACT_CODE, CENSUS_BLOCK_GROUP, CATEGORY)
    )
    SELECT
        pois.COUNTY_FIPS,
        pois.TRACT_CODE,
        pois.CENSUS_BLOCK_GROUP,
        CATEGORY,
        NTA_CODE,
        count,
        total_count,
        geometry
    FROM pois
    LEFT JOIN OPENCENSUSDATA.PUBLIC."2020_CBG_GEOMETRY_WKT" USING (CENSUS_BLOCK_GROUP)
    LEFT JOIN PERSONAL.PUBLIC.NTA_MAPPER as nta ON pois.COUNTY_FIPS=nta.county_fips AND pois.TRACT_CODE=nta.census_tract_2020
    WHERE CATEGORY=%(category)s AND pois.COUNTY_FIPS IN (%(county_fips)s);
    """
    params = {
        "category": category,
        "county_fips": encode_list(county_fips),
    }

    df = run_query(query, params=params)
    return (
        df
        .rename(columns={"GEOMETRY": "geometry"})
        .assign(
            geometry=lambda df: gpd.GeoSeries.from_wkt(df["geometry"], crs="EPSG:4326"),
        )
        .pipe(gpd.GeoDataFrame)
    )


def get_main_stats() -> pd.DataFrame:
    query = """
    WITH census_stats AS (
        SELECT 
            COUNTY_FIPS, 
            SUM("B01003e1") TOTAL_POPULATION,
            SUM("B25054e1") AS TOTAL_HOUSEHOLDS,
            SUM("B19313e1") AS TOTAL_INCOME
        FROM OPENCENSUSDATA.PUBLIC."2020_CBG_B01"
        LEFT JOIN OPENCENSUSDATA.PUBLIC."2020_CBG_B19" USING (CENSUS_BLOCK_GROUP)
        LEFT JOIN OPENCENSUSDATA.PUBLIC."2020_CBG_B25" USING (CENSUS_BLOCK_GROUP)
        LEFT JOIN OPENCENSUSDATA.PUBLIC."2020_CBG_GEOMETRY_WKT" as c USING(CENSUS_BLOCK_GROUP)
        WHERE STATE_FIPS = '36' AND COUNTY_FIPS IN ('061', '047', '081', '005', '085')
        GROUP BY COUNTY_FIPS
    ), places_stats AS (
        SELECT 
            COUNTY_FIPS,
            COUNT(*) as TOTAL_PLACES
        FROM PERSONAL.PUBLIC.POIS_WITH_BLOCKS
        WHERE COUNTY_FIPS IN ('061', '047', '081', '005', '085')
        GROUP BY COUNTY_FIPS
    )
    SELECT *
    FROM census_stats
    LEFT JOIN places_stats USING(COUNTY_FIPS);
    """
    return run_query(query).set_index("COUNTY_FIPS")
