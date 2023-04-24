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
    long_distribution = (
        distribution
        .melt(id_vars=["COUNTY_FIPS", "COUNTY", "NTA_CODE"], var_name=table, value_name="population")
        .filter([table, "population"])
    )
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
    distribution = runner.run_query(query.format(table=table), params={"county_fips": county_fips})
    long_distribution = (
        distribution
        .melt(id_vars=["COUNTY_FIPS", "COUNTY", "NTA_CODE"], var_name=table, value_name="population")
        .groupby(table, as_index=False)["population"].sum()
    )
    return long_distribution


def get_nta_list(county: str) -> pd.DataFrame:
    query = """
    SELECT NTA_CODE, NTA_NAME
    FROM PERSONAL.PUBLIC.NTA_MAPPER
    WHERE COUNTY_FIPS = %(county)s
    GROUP BY (NTA_CODE, NTA_NAME);
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
