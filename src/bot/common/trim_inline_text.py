__all__ = [
    "trim_inline_text",
]


def trim_inline_text(text: str) -> str:
    MAX_STR_SIZE: int = 35
    if len(text) <= MAX_STR_SIZE:
        return text
    return text[: MAX_STR_SIZE - 3] + "..."
