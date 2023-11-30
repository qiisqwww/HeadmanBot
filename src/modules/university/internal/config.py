from src.modules.university.api.enums import UniversityAlias

__all__ = [
    "UNIVERSITIES_LIST",
]

UNIVERSITIES_LIST: list[tuple[str, UniversityAlias]] = [
    ("РТУ МИРЭА", UniversityAlias.MIREA),
    ("МГТУ им. Н.Э. Баумана", UniversityAlias.BMSTU),
]
