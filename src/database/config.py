__all__ = [
    "DATABASE_URL",
]

from ..config import DB_HOST, DB_NAME, DB_PASS, DB_USER

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
