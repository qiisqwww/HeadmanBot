__all__ = [
    "is_number",
    "is_valid_name_len",
    "is_valid_surname_len",
]


def is_number(num: str) -> bool:
    if num.startswith("-"):
        num = num[1:]

    return num.isdigit()


def is_valid_name_len(name: str) -> bool:
    return len(name) <= 255


def is_valid_surname_len(surname: str) -> bool:
    return len(surname) <= 255
