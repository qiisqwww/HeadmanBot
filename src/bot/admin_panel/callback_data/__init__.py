from .cancel_action_callback_data import CancelActionCallbackData
from .delete_by_name_and_group_callback_data import DeleteByNameAndGroupCallbackData
from .delete_by_tg_id_callback_data import DeleteByTGIDCallbackData
from .delete_user_callback_data import DeleteStudentCallbackData
from .groups_list_callback_data import GroupsListCallbackData
from .make_new_admin_callback_data import MakeNewAdminCallbackData
from .students_count_callback_data import StudentsCountCallbackData
from .change_group_callback_data import ChangeGroupCallbackData
from .choose_uni_callback_data import ChooseUniCallbackData

__all__ = [
    "GroupsListCallbackData",
    "MakeNewAdminCallbackData",
    "StudentsCountCallbackData",
    "DeleteStudentCallbackData",
    "DeleteByTGIDCallbackData",
    "DeleteByNameAndGroupCallbackData",
    "CancelActionCallbackData",
    "ChooseUniCallbackData",
    "ChangeGroupCallbackData",
]
