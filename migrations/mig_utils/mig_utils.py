import pandas as pd
import snowflake.connector
from snowflake.connector import pandas_tools


def init_connection(**kwargs):
    return snowflake.connector.connect(
        **kwargs, client_session_keep_alive=True
    )


def export_data_to_snowflake(conn, data: pd.DataFrame, table_name: str):
    mapper = {"int64": "numeric", "object": "string", "float64": "numeric"}
    cols = {key: mapper[str(val)] for key, val in data.dtypes.to_dict().items()}
    parsed_cols = ", ".join([f"{key} {val}" for key, val in cols.items()])

    conn.cursor().execute("CREATE DATABASE IF NOT EXISTS PERSONAL")
    conn.cursor().execute("USE DATABASE PERSONAL")
    conn.cursor().execute("CREATE SCHEMA IF NOT EXISTS PUBLIC")
    conn.cursor().execute(
        "CREATE OR REPLACE TABLE "
        f"{table_name}({parsed_cols})"
    )
    pandas_tools.write_pandas(
        conn, data, table_name, database="PERSONAL", schema="PUBLIC"
    )
