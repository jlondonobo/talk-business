from utils.plots import neighborhood as nplot
from utils.sql import neighborhood_explorer as ne
from utils.transformers import constants as c
from utils.transformers import neighborhood as ntransform


def plot_distribution(style: str, neighborhood: str, share: bool):
    if share:
        metric = "pop_share"
    else:
        metric = "population"

    if style == "AGE_GROUPS":
        age = ne.get_distribution(style, neighborhood)
        age = age.assign(
            age_category=lambda df: ntransform.map_to_category(
                df[style], c.AGE_CATEGORY
            ),
            pop_share=lambda df: ntransform.compute_share(df["population"]),
        )
        return nplot.distribution(
            age,
            style,
            metric=metric,
            title="Age Distribution",
            color="age_category",
        )

    elif style == "ENROLLMENT_GROUPS":
        enrollment = (
            ne.get_distribution(style, neighborhood)
        )
        enrollment = enrollment.pipe(
            ntransform.resort_categories, style, c.SORTED_ENROLLMENT
        ).assign(pop_share=lambda df: ntransform.compute_share(df["population"]))
        return nplot.distribution(
            enrollment,
            style,
            metric=metric,
            title="Stage of Studies",
        )
    elif style == "FAMILY_INCOME_GROUPS":
        income = ne.get_distribution(style, neighborhood)
        income = ntransform.aggregate(
            income, style, c.FAMILY_INCOME_GROUPPED
        ).assign(pop_share=lambda df: ntransform.compute_share(df["population"]))
        return nplot.distribution(
            income,
            style,
            metric=metric,
            title="Family Income Distribution",
        )

    elif style == "OCCUPATION_GROUPS":
        occupation = ne.get_distribution(style, neighborhood)
        occupation = (
            ntransform.parse_occupation(occupation, c.OCCUPATION_MAPPER, 10)
            .assign(pop_share=lambda df: ntransform.compute_share(df["population"]))
        )
        return nplot.distribution(
            occupation, style, metric=metric, title="Top 10 Common Jobs", orient="h"
        )

    elif style == "RACE_GROUPS":
        race = ne.get_distribution(style, neighborhood)
        race = (
            ntransform.aggregate(race, style, c.RACE_GROUPS_MAPPER, False)
            .assign(pop_share=lambda df: ntransform.compute_share(df["population"]))
        )
        return nplot.plot_donut(race, style, "Racial Profile")

    elif style == "RENT_GROUPS":
        rent = ne.get_distribution(style, neighborhood)
        rent = (
            ntransform.aggregate(rent, style, c.RENT_MAPPER)
            .assign(pop_share=lambda df: ntransform.compute_share(df["population"]))
        )
        return nplot.distribution(
            rent,
            style,
            metric=metric,
            title="Monthly Rent Distribution",
        )
