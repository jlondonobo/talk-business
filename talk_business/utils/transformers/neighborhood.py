import pandas as pd
from utils.transformers import constants as const


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


def compute_share(s: pd.Series) -> pd.Series:
    """Computes the percentage of the population in each category."""
    return s / s.sum()


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
    data: pd.DataFrame, occupation_mapper: dict[str, str], n: int = 10
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


def transform_age(data: pd.DataFrame) -> pd.DataFrame:
    """
    Assign 'AGE_CATEGORY' and compute share.
    """
    return data.assign(
        AGE_CATEGORY=lambda df: map_to_category(df["AGE_GROUPS"], const.AGE_CATEGORY),
        pop_share=lambda df: compute_share(df["population"]),
    )


def transform_enrollment(data) -> pd.DataFrame:
    """
    Resort enrollment categories and compute share.
    """
    return (
        data
        .pipe(resort_categories, "ENROLLMENT_GROUPS", const.SORTED_ENROLLMENT)
        .assign(pop_share=lambda df: compute_share(df["population"]))
    )


def transform_family_income(data: pd.DataFrame) -> pd.DataFrame:
    """
    Bin family income in larger bins and compute share.
    """
    return (
        data
        .pipe(aggregate, "FAMILY_INCOME_GROUPS", const.FAMILY_INCOME_GROUPPED)
        .assign(pop_share=lambda df: compute_share(df["population"]))
    )


def transform_occupation(data: pd.DataFrame) -> pd.DataFrame:
    """
    Parse occupation data and compute share.
    """
    return (
        data
        .assign(
            pop_share=lambda df: compute_share(df["population"]),
            OCCUPATION_GROUPS=data["OCCUPATION_GROUPS"].map(const.OCCUPATION_MAPPER),
        )
        .sort_values("population", ascending=True)
    )


def transform_race(data: pd.DataFrame) -> pd.DataFrame:
    """
    Group races and compute share.
    """
    return (
        data
        .pipe(aggregate, "RACE_GROUPS", const.RACE_GROUPS_MAPPER, False)
        .assign(pop_share=lambda df: compute_share(df["population"]))
    )


def transform_rent(data: pd.DataFrame) -> pd.DataFrame:
    """
    Bin rent in larger bins and compute share.
    """
    return (
        data
        .pipe(aggregate, "RENT_GROUPS", const.RENT_MAPPER)
        .assign(pop_share=lambda df: compute_share(df["population"]))
    )
