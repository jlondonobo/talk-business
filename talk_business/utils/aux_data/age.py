from typing import Any, Union

from utils.columns import COLUMNS

AGE_GROUPS = {
    "Under 5 years": {
        "codes": [
            "B01001e27",
            "B01001e3",
        ],
        "name": "00-05",
    },
    "5 to 9 years": {
        "codes": [
            "B01001e28",
            "B01001e4",
        ],
        "name": "05-10",
    },
    "10 to 14 years": {
        "codes": [
            "B01001e29",
            "B01001e5",
        ],
        "name": "10-14",
    },
    "15 to 19 years": {
        "codes": [
            "B01001e31",
            "B01001e7",
            "B01001e30",
            "B01001e6",
        ],
        "name": "15-19",
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
        "name": "20-24",
    },
    "25 to 29 years": {
        "codes": [
            "B01001e11",
            "B01001e35",
        ],
        "name": "25-29",
    },
    "30 to 34 years": {
        "codes": [
            "B01001e12",
            "B01001e36",
        ],
        "name": "30-34",
    },
    "35 to 39 years": {
        "codes": [
            "B01001e13",
            "B01001e37",
        ],
        "name": "35-39",
    },
    "40 to 44 years": {
        "codes": [
            "B01001e14",
            "B01001e38",
        ],
        "name": "40-44",
    },
    "45 to 49 years": {
        "codes": [
            "B01001e15",
            "B01001e39",
        ],
        "name": "45-49",
    },
    "50 to 54 years": {
        "codes": [
            "B01001e16",
            "B01001e40",
        ],
        "name": "50-54",
    },
    "55 to 59 years": {
        "codes": [
            "B01001e17",
            "B01001e41",
        ],
        "name": "55-59",
    },
    "60 to 64 years": {
        "codes": [
            "B01001e19",
            "B01001e43",
            "B01001e18",
            "B01001e42",
        ],
        "name": "60-64",
    },
    "65 to 69 years": {
        "codes": [
            "B01001e21",
            "B01001e45",
            "B01001e20",
            "B01001e44",
        ],
        "name": "65-69",
    },
    "70 to 74 years": {
        "codes": [
            "B01001e22",
            "B01001e46",
        ],
        "name": "70-74",
    },
    "75 to 79 years": {
        "codes": [
            "B01001e23",
            "B01001e47",
        ],
        "name": "75-79",
    },
    "80 to 84 years": {
        "codes": [
            "B01001e24",
            "B01001e48",
        ],
        "name": "80-84",
    },
    "85 years and over": {
        "codes": [
            "B01001e25",
            "B01001e49",
        ],
        "name": "85-100",
    },
}


RENT_GROUPS = {
    "Less than $100": {"codes": ["B25063e3"], "name": "0-100", "numeric": 0},
    "$100 to $149": {"codes": ["B25063e4"], "name": "100-149", "numeric": 100},
    "$150 to $199": {"codes": ["B25063e5"], "name": "150-199", "numeric": 150},
    "$200 to $249": {"codes": ["B25063e6"], "name": "200-249", "numeric": 200},
    "$250 to $299": {"codes": ["B25063e7"], "name": "250-299", "numeric": 250},
    "$300 to $349": {"codes": ["B25063e8"], "name": "300-349", "numeric": 300},
    "$350 to $399": {"codes": ["B25063e9"], "name": "350-399", "numeric": 350},
    "$400 to $449": {"codes": ["B25063e10"], "name": "400-449", "numeric": 400},
    "$450 to $499": {"codes": ["B25063e11"], "name": "450-499", "numeric": 450},
    "$500 to $549": {"codes": ["B25063e12"], "name": "500-549", "numeric": 500},
    "$550 to $599": {"codes": ["B25063e13"], "name": "550-599", "numeric": 550},
    "$600 to $649": {"codes": ["B25063e14"], "name": "600-649", "numeric": 600},
    "$650 to $699": {"codes": ["B25063e15"], "name": "650-699", "numeric": 650},
    "$700 to $749": {"codes": ["B25063e16"], "name": "700-749", "numeric": 700},
    "$750 to $799": {"codes": ["B25063e17"], "name": "750-799", "numeric": 750},
    "$800 to $899": {"codes": ["B25063e18"], "name": "800-899", "numeric": 800},
    "$900 to $999": {"codes": ["B25063e19"], "name": "900-999", "numeric": 900},
    "$1 000 to $1 249": {"codes": ["B25063e20"], "name": "1000-1249", "numeric": 1000},
    "$1 250 to $1 499": {"codes": ["B25063e21"], "name": "1250-1499", "numeric": 1250},
    "$1 500 to $1 999": {"codes": ["B25063e22"], "name": "1500-1999", "numeric": 1500},
    "$2 000 to $2 499": {"codes": ["B25063e23"], "name": "2000-2499", "numeric": 2000},
    "$2 500 to $2 999": {"codes": ["B25063e24"], "name": "2500-2999", "numeric": 2500},
    "$3 000 to $3 499": {"codes": ["B25063e25"], "name": "3000-3499", "numeric": 3000},
    "$3 500 or more": {"codes": ["B25063e26"], "name": "3500-", "numeric": 3500},
}


