import geopandas as gpd


def dissolve_count(
    gdf: gpd.GeoDataFrame,
    column: str,
) -> gpd.GeoDataFrame:
    return (
        gdf.filter(["COUNTY_FIPS", "COUNTY", "NTA_NAME", "TRACT_CODE", column, "geometry"])
        .dissolve(by=["COUNTY_FIPS", "COUNTY", "NTA_NAME", "TRACT_CODE"], aggfunc="sum")
        .reset_index()
    )


def dissolve_weighted_average(
    gdf: gpd.GeoDataFrame,
    by: str,
    column: str,
    weight: str,
) -> gpd.GeoDataFrame:
    return (
        gdf.filter(["COUNTY_FIPS", "COUNTY", "NTA_NAME", by, "geometry", column, weight])
        .assign(premultiplied=lambda df: df[column] * df[weight])
        .dissolve(by=["COUNTY_FIPS", "COUNTY", "NTA_NAME", by], aggfunc="sum")
        .reset_index()
        .assign(**{column: lambda df: df["premultiplied"] / df[weight]})
    )

