from typing import Final

__all__ = [
    "trim_inline_text",
]


MAX_STR_SIZE: Final[int] = 35


def trim_inline_text(text: str) -> str:
    if len(text) <= MAX_STR_SIZE:
        return text
    return text[: MAX_STR_SIZE - 3] + "..."
