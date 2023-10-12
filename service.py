import sqlite3 as sq
import logging

__all__ = ["UsersService"]

class UsersService:
    _conn: sq.Connection

    def __init__(self) -> None:
        self._con = sq.connect(r'database\bot.db', check_same_thread=False)
        logging.info('connected to database')

    def create_table(self) -> None:
        cur = self._con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS students(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        telegram_id INTEGER,
                        user_name TEXT,
                        name_surname TEXT,
                        study_group TEXT,
                        is_headman TEXT)""")
        logging.info("table created")

    def is_registered(self,tg_id : int):
        cur = self._con.cursor()

        data = cur.execute("SELECT telegram_id FROM students")
        return tg_id in [user_id for (user_id, ) in data]

    def registration(self,tg_id : int, user_name : str, name_surname : str, study_group : str) -> bool:
        cur = self._con.cursor()

        try:
            count_id = cur.execute("""SELECT COUNT(*) FROM students""").fetchone()[0]  # Создаем id пользователя с помощью кол-ва участников
            cur.execute("INSERT INTO students VALUES(?, ?, ?, ?, ?, 0)", (count_id, tg_id, user_name, name_surname, study_group))  # Добавляем строчку в таблицу

            logging.info("user was registered in database")
            return True
        except:
            logging.warning("user wasn't registered in database (exception)")
            return False

    def set_status(self, telegram_id) -> bool:
        cur = self._con.cursor()
        try :
            cur.execute(f'''UPDATE students SET is_headmen="{1}" WHERE name = "{telegram_id}"''')
            logging.info("headmen status was set")
        except:
            logging.warning("headmen status wasn't set (exception)")
            return False


    def get_groups(self):
        cur = self._con.cursor()
        return set(cur.execute("""SELECT study_group FROM students""").fetchall())

    def get_group_of_id_tg(self, tg_id: int):
        cur = self._con.cursor()

        data = cur.execute(f'SELECT study_group FROM students WHERE telegram_id = "{tg_id}"').fetchone()
        return data[0]

    def get_user_of_group(self, group):
        cur = self._con.cursor()
        return cur.execute(f'''SELECT telegram_id FROM students WHERE study_group = "{group}"''').fetchall()
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
           print(exc_type, exc_value, tb)
        self._con.commit()
        self._con.close()
        logging.info('disconnected from database')

if __name__ == '__main__':
    with UsersService() as con:
        print(con.get_user_of_group('ИКБО-20-23'))