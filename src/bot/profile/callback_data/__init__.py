from .access_callback_data import AccessCallbackData
from .ask_new_fullname_validity_callback_data import AskNewFullnameValidityCallbackData
from .ask_updated_field_validity_callback_data import AskUpdatedFieldValidityCallbackData
from .choose_lesson_callback_data import ChooseLessonCallbackData
from .choose_role_callback_data import ChooseRoleCallbackData
from .get_back_to_profile_callback_data import GetBackToProfileCallbackData
from .profile_menu import ProfileUpdateCallbackData
from .profile_update_choice_callback_data import ProfileUpdateChoiceCallbackData
from .university_callback_data import UniversityCallbackData
from .update_attendance_callback_data import UpdateAttendanceCallbackData

__all__ = [
    "AskNewFullnameValidityCallbackData",
    "AccessCallbackData",
    "ChooseRoleCallbackData",
    "UniversityCallbackData",
    "ChooseLessonCallbackData",
    "UpdateAttendanceCallbackData",
    "AskUpdatedFieldValidityCallbackData",
    "ProfileUpdateChoiceCallbackData",
    "ProfileUpdateCallbackData",
    "GetBackToProfileCallbackData",
]
