from aiogram import Router, F
from buttons import load_attendance_kb
from work_api import API
from service import UsersService
from middlewares import HeadmenCommandsMiddleware


router = Router()

router.message.middleware(HeadmenCommandsMiddleware())
router.message.filter(F.chat.type.in_({"private"}))  # Бот будет отвечать только в личных сообщениях

api = API()


async def job(k, bot):  # ругается, если убрать k
    with UsersService() as con:
        groups = con.get_groups()
        print(groups)
        for group in groups:
            api.regenerate(group[0])
            day = api.get_today()
            seen = set()
            seen_add = seen.add
            day = [x for x in day if not (str(x) in seen or seen_add(str(x)))]
            for Id in con.get_user_of_group(group[0]):
                con.change_attendance(Id[0], f'start {len(day)}')

                print(con.get_user_of_group(group[0]), group)
                await bot(Id[0], f'Привет, ты будешь на паре', reply_markup=load_attendance_kb(day))
