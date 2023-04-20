from typing import Any

import pandas as pd
import streamlit as st
from constants.feature_groups import COUNT_GROUPS
from extract.nta_distribution import query_nta_feature_distribution, query_nta_statistic
from utils.pandas_exporter import export_data_to_snowflake, init_connection, run_query


def load_transformed(conn, feature_groups: dict[str, Any]) -> pd.DataFrame:
    """Queries Snowflake for already transformed data."""
    query = query_nta_feature_distribution(feature_groups)
    return run_query(conn, query)


def export_to_snowflake(conn, data: pd.DataFrame, table_name: str):
    """Loads data to Snowflake table."""
    export_data_to_snowflake(conn, data, table_name)


def main():
    # TODO: TRANSFORM is already done in Snowflake. Would like to do it here
    conn = init_connection(**st.secrets["snowflake"])
    for feature, meta in COUNT_GROUPS.items():
        df = load_transformed(conn, meta)
        export_to_snowflake(conn, df, feature)


if __name__ == "__main__":
    main()

# total_income = query_nta_statistic("TOTAL_INCOME")
# total_population = query_nta_statistic("TOTAL_POPULATION")
# school_enrollment = query_nta_statistic("ENROLLED_IN_SCHOOL")