from typing import Union

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

LABELS = {
    "AGE_GROUPS": "Age",
    "ENROLLMENT_GROUPS": "School enrollment",
    "FAMILY_INCOME_GROUPS": "Family income (yearly)",
    "OCCUPATION_GROUPS": "Occupation",
    "RACE_GROUPS": "Race",
    "RENT_GROUPS": "Rent (monthly)",
    "population": "Population",
    "age_category": "Age group",
    "income_groups": "Family income",
    "pop_share": "Share of population",
}


def distribution(
    data: pd.DataFrame,
    labels: str,
    metric: str,
    title: str,
    color: Union[str, None] = None,
    orient: str = "v",
) -> go.Figure:
    """
    Plots a bar chart of the distribution of the data.
    """
    
    tickformat = ",.0%" if metric == "pop_share" else ",.0f"
    
    if orient == "v":
        x = labels
        y = metric

    else:
        x = metric
        y = labels

    fig = px.bar(
        data,
        x=x,
        y=y,
        text_auto=tickformat,
        color=color,
        labels=LABELS,
        title=title,
        orientation=orient,
    )

    if orient == "v":
        fig.update_layout(xaxis_type="category")
        fig.update_yaxes(tickformat=tickformat)
    else:
        fig.update_layout(yaxis_type="category")
        fig.update_xaxes(tickformat=tickformat)
    return fig


def plot_donut(data: pd.DataFrame, labels: str, title: str) -> go.Figure:
    """Return a donut chart from a DataFrame."""
    fig = go.Figure(
        data=[
            go.Pie(
                labels=data[labels],
                values=data["population"],
                hole=0.5,
                textinfo="label+percent",
                sort=False,
                direction="clockwise",
            )
        ]
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=70, b=0),
        showlegend=False,
        title=dict(
            x=0.5,
            xanchor="center",
            text=title,
        ),
        height=300,
    )
    return fig
