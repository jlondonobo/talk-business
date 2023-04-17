from typing import Any, Union

AGE_GROUPS = {
    "Under 5 years": {
        "codes": [
            "B01001e27",
            "B01001e3",
        ],
        "name": "00-05"
    },
    "5 to 9 years": {
        "codes": [
            "B01001e28",
            "B01001e4",
        ],
        "name": "05-10"
    },
    "10 to 14 years": {
        "codes": [
            "B01001e29",
            "B01001e5",
        ],
        "name": "10-14"
        
    },
    "15 to 19 years": {
        "codes": [
            "B01001e31",
            "B01001e7",
            "B01001e30",
            "B01001e6",
        ],
        "name": "15-19"
    },
    "20 to 24 years": {
        "codes": [
            "B01001e10",
            "B01001e34",
            "B01001e33",
            "B01001e9",
            "B01001e32",
            "B01001e8",
        ],
        "name": "20-24"
    },
    "25 to 29 years": {
        "codes": [
            "B01001e11",
            "B01001e35",
        ],
        "name": "25-29"
    },
    "30 to 34 years": {
        "codes": [
            "B01001e12",
            "B01001e36",
        ],
        "name": "30-34"
    },
    "35 to 39 years": {
        "codes": [
            "B01001e13",
            "B01001e37",
        ],
        "name": "35-39"
    },
    "40 to 44 years": {
        "codes": [
            "B01001e14",
            "B01001e38",
        ],
        "name": "40-44"
    },
    "45 to 49 years": {
        "codes": [
            "B01001e15",
            "B01001e39",
        ],
        "name": "45-49"
    },
    "50 to 54 years": {
        "codes": [
            "B01001e16",
            "B01001e40",
        ],
        "name": "50-54"
    },
    "55 to 59 years": {
        "codes": [
            "B01001e17",
            "B01001e41",
        ],
        "name": "55-59"
    },
    "60 to 64 years": {
        "codes": [
            "B01001e19",
            "B01001e43",
            "B01001e18",
            "B01001e42",
        ],
        "name": "60-64"
    },
    "65 to 69 years": {
        "codes": [
            "B01001e21",
            "B01001e45",
            "B01001e20",
            "B01001e44",
        ],
        "name": "65-69"
    },
    "70 to 74 years": {
        "codes": [
            "B01001e22",
            "B01001e46",
        ],
        "name": "70-74"
    },
    "75 to 79 years": {
        "codes": [
            "B01001e23",
            "B01001e47",
        ],
        "name": "75-79"
    },
    "80 to 84 years": {
        "codes": [
            "B01001e24",
            "B01001e48",
        ],
        "name": "80-84"
    },
    "85 years and over": {
        "codes": [
            "B01001e25",
            "B01001e49",
        ],
        "name": "85-100"
    },
}


def format_horizontal_sum(columns: list[str]) -> str:
    """Returns a SELECT statement for a SUM."""
    return " + ".join([f'"{column}"' for column in columns])


def format_sum_with_horizontal_sum(columns: list[str], alias: Union[str, int]) -> str:
    """Returns a SELECT statement for a SUM."""
    horizontal_sum = format_horizontal_sum(columns)
    return f'SUM({horizontal_sum}) AS "{alias}"'


def select_age_groups(age_groups: dict[str, Any]) -> str:
    """Returns a SELECT statement for age groups."""
    select = []
    for group, data in age_groups.items():
        select.append(format_sum_with_horizontal_sum(data["codes"], data["name"]))
    return ", ".join(select)


query = f"""
    SELECT
    {select_age_groups(AGE_GROUPS)}
    FROM OPENCENSUSDATA.PUBLIC."2020_CBG_B01"
    LEFT JOIN OPENCENSUSDATA.PUBLIC."2020_CBG_GEOMETRY_WKT" as c USING (census_block_group)
    LEFT JOIN PERSONAL.PUBLIC.NTA_MAPPER AS nta ON nta.CT2020=c.tract_code 
    WHERE "STATE" = 'NY' AND "COUNTY"='New York County'
    GROUP BY NTANAME;
"""
