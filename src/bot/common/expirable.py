from datetime import date, datetime

from pydantic import BaseModel, Field

__all__ = [
    "Expirerable",
]


class Expirerable(BaseModel):
    created_at: date = Field(default_factory=lambda: datetime.today().date())
