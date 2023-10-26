from datetime import *
import requests


class API:
    def __init__(self):
        """
        Инициализация объекта API.

        Этот метод инициализирует объект API с начальной датой (self.start) и вызывает метод regenerate() для получения расписания.

        Параметры:
        - Нет параметров.

        Возвращает:
        - Ничего не возвращает.
        """
        self.start = datetime(2023, 8, 28)  # в начале следующего семестра эту дату нужно будет поменять

    def regenerate(self, group):
        """
        Получение расписания из API.

        Этот метод отправляет GET-запрос к API университета и сохраняет результат в self.req.

        Параметры:
        - Нет параметров.

        Возвращает:
        - Если запрос прошел успешно, возвращает True и 'ok'.
        - Если в запросе были ошибки, возвращает False и сообщение об ошибке.
        """
        self.req = requests.get(f"https://timetable.mirea.ru/api/groups/name/{group}").json()
        if 'errors' in self.req.keys():
            return False, self.req['errors']
        return True, 'ok'

    def get_today(self):
        """
        Получение расписания на текущий день.

        Этот метод анализирует расписание, полученное из API, и возвращает список занятий на текущий день.

        Параметры:
        - Нет параметров.

        Возвращает:
        - Список занятий на текущий день. Каждый элемент списка представляет собой список с названием дисциплины и временем начала занятия.
        """
        self.day = []
        now = datetime.now()
        week, now_day = (now - self.start).days // 7 + 1, now.weekday() + 1
        print(week)
        for lesson in self.req['lessons']:
            if week in lesson['weeks'] and now_day == lesson['weekday']:
                text = []
                count = 0
                for i in lesson['discipline']['name'].split():
                    if count + len(i) + 1 <= 17:
                        text.append(i)
                        count += len(i) + 1
                    else:
                        text.append('...')
                        break
                self.day.append([' '.join(text), ':'.join(lesson['calls']['time_start'].split(':')[:2])])

        seen = set()
        seen_add = seen.add
        self.day = [x for x in self.day if not (str(x) in seen or seen_add(str(x)))]

        return self.day