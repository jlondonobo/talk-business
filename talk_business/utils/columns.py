COLUMNS = {
    "PER_CAPITA_INCOME": {
        "type": "METRIC",
        "label": "Income",
        "table": "B19",
        "code": "B19301e1",
        "total": "B01003e1", 
    },
    "MEDIAN_GROSS_RENT": {
        "type": "METRIC",
        "label": "Rent",
        "table": "B25",
        "code": "B25064e1",
        "total": "B25054e1"
    },
    "HOUSEHOLD_SIZE": {
        "type": "METRIC",
        "label": "People per household",
        "table": "B25",
        "code": "B25010e1",
        "total": "B25003e1",
    },
    "TOTAL_POPULATION": {
        "type": "COUNT_METRIC",
        "label": "Total population",
        "table": "B01",
        "code": "B01003e1",
    },
    "MEDIAN_AGE": {
        "type": "SEGMENTED_METRIC",
        "label": "Mean age",
        "table": "B01",
        "total": "B01002e1",
        "segments": {
            "MALE": "B01002e2",
            "FEMALE": "B01002e3",    
        }
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
        "label": "Available properties",
        "table": "B25",
        "total": "B25002e1",
        "segments": {
            "OCCUPIED": "B25002e2",
            "VACANT": "B25002e3",
        }
    }
}


def preprocess_column_group(
    column_groups: dict[str, dict[str, dict[str, str]]]
) -> list[dict[str, str]]:
    """Preprocesses a column group for use in a SELECT statement."""
    columns_sequence = []
    for group, columns in column_groups.items():
        for column, variations in columns.items():
            for variation, code in variations.items():
                columns_sequence.append(
                    {"column": code, "alias": f"{column}-{variation}"}
                )

    return columns_sequence


def encode_columns(column_group: dict[str, dict[str, dict[str, str]]]) -> str:
    preprocessed_columns = preprocess_column_group(column_group)
    return ", ".join([encode_select(**column) for column in preprocessed_columns])
