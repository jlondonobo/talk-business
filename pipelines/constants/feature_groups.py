COLUMNS = {
    "PER_CAPITA_INCOME": {
        "type": "METRIC",
        "label": "Per capita income (12 months)",
        "table": "B19",
        "code": "B19301e1",
        "total": "B01003e1",
    },
    "MEDIAN_GROSS_RENT": {
        "type": "METRIC",
        "label": "Median gross rent",
        "table": "B25",
        "code": "B25064e1",
        "total": "B25054e1",
    },
    "HOUSEHOLD_SIZE": {
        "type": "METRIC",
        "label": "Household size",
        "table": "B25",
        "code": "B25010e1",
        "total": "B25003e1",
    },
    "TOTAL_POPULATION": {
        "type": "COUNT_METRIC",
        "label": "Population",
        "table": "B01",
        "code": "B01003e1",
    },
    "MEDIAN_AGE": {
        "type": "SEGMENTED_METRIC",
        "label": "Median age",
        "table": "B01",
        "total": "B01002e1",
        "segments": {
            "MALE": "B01002e2",
            "FEMALE": "B01002e3",
        },
    },
    "RACE": {
        "type": "SEGMENTED_COUNT",
        "label": "Race",
        "table": "B02",
        "total": "B02001e1",
        "segments": {
            "WHITE": "B02001e2",
            "BLACK_OR_AFRICAN_AMERICAN": "B02001e3",
            "AMERICAN_INDIAN_AND_ALASKA_NATIVE": "B02001e4",
            "ASIAN": "B02001e5",
            "NATIVE_HAWAIIAN_AND_OTHER_PACIFIC_ISLANDER_ALONE": "B02001e6",
            "SOME_OTHER_RACE": "B02001e7",
            "TWO_OR_MORE_RACES": "B02001e8",
        },
    },
    "OCCUPANCY_STATUS": {
        "type": "SEGMENTED_COUNT",
        "label": "Dwelling occupancy status",
        "table": "B25",
        "total": "B25002e1",
        "segments": {
            "OCCUPIED": "B25002e2",
            "VACANT": "B25002e3",
        },
    },
}

