import pandas as pd
from utils.sql import runner


def get_distribution(table: str, nta: str) -> pd.DataFrame:
    query = f"""
    SELECT *
    FROM PERSONAL.PUBLIC.{table}
    WHERE NTANAME = %(nta)s
    """
    distribution = runner.run_query(query.format(table=table), params={"nta": nta})
    long_distribution = (
        distribution
        .melt(id_vars=["COUNTY", "NTANAME"], var_name=table, value_name="population")
        .filter([table, "population"])
    )
    return long_distribution


def get_nta_list() -> pd.DataFrame:
    query = """
    SELECT COUNTYFIPS, NTANAME
    FROM PERSONAL.PUBLIC.NTA_MAPPER
    GROUP BY (COUNTYFIPS, NTANAME);
    """
    return runner.run_query(query)
