from typing import Union


def encode_list(param_list: list[str]) -> Union[str, tuple[str]]:
    """Sanitize a list of parameters for SQL injection."""
    num_params = len(param_list)
    if num_params > 1:
        return tuple(param_list)
    elif num_params == 1:
        return param_list[0]
    else:
        return ""


def encode_select(column: str, alias: str) -> str:
    """Econdes column and alias pair for use in a SELECT statement."""
    return f'"{column}" AS {alias}'


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
