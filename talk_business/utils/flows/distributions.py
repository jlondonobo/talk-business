from utils.plots import neighborhood as nplot
from utils.sql import neighborhood_explorer as ne
from utils.transformers import constants as c
from utils.transformers import neighborhood as ntransform


def plot_distribution(style: str, neighborhood: str):
    if style == "AGE_GROUPS":
        age = ne.get_distribution("AGE_GROUPS", neighborhood)
        age = age.assign(
            age_category=lambda df: ntransform.map_to_category(
                df["AGE_GROUPS"], c.AGE_CATEGORY
            )
        )
        return nplot.distribution(
            age,
            "AGE_GROUPS",
            title="Age Distribution",
            color="age_category",
        )

    elif style == "ENROLLMENT_GROUPS":
        enrollment = ne.get_distribution("ENROLLMENT_GROUPS", neighborhood)
        enrollment = enrollment.pipe(
            ntransform.resort_categories, "ENROLLMENT_GROUPS", c.SORTED_ENROLLMENT
        )
        return nplot.distribution(
            enrollment,
            "ENROLLMENT_GROUPS",
            title="Stage of Studies",
        )
    elif style == "FAMILY_INCOME_GROUPS":
        income = ne.get_distribution("FAMILY_INCOME_GROUPS", neighborhood)
        income = ntransform.aggregate(
            income, "FAMILY_INCOME_GROUPS", c.FAMILY_INCOME_GROUPPED
        )
        return nplot.distribution(
            income,
            "FAMILY_INCOME_GROUPS",
            title="Family Income Distribution",
        )

    elif style == "OCCUPATION_GROUPS":
        occupation = ne.get_distribution("OCCUPATION_GROUPS", neighborhood)
        occupation = ntransform.parse_occupation(occupation, c.OCCUPATION_MAPPER, 10)
        return nplot.distribution(
            occupation, "OCCUPATION_GROUPS", title="Top 10 Common Jobs", orient="h"
        )

    elif style == "RACE_GROUPS":
        race = ne.get_distribution("RACE_GROUPS", neighborhood)
        race = ntransform.aggregate(race, "RACE_GROUPS", c.RACE_GROUPS_MAPPER, False)
        return nplot.plot_donut(race, "RACE_GROUPS", "Racial Profile")

    elif style == "RENT_GROUPS":
        rent = ne.get_distribution("RENT_GROUPS", neighborhood)
        rent = ntransform.aggregate(rent, "RENT_GROUPS", c.RENT_MAPPER)
        return nplot.distribution(
            rent,
            "RENT_GROUPS",
            title="Monthly Rent Distribution",
        )
