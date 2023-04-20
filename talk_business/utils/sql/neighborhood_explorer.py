import pandas as pd
from utils.sql import runner


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
