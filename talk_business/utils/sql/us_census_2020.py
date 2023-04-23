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


def get_total_population(
    county: list[str],
) -> gpd.GeoDataFrame:
    """Get the total population and population density for each county."""

    query = """
    SELECT 
        census_block_group,
        county,
        COUNTY_FIPS,
        TRACT_CODE,
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
    variant: Union[str, None] = None,
    agg_type: Literal["TOTAL", "PERCENTAGE"] = "TOTAL",
) -> gpd.GeoDataFrame:
    meta = COLUMNS[column]
    table = meta["table"]

    if meta["type"] == "METRIC":
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
    LEFT JOIN PERSONAL.PUBLIC.NTA_MAPPER AS nta ON nta.CENSUS_TRACT_2020=c.tract_code AND nta.COUNTY_FIPS=c.COUNTY_FIPS
    WHERE census_block_group IN (
        SELECT census_block_group
        FROM OPENCENSUSDATA.PUBLIC."2020_CBG_GEOMETRY_WKT"
        WHERE state = 'NY' AND county IN (%(county)s)
    ) AND "{table}001e1" > 10;
    """
    df = run_query(query, params={"county": encode_list(county)})
    return to_gdf(df)


def get_statistics(county: list[str]) -> pd.DataFrame:
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
        WHERE state = 'NY' AND county IN (%(county)s)
    );
    """
    df = run_query(query, params={"county": encode_list(county)})
    return df


def get_bounding_box_points(county: list[str]) -> tuple[float, Polygon]:
    query = """
    WITH geoms AS (
        SELECT st_collect(to_geography(geometry)) as g
        FROM OPENCENSUSDATA.PUBLIC."2020_CBG_GEOMETRY_WKT"
        WHERE state = 'NY' AND county IN (%(county)s)
    )

    SELECT st_xmin(g) as xmin, st_xmax(g) as xmax, st_ymin(g) as ymin, st_ymax(g) as ymax
    FROM geoms;
    """

    df = run_query(query, params={"county": encode_list(county)})
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
