import json
import os
from typing import Any, Union

import geopandas as gpd
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv
from utils.columns import COLUMNS

load_dotenv()
LABELS = {col: meta["full_label"] for col, meta in COLUMNS.items()}


def plot_blocks_choropleth(
    data: gpd.GeoDataFrame,
    id: str,
    value: str,
    borders: Union[dict[Any, Any], None] = None,
    nta_centroids: pd.DataFrame = pd.DataFrame(),
    center: dict[str, float] = {"lat": 40.7128, "lon": -74.0060},
    zoom: int = 12,
    uichange: bool = False,
) -> go.Figure:
    """Plot blocks colored by 'value'.

    Args:
        data (gpd.GeoDataFrame): block-level census geodataframe
        id (str): name of columm with geometry ids
        value (str): name of column with values to color by
        center (dict[str, float]): dict with lat and lon values
        zoom (int, optional): zoom level. Defaults to 12.

    Returns:
        go.Figure: Choropleth map
    """

    geojson = json.loads(data.set_index(id)["geometry"].to_json())

    fig = px.choropleth_mapbox(
        data,
        geojson=geojson,
        locations=id,
        color=value,
        color_continuous_scale="Sunsetdark",
        center=center,
        zoom=zoom,
        custom_data=["COUNTY", "NTA_NAME"],
        hover_data={
            "COUNTY": True,
            "NTA_NAME": True,
            value: True,
        },
        labels=LABELS,
    )
    if borders is not None:
        marker_line_width = 0
    else:
        marker_line_width = 0.3

    fig.update_traces(
        marker_line_width=marker_line_width,
        marker_line_color="white",
        hovertemplate=(
            "<b>%{customdata[1]}</b><br>"
            "<i>GeoID: %{location}</i><br>"
            "<br>"
            f"{LABELS[value]}<br>"
            "<b>%{z}</b><br>"
            "<extra></extra>"
        ),
        hoverlabel=dict(bgcolor="#2D3847"),
    )

    uirevision = "Don't change" if uichange else None
    if borders is not None:
        fig.add_scattermapbox(
            "above",
            lat=nta_centroids["LAT"],
            lon=nta_centroids["LON"],
            text=nta_centroids["NTA_NAME"],
            mode='text',
            textfont=dict(size=7, color='#4A4A4A'),
        )

        mapbox_layers = [
            dict(
                sourcetype="geojson",
                source=borders,
                color="grey",
                type="line",
                line=dict(width=0.5),
                opacity=0.5,
            )
        ]
    else:
        mapbox_layers = None

    fig.update_layout(
        mapbox_style="light",
        mapbox_accesstoken=os.environ["MAPBOX_TOKEN"],
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        uirevision=uirevision,
        mapbox_layers=mapbox_layers,
    )

    
    fig.update_coloraxes(
        colorbar=dict(
            orientation="h",
            y=0,
            tickfont=dict(color="black"),
            title=dict(side="top", font=dict(color="black")),
            thickness=5,
            len=0.4,
            x=0.93,
            xanchor="right",
        )
    )
    return fig
