from .check_group_exists_in_uni_query import CheckGroupExistsInUniQuery
from .find_group_by_name_and_alias_query import FindGroupByNameAndAliasQuery
from .find_group_headman_query import FindGroupHeadmanQuery
from .find_student_query import FindStudentByTelegramIdQuery
from .get_all_universities_query import GetAllUniversitiesQuery
from .get_edu_profile_info_query import GetEduProfileInfoQuery
from .get_students_from_group_query import GetStudentsInfoFromGroupQuery
from .get_university_by_alias_query import GetUniversityByAliasQuery
from .get_student_role_by_telegram_id_query import GetStudentRoleByTelegramIDQuery
from .get_all_and_active_students_count_query import GetAllAndActiveStudentsCountQuery

__all__ = [
    "FindStudentByTelegramIdQuery",
    "GetUniversityByAliasQuery",
    "GetAllUniversitiesQuery",
    "CheckGroupExistsInUniQuery",
    "FindGroupByNameAndAliasQuery",
    "FindGroupHeadmanQuery",
    "GetEduProfileInfoQuery",
    "GetStudentsInfoFromGroupQuery",
    "GetStudentRoleByTelegramIDQuery",
    "GetAllAndActiveStudentsCountQuery"
]
