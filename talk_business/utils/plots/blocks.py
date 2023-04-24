import json
import os

import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv

load_dotenv()


def plot_blocks_choropleth(
    data: gpd.GeoDataFrame,
    id: str,
    value: str,
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
    )

    uirevision = "Don't change" if uichange else None
    fig.update_layout(
        mapbox_style="light",
        mapbox_accesstoken=os.getenv("MAPBOX_TOKEN"),
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        uirevision=uirevision,
    )
    fig.update_traces(marker_line_width=0.3, marker_line_color="white")
    return fig
