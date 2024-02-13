from typing import Any

from jinja2 import Template

__all__ = [
    "render_template",
]


def render_template(template: str, **kwargs: Any) -> str:
    res: str = Template(template, autoescape=True, trim_blocks=True).render(**kwargs)
    return res
