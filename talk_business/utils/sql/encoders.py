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

