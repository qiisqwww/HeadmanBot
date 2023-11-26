__all__ = [
    "is_number",
]


def is_number(num: str) -> bool:
    if num.startswith("-"):
        num = num[1:]

    return num.isdigit()
