import plotly.graph_objects as go
from utils.plots import neighborhood as nplot
from utils.sql import neighborhood_explorer as ne
from utils.transformers import neighborhood as ntransform


def plot_age_dist(neighborhood: str, share: bool) -> go.Figure:
    """Query and plot age distribution data."""
    TABLE = "AGE_GROUPS"
    age = ne.get_distribution(TABLE, neighborhood)
    age = ntransform.transform_age(age)
    return nplot.distribution(
            age,
            TABLE,
            share=share,
            title="Age Distribution",
            color="AGE_CATEGORY",
    )
    

def plot_enrollment_dist(neighborhood: str, share: bool) -> go.Figure:
    """Query and plot enrollment distribution data."""
    TABLE = "ENROLLMENT_GROUPS"
    enrollment = ne.get_distribution(TABLE, neighborhood)
    enrollment = ntransform.transform_enrollment(enrollment)
    return nplot.distribution(
        enrollment,
        TABLE,
        share=share,
        title="Stage of Studies",
    )


def plot_family_income_dist(neighborhood: str, share: bool) -> go.Figure:
    """Query and plot family income distribution data."""
    TABLE = "FAMILY_INCOME_GROUPS"
    income = ne.get_distribution(TABLE, neighborhood)
    income = ntransform.transform_family_income(income)
    return nplot.distribution(
        income,
        TABLE,
        share=share,
        title="Family Income Distribution",
    )
    

def plot_occupation_dist(neighborhood: str, share: bool) -> go.Figure:
    """Query and plot occupation distribution data."""
    TABLE = "OCCUPATION_GROUPS"
    occupation = ne.get_distribution(TABLE, neighborhood)
    occupation = ntransform.transform_occupation(occupation)
    return nplot.distribution(
        occupation,
        TABLE,
        share=share,
        title="Occupation",
        orient="h",
    )


def plot_race_dist(neighborhood: str, share: bool) -> go.Figure:
    """Query and plot race distribution data."""
    TABLE = "RACE_GROUPS"
    race = ne.get_distribution(TABLE, neighborhood)
    race = ntransform.transform_race(race)
    return nplot.distribution(
        race,
        TABLE,
        share=share,
        title="Race profile",
    )


def plot_rent_dist(neighborhood: str, share: bool) -> go.Figure:
    """Query and plot rent distribution data."""
    TABLE = "RENT_GROUPS"
    rent = ne.get_distribution(TABLE, neighborhood)
    rent = ntransform.transform_rent(rent)
    return nplot.distribution(
        rent,
        TABLE,
        share=share,
        title="Monthly Rent Distribution",
    )