FAMILY_INCOME = {
    "Less than $10 000": {"codes": ["B19001e2"], "name": "0-10000", "numeric": 0},
    "$10 000 to $14 999": {
        "codes": ["B19001e3"],
        "name": "10000-14999",
        "numeric": 10000,
    },
    "$15 000 to $19 999": {
        "codes": ["B19001e4"],
        "name": "15000-19999",
        "numeric": 15000,
    },
    "$20 000 to $24 999": {
        "codes": ["B19001e5"],
        "name": "20000-24999",
        "numeric": 20000,
    },
    "$25 000 to $29 999": {
        "codes": ["B19001e6"],
        "name": "25000-29999",
        "numeric": 25000,
    },
    "$30 000 to $34 999": {
        "codes": ["B19001e7"],
        "name": "30000-34999",
        "numeric": 30000,
    },
    "$35 000 to $39 999": {
        "codes": ["B19001e8"],
        "name": "35000-39999",
        "numeric": 35000,
    },
    "$40 000 to $44 999": {
        "codes": ["B19001e9"],
        "name": "40000-44999",
        "numeric": 40000,
    },
    "$45 000 to $49 999": {
        "codes": ["B19001e10"],
        "name": "45000-49999",
        "numeric": 45000,
    },
    "$50 000 to $59 999": {
        "codes": ["B19001e11"],
        "name": "50000-59999",
        "numeric": 50000,
    },
    "$60 000 to $74 999": {
        "codes": ["B19001e12"],
        "name": "60000-74999",
        "numeric": 60000,
    },
    "$75 000 to $99 999": {
        "codes": ["B19001e13"],
        "name": "75000-99999",
        "numeric": 75000,
    },
    "$100 000 to $124 999": {
        "codes": ["B19001e14"],
        "name": "100000-124999",
        "numeric": 100000,
    },
    "$125 000 to $149 999": {
        "codes": ["B19001e15"],
        "name": "125000-149999",
        "numeric": 125000,
    },
    "$150 000 to $199 999": {
        "codes": ["B19001e16"],
        "name": "150000-199999",
        "numeric": 150000,
    },
    "$200 000 or more": {"codes": ["B19001e17"], "name": "200000-", "numeric": 200000},
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


def query_distribution_per_nta(values: dict[str, Any], table: str) -> str:
    return f"""
        SELECT
        COUNTY,
        NTANAME,
        {select_age_groups(values)}
        FROM OPENCENSUSDATA.PUBLIC."2020_CBG_{table}"
        LEFT JOIN OPENCENSUSDATA.PUBLIC."2020_CBG_GEOMETRY_WKT" as c USING (census_block_group)
        LEFT JOIN PERSONAL.PUBLIC.NTA_MAPPER AS nta ON nta.CT2020=c.tract_code AND nta.COUNTYFIPS=c.COUNTY_FIPS
        WHERE STATE_FIPS = 36 AND COUNTY IN ('New York County', 'Queens County', 'Kings County', 'Richmond County', 'Bronx County')
        GROUP BY (COUNTY, NTANAME);
    """


age_query = query_distribution_per_nta(AGE_GROUPS, "B01")
rent_query = query_distribution_per_nta(RENT_GROUPS, "B25")
family_income_query = query_distribution_per_nta(FAMILY_INCOME, "B19")


STATISTICS = {
    "TOTAL_INCOME": {
        "query": 'SUM("B19001e1" * "B19013e1") as total_income_12_m',
        "table": "B19",
    },
    "TOTAL_POPULATION": {
        "query": 'SUM("B01001e1") as total_population',
        "table": "B01",
    },
    "ENROLLED_IN_SCHOOL": {
        "query": 'SUM("B14007e2") / SUM("B14007e1") as pctg_enrolled_in_school',
        "table": "B14",
    },
}


def query_nta_statistic(statistic: str) -> str:
    return f"""
        SELECT
            COUNTY,
            NTANAME,
            {STATISTICS[statistic]["query"]}
        FROM OPENCENSUSDATA.PUBLIC."2020_CBG_{STATISTICS[statistic]["table"]}"
        LEFT JOIN OPENCENSUSDATA.PUBLIC."2020_CBG_GEOMETRY_WKT" as c USING (census_block_group)
        LEFT JOIN PERSONAL.PUBLIC.NTA_MAPPER AS nta ON nta.CT2020=c.tract_code AND nta.COUNTYFIPS=c.COUNTY_FIPS
        WHERE STATE_FIPS = 36 AND COUNTY IN ('New York County', 'Queens County', 'Kings County', 'Richmond County', 'Bronx County')
        GROUP BY (COUNTY, NTANAME);
    """


total_income = query_nta_statistic("TOTAL_INCOME")
total_population = query_nta_statistic("TOTAL_POPULATION")


RACE = {
    key: {"codes": [value], "name": key}
    for key, value in COLUMNS["RACE"]["segments"].items()
}

EDUCATION = {
    "ELEMENTARY_SCHOOL": {
        "codes": [
            "B14007e4",
            "B14007e5",
            "B14007e6",
            "B14007e7",
            "B14007e8",
            "B14007e9",
        ],
        "name": "ELEMENTARY_SCHOOL",
    },
    "HIGHER_EDUCATION": {
        "codes": ["B14007e17", "B14007e18", "B14007e3"],
        "name": "HIGHER_EDUCATION",
    },
    "HIGH_SCHOOL": {
        "codes": ["B14007e13", "B14007e14", "B14007e15", "B14007e16"],
        "name": "HIGH_SCHOOL",
    },
    "MIDDLE_SCHOOL": {
        "codes": ["B14007e10", "B14007e11", "B14007e12"],
        "name": "MIDDLE_SCHOOL",
    },
}


OCCUPATION = {
    "Building and grounds cleaning and maintenance occupations": {
        "codes": [
            "C24010e25",
            "C24010e61",
        ],
        "name": "1",
    },
    "Computer engineering and science occupations": {
        "codes": [
            "C24010e43",
            "C24010e7",
        ],
        "name": "2",
    },
    "Construction and extraction occupations": {
        "codes": [
            "C24010e32",
            "C24010e68",
        ],
        "name": "3",
    },
    "Education legal community service arts and media occupations": {
        "codes": [
            "C24010e11",
            "C24010e47",
        ],
        "name": "4",
    },
    "Farming fishing and forestry occupations": {
        "codes": [
            "C24010e31",
            "C24010e67",
        ],
        "name": "5",
    },
    "Food preparation and serving related occupations": {
        "codes": [
            "C24010e24",
            "C24010e60",
        ],
        "name": "6",
    },
    "Healthcare practitioners and technical occupations": {
        "codes": [
            "C24010e16",
            "C24010e52",
        ],
        "name": "7",
    },
    "Healthcare support occupations": {
        "codes": [
            "C24010e20",
            "C24010e56",
        ],
        "name": "8",
    },
    "Installation maintenance and repair occupations": {
        "codes": [
            "C24010e33",
            "C24010e69",
        ],
        "name": "9",
    },
    "Management business and financial occupations": {
        "codes": [
            "C24010e4",
            "C24010e40",
        ],
        "name": "10",
    },
    "Material moving occupations": {
        "codes": [
            "C24010e37",
            "C24010e73",
        ],
        "name": "11",
    },
    "Office and administrative support occupations": {
        "codes": [
            "C24010e29",
            "C24010e65",
        ],
        "name": "12",
    },
    "Personal care and service occupations": {
        "codes": [
            "C24010e26",
            "C24010e62",
        ],
        "name": "13",
    },
    "Production occupations": {
        "codes": [
            "C24010e35",
            "C24010e71",
        ],
        "name": "14",
    },
    "Protective service occupations": {
        "codes": [
            "C24010e21",
            "C24010e57",
        ],
        "name": "15",
    },
    "Sales and related occupations": {
        "codes": [
            "C24010e28",
            "C24010e64",
        ],
        "name": "16",
    },
    "Transportation occupations": {
        "codes": [
            "C24010e36",
            "C24010e72",
        ],
        "name": "17",
    },
}


race_query = query_distribution_per_nta(RACE, "B02")
school_enrollment = query_nta_statistic("ENROLLED_IN_SCHOOL")
school_enrolled_distribution = query_distribution_per_nta(EDUCATION, "B14")
occupation_distribution = query_distribution_per_nta(OCCUPATION, "C24")
