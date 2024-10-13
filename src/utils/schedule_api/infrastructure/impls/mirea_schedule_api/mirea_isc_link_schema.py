from pydantic import BaseModel
from pydantic_core import Url

__all__ = [
    "MireaIscLinkSchema",
    "IscLinkItem",
]


class IscLinkItem(BaseModel):
    iCalLink: Url # noqa: N815
    targetTitle: str # noqa: N815


class MireaIscLinkSchema(BaseModel):
    data: list[IscLinkItem]
