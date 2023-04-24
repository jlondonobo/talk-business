import plotly.graph_objects as go
from utils.plots import neighborhood as nplot
from utils.sql import neighborhood_explorer as ne
from utils.transformers import neighborhood as ntransform


def plot_age_dist(
    county_fips: str, nta_code: str, share: bool, compare: bool
) -> go.Figure:
    """Query and plot age distribution data."""
    TABLE = "AGE_GROUPS"
    age = ne.get_distribution(TABLE, nta_code)
    age = ntransform.transform_age(age)
    if compare:
        county = ne.get_county_distribution(TABLE, county_fips)
        county = ntransform.transform_age(county)

        title = (
            f"<b>What is the age of {nta_code} residents?<br>"
            f"<sup>{nta_code} vs {county_fips}"
        )
        return nplot.compare_distributions(
            age, county, TABLE, share, title, nta_code, county_fips
        )
    return nplot.distribution(
        age,
        TABLE,
        share=share,
        title="Age Distribution",
        color="AGE_CATEGORY",
    )


def plot_family_income_dist(
    county_fips: str, nta_code: str, share: bool, compare: bool
) -> go.Figure:
    """Query and plot family income distribution data."""
    TABLE = "FAMILY_INCOME_GROUPS"
    income = ne.get_distribution(TABLE, nta_code)
    income = ntransform.transform_family_income(income)

    if compare:
        county = ne.get_county_distribution(TABLE, county_fips)
        county = ntransform.transform_family_income(county)

        title = (
            f"<b>How much do families in {nta_code} earn each year?<br>"
            f"<sup>{nta_code} vs {county_fips}"
        )
        return nplot.compare_distributions(
            income, county, TABLE, share, title, nta_code, county_fips
        )

    return nplot.distribution(
        income,
        TABLE,
        share=share,
        title="Family Income Distribution",
    )


def plot_rent_dist(
    county_fips: str, nta_code: str, share: bool, compare: bool
) -> go.Figure:
    """Query and plot rent distribution data."""
    TABLE = "RENT_GROUPS"
    rent = ne.get_distribution(TABLE, nta_code)
    rent = ntransform.transform_rent(rent)
    if compare:
        county = ne.get_county_distribution(TABLE, county_fips)
        county = ntransform.transform_rent(county)

        title = (
            f"<b>How much do people in {nta_code} pay for rent?<br>"
            f"<sup>{nta_code} vs {county_fips}"
        )
        return nplot.compare_distributions(
            rent, county, TABLE, share, title, nta_code, county_fips
        )

    return nplot.distribution(
        rent,
        TABLE,
        share=share,
        title="Monthly Rent Distribution",
    )


def plot_race_dist(
    county_fips: str, nta_code: str, share: bool, compare: bool
) -> go.Figure:
    """Query and plot race distribution data."""
    TABLE = "RACE_GROUPS"
    race = ne.get_distribution(TABLE, nta_code)
    race = ntransform.transform_race(race)
    if compare:
        county = ne.get_county_distribution(TABLE, county_fips)
        county = ntransform.transform_race(county)

        title = (
            f"<b>What are the races of {nta_code}'s population?<br>"
            f"<sup>{nta_code} vs {county_fips}"
        )
        return nplot.compare_distributions(
            race, county, TABLE, share, title, nta_code, county_fips
        )

    return nplot.distribution(
        race,
        TABLE,
        share=share,
        title="Race profile",
    )


def plot_occupation_dist(
    county_fips: str, nta_code: str, share: bool, compare: bool
) -> go.Figure:
    """Query and plot occupation distribution data."""
    TABLE = "OCCUPATION_GROUPS"
    occupation = ne.get_distribution(TABLE, nta_code)
    occupation = ntransform.transform_occupation(occupation)
    if compare:
        county = ne.get_county_distribution(TABLE, county_fips)
        county = ntransform.transform_occupation(county)

        title = (
            f"<b>What jobs do people from {nta_code} work?<br>"
            f"<sup>{nta_code} vs {county_fips}"
        )
        return nplot.compare_distributions(
            occupation, county, TABLE, share, title, nta_code, county_fips
        )
    return nplot.distribution(
        occupation,
        TABLE,
        share=share,
        title="Occupation",
        orient="h",
    )





def plot_enrollment_dist(
    county_fips: str, nta_code: str, share: bool, compare: bool
) -> go.Figure:
    """Query and plot enrollment distribution data."""
    TABLE = "ENROLLMENT_GROUPS"
    enrollment = ne.get_distribution(TABLE, nta_code)
    enrollment = ntransform.transform_enrollment(enrollment)
    if compare:
        county = ne.get_county_distribution(TABLE, county_fips)
        county = ntransform.transform_enrollment(county)

        title = (
            f"<b>What stage of education are the currently-enrolled population  of {nta_code} going through?<br>"
            f"<sup>{nta_code} vs {county_fips}"
        )
        return nplot.compare_distributions(
            enrollment, county, TABLE, share, title, nta_code, county_fips
        )

    return nplot.distribution(
        enrollment,
        TABLE,
        share=share,
        title="Stage of Studies",
    )
