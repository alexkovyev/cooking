"""Этот модуль содержит информмацию об оборудовании"""


class Oven(object):
    """Этот класс собирает информацию о печах в текущий день
    self.oven_id: это идентификатор физической печи, одинаоквый с контролерами
    ПРИДУМАТЬ как хранить информацию о том, что печь на такое то время назначен заказ
    Как передается температура и время нагрева и прогрева?
    """
    OVEN_STATUSES = ["broken", "not_available", "free", "occupied"]

    def __init__(self):
        self.oven_id = int
        self.status = str
        self.busy_time = {"busy_time": ["start_time", "stop_time"],
                          "dish_id": "dish_refid"}

    def oven_busy(self):
        """Функция данные о занятости печи self.busy_time"""
        pass

    def oven_broke_handler(self):
        """Это группа функций обрабатывает поломку печи.
        - поиск назначенных блюд на печь
        - замена печи на исправную
        - смена статуса, запись в БД ? Или это контролер делает?
        """
        pass