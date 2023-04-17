import geopandas as gpd


def dissolve_count(
    gdf: gpd.GeoDataFrame,
    column: str,
) -> gpd.GeoDataFrame:
    return (
        gdf.filter(["TRACT_CODE", "COUNTY_FIPS", "COUNTY", column, "geometry"])
        .dissolve(by=["COUNTY", "TRACT_CODE", "COUNTY_FIPS"], aggfunc="sum")
        .reset_index()
    )


def dissolve_weighted_average(
    gdf: gpd.GeoDataFrame,
    by: str,
    column: str,
    weight: str,
) -> gpd.GeoDataFrame:
    return (
        gdf.filter(["COUNTY", "COUNTY_FIPS", by, "geometry", column, weight])
        .assign(premultiplied=lambda df: df[column] * df[weight])
        .dissolve(by=[by, "COUNTY", "COUNTY_FIPS"], aggfunc="sum")
        .reset_index()
        .assign(**{column: lambda df: df["premultiplied"] / df[weight]})
    )

