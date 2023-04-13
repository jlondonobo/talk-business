import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def plot_distribution_by_area(
    data: pd.DataFrame,
    column: str,
    area: str = "COUNTY",
) -> go.Figure:
    """
    A histogram to compare single variables in each area.
    """
    fig = px.histogram(
        data,
        x=column,
        color=area,
        barmode="overlay",
        histnorm='probability',
        labels={"COUNTY": "County"},
    )
    fig.update_yaxes(title_text="Share of Census Block Groups", tickformat=".0%")
    fig.update_traces(opacity=0.6)
    return fig
