import pandas as pd
import streamlit as st
from utils.pandas_exporter import export_data_to_snowflake, init_connection


def load_mapper():
    """Maps Cenus Tract codes to Neighborhood Tabulation Areas (NTAs)."""
    MAPPER_URL = "https://www.nyc.gov/assets/planning/download/office/planning-level/nyc-population/census2020/nyc2020census_tract_nta_cdta_relationships.xlsx?r=092221"
    return pd.read_excel(
        MAPPER_URL,
        usecols=["CountyFIPS", "CT2020", "NTACode", "NTAName", "NTAAbbrev"],
        dtype={"CountyFIPS": str, "CT2020": str, "NTACode": str},
    )


def transform_mapper(mapper: pd.DataFrame) -> pd.DataFrame:
    return (
        mapper
        .assign(STATE_FIPS="36")
        .rename(
            {
                "CountyFIPS": "COUNTY_FIPS",
                "CT2020": "CENSUS_TRACT_2020",
                "NTACode": "NTA_CODE",
                "NTAName": "NTA_NAME",
                "NTAAbbrev": "NTA_ABBREV",
            },
            axis="columns"
        )
    )


def main():
    mapper = load_mapper()
    mapper = transform_mapper(mapper)
    conn = init_connection(**st.secrets["snowflake"])
    export_data_to_snowflake(conn, mapper, "NTA_MAPPER")


if __name__ == "__main__":
    main()
