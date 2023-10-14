__all__ = ["START_MESSAGE","REG_MESSAGE_1", "REG_MESSAGE_2",
           "SUCCESFULLY_REG_MESSAGE", "UNSUCCESFULLY_REG_MESSAGE", "PASS_ASK_MESSAGE",
           "STAROSTA_REG_MESSAGE","UNSUCCESFULL_STAROSTA_REG_MESSAGE", "ALREADY_HEADMAN_MESSAGE",
           "MUST_BE_REG_MESSAGE", "MUST_BE_HEADMEN_MESSAGE", "ALREADY_REGISTERED_MESSAGE"]

START_MESSAGE = """
Привет! Я - твоя староста!"""

REG_MESSAGE_1 = """
Для начала, напомни, как тебя зовут?"""

REG_MESSAGE_2 = """
Из какой ты группы? (!Вводить строго в формате ХХХХ-ХХ-ХХ!)"""

SUCCESFULLY_REG_MESSAGE = """
Ты был успешно зарегестрирован в системе!"""

UNSUCCESFULLY_REG_MESSAGE = """
Ой! Из-за какой-то ошибки я не смог внести тебя в систему, попробуй снова!"""

ALREADY_REGISTERED_MESSAGE = """
Ты уже зарегестрирован в системе!"""

PASS_ASK_MESSAGE = """
Введите пароль старосты"""

STAROSTA_REG_MESSAGE = """
Вы были успешно зарегестрированы как староста!"""

UNSUCCESFULL_STAROSTA_REG_MESSAGE = """
Ой! Из-за какой-то ошибки я не смог зарегестрировать тебя, как старосту!"""

ALREADY_HEADMAN_MESSAGE = """
Вы и так зарегестрированы как староста!"""

MUST_BE_REG_MESSAGE = """
Для выполнения данной команды вы должны быть зарегестрированы! (/start)"""

MUST_BE_HEADMEN_MESSAGE = """
Для выполнения данной команды вы должны быть старостой.
Для регистрации как страоста - /set_headmen"""