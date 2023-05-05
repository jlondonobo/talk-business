import json
import os
from typing import Union

import geopandas as gpd
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def id_is_selected(s: pd.Series, selected_id: str) -> pd.Series:
    """Returns a boolean series indicating if a polygon is selected."""
    return s == selected_id


def plot_highlighted_choropleth(
    geodata: gpd.GeoDataFrame,
    selection: str,
    id_col: str,
    geometry_col: str = "geometry",
    selected_color: str = "#EAB9A5",
    default_color: str = "#F4F4F4",
    hover_data: Union[dict, None] = None,
    zoom: int = 9,
    center: dict = {"lat": 6.240833, "lon": -75.530553},
) -> go.Figure:
    """Return choropleth map with highlighted selection."""
    geojson_data = json.loads(geodata.set_index(id_col).to_json())
    geodata = geodata.assign(
        is_selected=lambda df: id_is_selected(df[id_col], selection),
    )

    fig = px.choropleth_mapbox(
        geodata,
        geojson=geojson_data,
        locations=id_col,
        color="is_selected",
        color_discrete_map={True: selected_color, False: default_color},
        mapbox_style=None,
        zoom=zoom,
        center=center,
        hover_data=hover_data,
        opacity=0.7,
    )

    fig.update_layout(
        mapbox_style="light",
        mapbox_accesstoken=os.environ["MAPBOX_TOKEN"],
        margin=dict(l=0, r=0, t=0, b=0),
        uirevision="Don't change",
        showlegend=False,
    )
    return fig