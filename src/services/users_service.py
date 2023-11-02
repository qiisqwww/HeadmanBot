import datetime
import logging
import sqlite3 as sq

__all__ = [
    "UsersService",
]

from config import DB_PATH


class UsersService:
    _conn: sq.Connection

    def __init__(self) -> None:
        self._con = sq.connect(DB_PATH, check_same_thread=False)
        logging.info("connected to database")

    def create_table(self) -> None:
        cur = self._con.cursor()
        cur.execute(
            """CREATE TABLE  IF NOT EXISTS students (
    telegram_id  INTEGER,
    user_name    TEXT,
    name_surname TEXT,
    study_group  TEXT,
    is_headmen   INTEGER,
    attendance   TEXT,
    time         TEXT,
    was_polled   TEXT
);
"""
        )
        logging.info("table created")

    def is_registered(self, tg_id: int):
        cur = self._con.cursor()

        data = cur.execute("SELECT telegram_id FROM students")
        return tg_id in [user_id for (user_id,) in data]

    def is_headmen(self, tg_id: int):
        cur = self._con.cursor()

        data = cur.execute("SELECT telegram_id FROM students WHERE is_headmen = 1")
        return tg_id in [headmen_id for (headmen_id,) in data]

    def registration(self, tg_id: int, user_name: str, name_surname: str, study_group: str) -> bool:
        cur = self._con.cursor()

        try:
            cur.execute(
                "INSERT INTO students VALUES(?, ?, ?, ?, 0, 0, 0, 0)", (tg_id, user_name, name_surname, study_group)
            )  # Добавляем строчку в таблицу

            logging.info("user was registered in database")
            return True

        except:
            logging.warning("user wasn't registered in database (exception)")
            return False

    def set_status(self, tg_id: int) -> bool:
        cur = self._con.cursor()
        try:
            cur.execute("UPDATE students SET is_headmen = 1 WHERE telegram_id = ?", (tg_id,))
            logging.info("headmen status was set")
            return True
        except Exception:
            logging.warning("headmen status wasn't set (exception)")
            return False

    def get_groups(self):
        cur = self._con.cursor()
        return set(cur.execute("""SELECT study_group FROM students""").fetchall())

    def get_group_of_id_tg(self, tg_id: int):
        cur = self._con.cursor()

        data = cur.execute("SELECT study_group FROM students WHERE telegram_id = ?", (tg_id,)).fetchone()
        logging.info(data)
        return data[0]

    def get_user_of_group(self, group):
        cur = self._con.cursor()

        data = cur.execute("SELECT telegram_id FROM students WHERE study_group = ?", (group,)).fetchall()
        return [user[0] for user in data]

    def get_user_of_id_tg(self, tg_id: int):
        cur = self._con.cursor()

        data = cur.execute("SELECT * FROM students WHERE telegram_id = ?", (tg_id,)).fetchone()
        return data

    def change_attendance(self, tg_id: int, cb_data: str):
        new_attendance = ""
        cur = self._con.cursor()
        attendance = cur.execute("SELECT attendance FROM students WHERE telegram_id = ?", (tg_id,)).fetchone()[0]
        cb_data, info = cb_data.split(" ")
        match cb_data:
            case "start":
                new_attendance = "0" * int(info)
            case "none":
                new_attendance = "2" * len(attendance)
            case "all":
                new_attendance = "1" * len(attendance)
            case "lesson":
                day = list(attendance)
                day[int(info)] = "1"
                new_attendance = "".join(day)

        cur.execute("UPDATE students SET attendance = ? WHERE telegram_id = ?", (new_attendance, tg_id))

    def get_time(self, tg_id: int) -> datetime.datetime.time:
        cur = self._con.cursor()
        time = cur.execute("SELECT time FROM students WHERE telegram_id = ?", (tg_id,)).fetchone()
        return datetime.time(*map(int, time[0].split(":")))

    def set_time(self, time: str, group: str) -> None:
        cur = self._con.cursor()
        cur.execute("UPDATE students SET time = ? WHERE study_group = ?", (time, group))

    def get_lessons(self, tg_id: int) -> str:
        cur = self._con.cursor()
        lessons = cur.execute("SELECT attendance FROM students WHERE telegram_id = ?", (tg_id,)).fetchone()
        return lessons[0]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            logging.error(exc_type)
        self._con.commit()
        self._con.close()
        logging.info("disconnected from database")
