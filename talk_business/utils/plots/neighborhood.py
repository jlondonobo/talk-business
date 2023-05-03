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


def vertical_distribuion(
    data: pd.DataFrame,
    labels: str,
    share: bool,
    title: str,
    color: Union[str, None] = None,
) -> go.Figure:
    metric = "pop_share" if share else "population"
    tickformat = ",.0%" if share else ",.0f"

    fig = px.bar(
        data,
        x=labels,
        y=metric,
        text_auto=tickformat,
        color=color,
        labels=LABELS,
        title=title,
    )

    fig.update_layout(xaxis_type="category")
    fig.update_yaxes(tickformat=tickformat)
    return fig


def horizontal_distribuion(
    data: pd.DataFrame,
    labels: str,
    share: bool,
    title: str,
    color: Union[str, None] = None,
) -> go.Figure:
    metric = "pop_share" if share else "population"
    tickformat = ",.0%" if share else ",.0f"

    fig = px.bar(
        data,
        x=metric,
        y=labels,
        text_auto=tickformat,
        color=color,
        labels=LABELS,
        title=title,
        orientation="h",
    )

    fig.update_layout(yaxis_type="category")
    fig.update_xaxes(tickformat=tickformat)
    return fig


def distribution(
    data: pd.DataFrame,
    labels: str,
    share: bool,
    title: str,
    color: Union[str, None] = None,
    orient: str = "v",
) -> go.Figure:
    """
    Plots a bar chart of the distribution of the data.
    """
    if orient == "v":
        return vertical_distribuion(data, labels, share, title, color)
    else:
        return horizontal_distribuion(data, labels, share, title, color)


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


def compare_distributions(
    data: pd.DataFrame,
    comp_data: pd.DataFrame,
    labels: str,
    share: bool,
    title: str,
    data_name: str,
    comp_data_name: str,
) -> go.Figure:
    """Plot a value from `main` in comparison to `comps`."""
    values = "pop_share" if share else "population"
    value_format = ".1%" if share else ",.0f"

    fig = go.Figure(data=[
        go.Bar(
            x=comp_data[labels],
            y=comp_data[values],
            # marker_color='#DEDEDE',
            # marker_line_color='rgb(8,48,107)',
            marker_line_width=0,
            name=comp_data_name,
        ),
        go.Bar(
            x=data[labels],
            y=data[values],
            width=0.6,
            # marker_color="blue",
            # marker_line_color='#ffffff',
            marker_line_width=0.0,
            name=data_name,
        )
    ])
    fig.update_layout(
        barmode="overlay",
        title=title,
        legend_traceorder="reversed",
        xaxis_type="category",
    )
    fig.update_xaxes(title_text=comp_data[labels].name, type="category")
    fig.update_yaxes(title_text=comp_data[values].name, tickformat=value_format)
    fig.update_layout(hovermode="x")
    return fig


def treemap(data: pd.DataFrame, nta: str) -> go.Figure:
    """Return a treemap of the places in a neighborhood."""
    fig = px.treemap(
        data,
        path=[px.Constant(f"Places in {nta}"), "CATEGORY", "SUB_CATEGORY"],
        values="PLACES_COUNT",
        labels={"CATEGORY": "Category", "SUB_CATEGORY": "Sub-category", "PLACES_COUNT": "Number of places"},
    )
    fig.update_layout(
        margin=dict(t=40, l=0, r=0, b=0),
        title_text=f"Places distribution in <b>{nta}</b>",
        title_x=0,
    )
    return fig
