import pandas as pd
import streamlit as st
from mig_utils.mig_utils import export_data_to_snowflake, init_connection


def load_mapper():
    """Maps Cenus Tract codes to Neighborhood Tabulation Areas (NTAs)."""
    MAPPER_URL = "https://www.nyc.gov/assets/planning/download/office/planning-level/nyc-population/census2020/nyc2020census_tract_nta_cdta_relationships.xlsx?r=092221"
    return pd.read_excel(
        MAPPER_URL,
        usecols=["CountyFIPS", "CT2020", "NTACode", "NTAName", "NTAAbbrev"],
        dtype={"CountyFIPS": str, "CT2020": str, "NTACode": str},
    )


def main():
    mapper = load_mapper()
    uppercase_mapper = mapper.rename(lambda x: x.upper(), axis="columns")
    conn = init_connection(**st.secrets["snowflake"])
    export_data_to_snowflake(conn, uppercase_mapper, "NTA_MAPPER")


if __name__ == "__main__":
    main()
