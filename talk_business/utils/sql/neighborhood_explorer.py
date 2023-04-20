import geopandas as gpd
import pandas as pd
from utils.sql import runner
from utils.transformers import geo


def get_distribution(table: str, nta: str) -> pd.DataFrame:
    query = f"""
    SELECT *
    FROM PERSONAL.PUBLIC.{table}
    WHERE NTACODE = %(nta)s
    """
    distribution = runner.run_query(query.format(table=table), params={"nta": nta})
    long_distribution = (
        distribution
        .melt(id_vars=["COUNTY", "NTACODE"], var_name=table, value_name="population")
        .filter([table, "population"])
    )
    return long_distribution


def get_nta_list(county: str) -> pd.DataFrame:
    query = """
    SELECT NTACODE, NTANAME
    FROM PERSONAL.PUBLIC.NTA_MAPPER
    WHERE COUNTYFIPS = %(county)s
    GROUP BY (NTACODE, NTANAME);
    """
    return runner.run_query(query, params={"county": county})


def get_ntas_by_county(county: str) -> gpd.GeoDataFrame:
    query = """
    SELECT NTA2020, GEOMETRY
    FROM PERSONAL.PUBLIC.NTA_GEOGRAPHY
    WHERE COUNTYFIPS = %(county)s;
    """
    data = runner.run_query(query, params={"county": county})
    return geo.to_gdf(data)


def get_nta_shape(nta: str) -> gpd.GeoDataFrame:
    query = """
    SELECT NTA2020, GEOMETRY
    FROM PERSONAL.PUBLIC.NTA_GEOGRAPHY
    WHERE NTA2020 = %(nta)s;
    """
    data = runner.run_query(query, params={"nta": nta})
    return geo.to_gdf(data)
