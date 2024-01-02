from .check_group_exists_in_uni_query import CheckGroupExistsInUniQuery
from .find_group_headman_query import FindGroupHeadmanQuery
from .find_student_query import FindStudentQuery
from .get_all_universities_query import GetAllUniversitiesQuery
from .get_university_by_alias_query import GetUniversityByAliasQuery
from .is_group_registered_query import IsGroupRegisteredQuery

__all__ = [
    "FindStudentQuery",
    "GetUniversityByAliasQuery",
    "GetAllUniversitiesQuery",
    "CheckGroupExistsInUniQuery",
    "IsGroupRegisteredQuery",
    "FindGroupHeadmanQuery",
]
