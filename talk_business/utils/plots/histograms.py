import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.columns import COLUMNS

LABELS = {col: meta["full_label"] for col, meta in COLUMNS.items()}
LABELS.update({"COUNTY": "Borough"})

COUNTY_TO_BOROUGH = {
    "New York County": "Manhattan",
    "Kings County": "Brooklyn",
    "Queens County": "Queens",
    "Bronx County": "The Bronx",
    "Richmond County": "Staten Island",
}


def plot_distribution_by_area(
    data: pd.DataFrame,
    column: str,
    area: str = "COUNTY",
) -> go.Figure:
    """
    A histogram to compare single variables in each area.
    """
    data = (
        data
        .assign(
            **{area: lambda df: df[area].map(COUNTY_TO_BOROUGH)},
        )
    )

    fig = px.histogram(
        data,
        x=column,
        color=area,
        barmode="overlay",
        histnorm='probability',
        labels=LABELS,
    )
    fig.update_yaxes(title_text="Share of Census Block Groups", tickformat=".0%")
    fig.update_traces(opacity=0.6)
    return fig
