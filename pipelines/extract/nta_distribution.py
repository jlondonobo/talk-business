from typing import Any, Union

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


def format_horizontal_sum(columns: list[str]) -> str:
    """Returns a SELECT statement for a SUM."""
    return " + ".join([f'"{column}"' for column in columns])


def format_vertical_sum_with_horizontal_sum(
    columns: list[str],
    alias: Union[str, int],
) -> str:
    """Returns a SELECT statement for a SUM."""
    horizontal_sum = format_horizontal_sum(columns)
    return f'SUM({horizontal_sum}) AS "{alias}"'


def format_feature_groups(feature_groups: dict[str, Any]) -> str:
    """Returns a SELECT statement for age groups."""
    select = []
    for _group, data in feature_groups.items():
        select.append(
            format_vertical_sum_with_horizontal_sum(data["codes"], data["alias"])
        )
    return ", ".join(select)


def query_nta_feature_distribution(feature_groups: dict[str, Any]) -> str:
    return f"""
        SELECT
            COUNTY,
            NTACODE,
        {format_feature_groups(feature_groups["columns"])}
        FROM OPENCENSUSDATA.PUBLIC."2020_CBG_{feature_groups["table"]}"
        LEFT JOIN OPENCENSUSDATA.PUBLIC."2020_CBG_GEOMETRY_WKT" as c USING (census_block_group)
        LEFT JOIN PERSONAL.PUBLIC.NTA_MAPPER AS nta ON nta.CT2020=c.tract_code AND nta.COUNTYFIPS=c.COUNTY_FIPS
        WHERE STATE_FIPS = 36 AND COUNTY IN ('New York County', 'Queens County', 'Kings County', 'Richmond County', 'Bronx County')
        GROUP BY (COUNTY, NTACODE);
    """


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
