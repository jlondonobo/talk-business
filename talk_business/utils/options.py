from utils.columns import COLUMNS

COUNTIES = ["New York County", "Bronx County", "Kings County", "Queens County", "Richmond County"]
METRICS = {column: meta["label"] for column, meta in COLUMNS.items()}

ADD_METRICS = {"PLACES": "Places"}
METRICS.update(ADD_METRICS)