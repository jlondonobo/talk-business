from typing import Union

import geopandas as gpd
import pandas as pd
from utils.sql import runner
from utils.transformers import geo


def get_distribution(table: str, nta: str) -> pd.DataFrame:
    query = f"""
    SELECT *
    FROM PERSONAL.PUBLIC.{table}
    WHERE NTA_CODE = %(nta)s
    """
    distribution = runner.run_query(query.format(table=table), params={"nta": nta})
    long_distribution = distribution.melt(
        id_vars=["COUNTY_FIPS", "COUNTY", "NTA_CODE"],
        var_name=table,
        value_name="population",
    ).filter([table, "population"])
    return long_distribution


def get_county_distribution(table: str, county_fips: str) -> pd.DataFrame:
    """
    Returns variable distribution for all NTAs in a county.
    """
    query = f"""
    SELECT *
    FROM PERSONAL.PUBLIC.{table}
    WHERE COUNTY_FIPS = %(county_fips)s
    """
    distribution = runner.run_query(
        query.format(table=table), params={"county_fips": county_fips}
    )
    long_distribution = (
        distribution.melt(
            id_vars=["COUNTY_FIPS", "COUNTY", "NTA_CODE"],
            var_name=table,
            value_name="population",
        )
        .groupby(table, as_index=False)["population"]
        .sum()
    )
    return long_distribution


def get_available_nta_list(county: str) -> pd.DataFrame:
    query = """
    SELECT NTA_CODE
    FROM PERSONAL.PUBLIC.NTA_MAPPER as nta
    LEFT JOIN OPENCENSUSDATA.PUBLIC."2020_CBG_GEOMETRY_WKT" AS c ON nta.CENSUS_TRACT_2020=c.tract_code AND nta.COUNTY_FIPS=c.COUNTY_FIPS AND nta.STATE_FIPS=c.STATE_FIPS  
    LEFT JOIN OPENCENSUSDATA.PUBLIC."2020_CBG_B01" USING (census_block_group)
    WHERE c.COUNTY_FIPS = %(county)s
    GROUP BY (NTA_CODE, NTA_NAME)
    HAVING SUM("B01001e1") > 100
    ORDER BY NTA_NAME;
    """
    return runner.run_query(query, params={"county": county})


def get_nta_geoms() -> gpd.GeoDataFrame:
    query = """
    SELECT NTA_CODE, GEOMETRY
    FROM PERSONAL.PUBLIC.NTA_GEOGRAPHY;
    """
    data = runner.run_query(query)
    return geo.to_gdf(data)


def get_nta_shape(nta: str) -> gpd.GeoDataFrame:
    query = """
    SELECT NTA_CODE, GEOMETRY
    FROM PERSONAL.PUBLIC.NTA_GEOGRAPHY
    WHERE NTA_CODE = %(nta)s;
    """
    data = runner.run_query(query, params={"nta": nta})
    return geo.to_gdf(data)


def fetch_neighborhood_statistics():
    """Return neighborhood statistics for all neighborhoods."""
    query = """
    SELECT 
        NTA_CODE,
        SUM("B01001e1") POPULATION, 
        SUM("B19313e1") AS TOTAL_INCOME,
        SUM("B25064e1" * "B25054e1") / SUM("B25054e1") AS AVG_RENT
    FROM OPENCENSUSDATA.PUBLIC."2020_CBG_B01" AS
    LEFT JOIN OPENCENSUSDATA.PUBLIC."2020_CBG_B19" USING(census_block_group)
    LEFT JOIN OPENCENSUSDATA.PUBLIC."2020_CBG_B25" USING(census_block_group)
    LEFT JOIN OPENCENSUSDATA.PUBLIC."2020_CBG_GEOMETRY_WKT" AS c USING(census_block_group)
    LEFT JOIN PERSONAL.PUBLIC.NTA_MAPPER AS nta ON nta.CENSUS_TRACT_2020=c.tract_code AND nta.COUNTY_FIPS=c.COUNTY_FIPS AND nta.STATE_FIPS=c.STATE_FIPS
    GROUP BY NTA_CODE;
    """
    data = runner.run_query(query)
    data = data.set_index("NTA_CODE")
    return data


def fetch_county_geoms(county_fips: str) -> gpd.GeoDataFrame:
    """Return county geometries for a single county."""
    query = """
    SELECT COUNTY_FIPS, GEOMETRY
    FROM PERSONAL.PUBLIC.NTA_GEOGRAPHY
    WHERE COUNTY_FIPS = %(county_fips)s;
    """
    data = runner.run_query(query, params={"county_fips": county_fips})
    return geo.to_gdf(data)


def neighborhood_stat(
    data: pd.DataFrame,
    nta_code: str,
    stat: str,
) -> Union[int, float]:
    """Return neighborhood statistics for a single neighborhood."""
    return data.at[nta_code, stat]

