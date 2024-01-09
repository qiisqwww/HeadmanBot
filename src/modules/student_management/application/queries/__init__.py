from .check_group_exists_in_uni_query import CheckGroupExistsInUniQuery
from .find_group_by_name_and_alias_query import FindGroupByNameAndAliasQuery
from .find_group_headman_query import FindGroupHeadmanQuery
from .find_student_query import FindStudentByTelegramIdQuery
from .get_all_universities_query import GetAllUniversitiesQuery
from .get_edu_profile_info_query import GetEduProfileInfoQuery
from .get_university_by_alias_query import GetUniversityByAliasQuery

__all__ = [
    "FindStudentByTelegramIdQuery",
    "GetUniversityByAliasQuery",
    "GetAllUniversitiesQuery",
    "CheckGroupExistsInUniQuery",
    "FindGroupByNameAndAliasQuery",
    "FindGroupHeadmanQuery",
    "GetEduProfileInfoQuery",
]
