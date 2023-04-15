import geopandas as gpd
import pandas as pd


def to_gdf(df: pd.DataFrame) -> gpd.GeoDataFrame:
    """Converts a pandas dataframe with WKT geometry to a geopandas dataframe."""
    df = df.rename(columns={"GEOMETRY": "geometry"})
    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.GeoSeries.from_wkt(df["geometry"]),
        crs="EPSG:4326",
    )
    return gdf
