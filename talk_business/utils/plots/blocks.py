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
    )

    fig.update_layout(
        mapbox_style="light",
        mapbox_accesstoken=os.getenv("MAPBOX_TOKEN"),
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        uirevision="Don't change",
        height=700,
    )
    fig.update_traces(marker_line_width=1, marker_line_color="white")
    return fig
