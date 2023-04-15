import geopandas as gpd


def dissolve_count(gdf: gpd.GeoDataFrame, column: str) -> gpd.GeoDataFrame:
    return (
        gdf
        .filter(["TRACT_CODE", column, "geometry"])
        .dissolve(by='TRACT_CODE', aggfunc='sum')
        .reset_index()
    )