COUNT_GROUPS = {
    "AGE_GROUPS": {
        "table": "B01",
        "columns": {
            "Under 5 years": {
                "codes": [
                    "B01001e27",
                    "B01001e3",
                ],
                "alias": "00-05",
            },
            "5 to 9 years": {
                "codes": [
                    "B01001e28",
                    "B01001e4",
                ],
                "alias": "05-10",
            },
            "10 to 14 years": {
                "codes": [
                    "B01001e29",
                    "B01001e5",
                ],
                "alias": "10-14",
            },
            "15 to 19 years": {
                "codes": [
                    "B01001e31",
                    "B01001e7",
                    "B01001e30",
                    "B01001e6",
                ],
                "alias": "15-19",
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
                "alias": "20-24",
            },
            "25 to 29 years": {
                "codes": [
                    "B01001e11",
                    "B01001e35",
                ],
                "alias": "25-29",
            },
            "30 to 34 years": {
                "codes": [
                    "B01001e12",
                    "B01001e36",
                ],
                "alias": "30-34",
            },
            "35 to 39 years": {
                "codes": [
                    "B01001e13",
                    "B01001e37",
                ],
                "alias": "35-39",
            },
            "40 to 44 years": {
                "codes": [
                    "B01001e14",
                    "B01001e38",
                ],
                "alias": "40-44",
            },
            "45 to 49 years": {
                "codes": [
                    "B01001e15",
                    "B01001e39",
                ],
                "alias": "45-49",
            },
            "50 to 54 years": {
                "codes": [
                    "B01001e16",
                    "B01001e40",
                ],
                "alias": "50-54",
            },
            "55 to 59 years": {
                "codes": [
                    "B01001e17",
                    "B01001e41",
                ],
                "alias": "55-59",
            },
            "60 to 64 years": {
                "codes": [
                    "B01001e19",
                    "B01001e43",
                    "B01001e18",
                    "B01001e42",
                ],
                "alias": "60-64",
            },
            "65 to 69 years": {
                "codes": [
                    "B01001e21",
                    "B01001e45",
                    "B01001e20",
                    "B01001e44",
                ],
                "alias": "65-69",
            },
            "70 to 74 years": {
                "codes": [
                    "B01001e22",
                    "B01001e46",
                ],
                "alias": "70-74",
            },
            "75 to 79 years": {
                "codes": [
                    "B01001e23",
                    "B01001e47",
                ],
                "alias": "75-79",
            },
            "80 to 84 years": {
                "codes": [
                    "B01001e24",
                    "B01001e48",
                ],
                "alias": "80-84",
            },
            "85 years and over": {
                "codes": [
                    "B01001e25",
                    "B01001e49",
                ],
                "alias": "85-100",
            },
        },
    },
    "RENT_GROUPS": {
        "table": "B25",
        "columns": {
            "Less than $100": {"codes": ["B25063e3"], "alias": "0-100", "numeric": 0},
            "$100 to $149": {"codes": ["B25063e4"], "alias": "100-149", "numeric": 100},
            "$150 to $199": {"codes": ["B25063e5"], "alias": "150-199", "numeric": 150},
            "$200 to $249": {"codes": ["B25063e6"], "alias": "200-249", "numeric": 200},
            "$250 to $299": {"codes": ["B25063e7"], "alias": "250-299", "numeric": 250},
            "$300 to $349": {"codes": ["B25063e8"], "alias": "300-349", "numeric": 300},
            "$350 to $399": {"codes": ["B25063e9"], "alias": "350-399", "numeric": 350},
            "$400 to $449": {
                "codes": ["B25063e10"],
                "alias": "400-449",
                "numeric": 400,
            },
            "$450 to $499": {
                "codes": ["B25063e11"],
                "alias": "450-499",
                "numeric": 450,
            },
            "$500 to $549": {
                "codes": ["B25063e12"],
                "alias": "500-549",
                "numeric": 500,
            },
            "$550 to $599": {
                "codes": ["B25063e13"],
                "alias": "550-599",
                "numeric": 550,
            },
            "$600 to $649": {
                "codes": ["B25063e14"],
                "alias": "600-649",
                "numeric": 600,
            },
            "$650 to $699": {
                "codes": ["B25063e15"],
                "alias": "650-699",
                "numeric": 650,
            },
            "$700 to $749": {
                "codes": ["B25063e16"],
                "alias": "700-749",
                "numeric": 700,
            },
            "$750 to $799": {
                "codes": ["B25063e17"],
                "alias": "750-799",
                "numeric": 750,
            },
            "$800 to $899": {
                "codes": ["B25063e18"],
                "alias": "800-899",
                "numeric": 800,
            },
            "$900 to $999": {
                "codes": ["B25063e19"],
                "alias": "900-999",
                "numeric": 900,
            },
            "$1 000 to $1 249": {
                "codes": ["B25063e20"],
                "alias": "1000-1249",
                "numeric": 1000,
            },
            "$1 250 to $1 499": {
                "codes": ["B25063e21"],
                "alias": "1250-1499",
                "numeric": 1250,
            },
            "$1 500 to $1 999": {
                "codes": ["B25063e22"],
                "alias": "1500-1999",
                "numeric": 1500,
            },
            "$2 000 to $2 499": {
                "codes": ["B25063e23"],
                "alias": "2000-2499",
                "numeric": 2000,
            },
            "$2 500 to $2 999": {
                "codes": ["B25063e24"],
                "alias": "2500-2999",
                "numeric": 2500,
            },
            "$3 000 to $3 499": {
                "codes": ["B25063e25"],
                "alias": "3000-3499",
                "numeric": 3000,
            },
            "$3 500 or more": {
                "codes": ["B25063e26"],
                "alias": "3500-",
                "numeric": 3500,
            },
        },
    },
    "FAMILY_INCOME_GROUPS": {
        "table": "B19",
        "columns": {
            "Less than $10 000": {
                "codes": ["B19001e2"],
                "alias": "0-10000",
                "numeric": 0,
            },
            "$10 000 to $14 999": {
                "codes": ["B19001e3"],
                "alias": "10000-14999",
                "numeric": 10000,
            },
            "$15 000 to $19 999": {
                "codes": ["B19001e4"],
                "alias": "15000-19999",
                "numeric": 15000,
            },
            "$20 000 to $24 999": {
                "codes": ["B19001e5"],
                "alias": "20000-24999",
                "numeric": 20000,
            },
            "$25 000 to $29 999": {
                "codes": ["B19001e6"],
                "alias": "25000-29999",
                "numeric": 25000,
            },
            "$30 000 to $34 999": {
                "codes": ["B19001e7"],
                "alias": "30000-34999",
                "numeric": 30000,
            },
            "$35 000 to $39 999": {
                "codes": ["B19001e8"],
                "alias": "35000-39999",
                "numeric": 35000,
            },
            "$40 000 to $44 999": {
                "codes": ["B19001e9"],
                "alias": "40000-44999",
                "numeric": 40000,
            },
            "$45 000 to $49 999": {
                "codes": ["B19001e10"],
                "alias": "45000-49999",
                "numeric": 45000,
            },
            "$50 000 to $59 999": {
                "codes": ["B19001e11"],
                "alias": "50000-59999",
                "numeric": 50000,
            },
            "$60 000 to $74 999": {
                "codes": ["B19001e12"],
                "alias": "60000-74999",
                "numeric": 60000,
            },
            "$75 000 to $99 999": {
                "codes": ["B19001e13"],
                "alias": "75000-99999",
                "numeric": 75000,
            },
            "$100 000 to $124 999": {
                "codes": ["B19001e14"],
                "alias": "100000-124999",
                "numeric": 100000,
            },
            "$125 000 to $149 999": {
                "codes": ["B19001e15"],
                "alias": "125000-149999",
                "numeric": 125000,
            },
            "$150 000 to $199 999": {
                "codes": ["B19001e16"],
                "alias": "150000-199999",
                "numeric": 150000,
            },
            "$200 000 or more": {
                "codes": ["B19001e17"],
                "alias": "200000-",
                "numeric": 200000,
            },
        },
    },
    "RACE_GROUPS": {
        "table": "B02",
        "columns": {
            key: {"codes": [value], "alias": key}
            for key, value in COLUMNS["RACE"]["segments"].items()
        },
    },
    "ENROLLMENT_GROUPS": {
        "table": "B14",
        "columns": {
            "ELEMENTARY_SCHOOL": {
                "codes": [
                    "B14007e4",
                    "B14007e5",
                    "B14007e6",
                    "B14007e7",
                    "B14007e8",
                    "B14007e9",
                ],
                "alias": "ELEMENTARY_SCHOOL",
            },
            "HIGHER_EDUCATION": {
                "codes": ["B14007e17", "B14007e18", "B14007e3"],
                "alias": "HIGHER_EDUCATION",
            },
            "HIGH_SCHOOL": {
                "codes": ["B14007e13", "B14007e14", "B14007e15", "B14007e16"],
                "alias": "HIGH_SCHOOL",
            },
            "MIDDLE_SCHOOL": {
                "codes": ["B14007e10", "B14007e11", "B14007e12"],
                "alias": "MIDDLE_SCHOOL",
            },
        },
    },
    "OCCUPATION_GROUPS": {
        "table": "C24",
        "columns": {
            "Building and grounds cleaning and maintenance occupations": {
                "codes": [
                    "C24010e25",
                    "C24010e61",
                ],
                "alias": "1",
            },
            "Computer engineering and science occupations": {
                "codes": [
                    "C24010e43",
                    "C24010e7",
                ],
                "alias": "2",
            },
            "Construction and extraction occupations": {
                "codes": [
                    "C24010e32",
                    "C24010e68",
                ],
                "alias": "3",
            },
            "Education legal community service arts and media occupations": {
                "codes": [
                    "C24010e11",
                    "C24010e47",
                ],
                "alias": "4",
            },
            "Farming fishing and forestry occupations": {
                "codes": [
                    "C24010e31",
                    "C24010e67",
                ],
                "alias": "5",
            },
            "Food preparation and serving related occupations": {
                "codes": [
                    "C24010e24",
                    "C24010e60",
                ],
                "alias": "6",
            },
            "Healthcare practitioners and technical occupations": {
                "codes": [
                    "C24010e16",
                    "C24010e52",
                ],
                "alias": "7",
            },
            "Healthcare support occupations": {
                "codes": [
                    "C24010e20",
                    "C24010e56",
                ],
                "alias": "8",
            },
            "Installation maintenance and repair occupations": {
                "codes": [
                    "C24010e33",
                    "C24010e69",
                ],
                "alias": "9",
            },
            "Management business and financial occupations": {
                "codes": [
                    "C24010e4",
                    "C24010e40",
                ],
                "alias": "10",
            },
            "Material moving occupations": {
                "codes": [
                    "C24010e37",
                    "C24010e73",
                ],
                "alias": "11",
            },
            "Office and administrative support occupations": {
                "codes": [
                    "C24010e29",
                    "C24010e65",
                ],
                "alias": "12",
            },
            "Personal care and service occupations": {
                "codes": [
                    "C24010e26",
                    "C24010e62",
                ],
                "alias": "13",
            },
            "Production occupations": {
                "codes": [
                    "C24010e35",
                    "C24010e71",
                ],
                "alias": "14",
            },
            "Protective service occupations": {
                "codes": [
                    "C24010e21",
                    "C24010e57",
                ],
                "alias": "15",
            },
            "Sales and related occupations": {
                "codes": [
                    "C24010e28",
                    "C24010e64",
                ],
                "alias": "16",
            },
            "Transportation occupations": {
                "codes": [
                    "C24010e36",
                    "C24010e72",
                ],
                "alias": "17",
            },
        },
    },
}
