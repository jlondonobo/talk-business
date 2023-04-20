import pandas as pd


def map_to_category(s: pd.Series, mapper: dict[str, str]) -> pd.Categorical:
    """
    Map a series to a new category.
    """
    ordered_categories = pd.Series(mapper).unique()
    return pd.Categorical(s.map(mapper), categories=ordered_categories, ordered=True)


def simple_map(s: pd.Series, mapper: dict[str, str]) -> pd.Series:
    """
    Map a series to a new category.
    """
    return s.map(mapper)


def aggregate(
    data: pd.DataFrame,
    col: str,
    mapper: dict[str, str],
    sorted_map: bool = True,
) -> pd.DataFrame:
    """
    Aggregate categories even more.
    """
    if sorted_map:
        map_fun = map_to_category
        sort_val = col
    else:
        map_fun = simple_map
        sort_val = "population"
    return (
        data.assign(**{col: lambda x: map_fun(x[col], mapper)})
        .groupby(col)["population"]
        .sum()
        .reset_index()
        .sort_values(sort_val)
    )


def resort_categories(
    data: pd.DataFrame,
    col: str,
    order: list[str],
) -> pd.DataFrame:
    """Resort category order for poor original data."""
    return data.assign(
        **{col: lambda x: pd.Categorical(x[col], categories=order, ordered=True)}
    ).sort_values(col)


def parse_occupation(
    data: pd.DataFrame,
    occupation_mapper: dict[str, str],
    n: int = 10
) -> pd.DataFrame:
    """Occupation data comes with encoded names."""
    return (
        data.nlargest(n, "population")
        .sort_values("population", ascending=True)
        .assign(
            OCCUPATION_GROUPS=lambda df: df["OCCUPATION_GROUPS"]
            .map(occupation_mapper)
            .str.replace(" occupations", "")
        )
    )
