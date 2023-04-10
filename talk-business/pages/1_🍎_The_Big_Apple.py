import snowflake.connector
import streamlit as st


# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )


conn = init_connection()


# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


rows = run_query(
    """
    SELECT DISTINCT county
    FROM "2019_CBG_GEOMETRY_WKT"
    WHERE state = 'NY';
    """
)


# Print results.
print("NYC Counties:")
for row in rows:
    st.write(row[0])
