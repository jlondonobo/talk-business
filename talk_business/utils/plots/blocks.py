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
ADD_LABELS = {
    "MEDIAN_AGE-MALE": "Male Median Age",
    "MEDIAN_AGE-FEMALE": "Female Median Age",
    "RACE-WHITE": "White Population",
    "RACE-BLACK_OR_AFRICAN_AMERICAN": "Black or African American Population",
    "RACE-AMERICAN_INDIAN_AND_ALASKA_NATIVE": "Indian and Alaska Native Population",
    "RACE-ASIAN": "Asian Population",
    "RACE-NATIVE_HAWAIIAN_AND_OTHER_PACIFIC_ISLANDER_ALONE": "Hawaiian Population",
    "RACE-SOME_OTHER_RACE": "Other race Population",
    "RACE-TWO_OR_MORE_RACES": "Two or more races Population",
    
}
LABELS.update(ADD_LABELS)


def plot_blocks_choropleth(
    data: gpd.GeoDataFrame,
    id: str,
    value: str,
    borders: Union[dict[Any, Any], None] = None,
    nta_centroids: pd.DataFrame = pd.DataFrame(),
    center: dict[str, float] = {"lat": 40.7128, "lon": -74.0060},
    zoom: int = 12,
    uichange: bool = False,
    parks = None,
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

    range_color = None
    hovertemplate = "<b>%{customdata[1]}</b>"
    if value is not None:
        zmin = data[value].quantile(0.05)
        zmax = data[value].quantile(0.95)
        range_color = [zmin, zmax]
        hovertemplate = (
                "<b>%{customdata[1]}</b><br>"
                "<i>GeoID: %{location}</i><br>"
                "<br>"
                f"{LABELS[value]}<br>"
                "<b>%{z}</b><br>"
                "<extra></extra>"
            )

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
        range_color=range_color,
    )
    if borders is not None:
        marker_line_width = 0
    else:
        marker_line_width = 0.3

    fig.update_traces(
        marker_line_width=marker_line_width,
        marker_line_color="white",
        hovertemplate=hovertemplate,
        hoverlabel=dict(bgcolor="#2D3847"),
    )

    uirevision = "Don't change" if uichange else None
    mapbox_layers = []
    if borders is not None:
        fig.add_scattermapbox(
            "above",
            lat=nta_centroids["LAT"],
            lon=nta_centroids["LON"],
            text=nta_centroids["NTA_NAME"],
            mode='text',
            textfont=dict(size=7, color='#4A4A4A'),
        )

        borders_layer = dict(
            sourcetype="geojson",
            source=borders,
            color="grey",
            type="line",
            line=dict(width=0.5),
            opacity=0.5,
        )
        mapbox_layers.append(borders_layer)
    
    if parks is not None:
        parks_json=json.loads(parks.to_json())
        parks_layer = dict(
            sourcetype="geojson",
            source=parks_json,
            color="#088C11",
            type="fill",
            line=dict(width=5),
            opacity=0.3,
        )
        mapbox_layers.append(parks_layer)

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
