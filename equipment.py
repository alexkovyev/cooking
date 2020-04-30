"""Этот модуль содержит информацию об оборудовании"""


class Equipment(object):
    """Этот класс собирает информацию о оборудовании в текущий день
    Так выглядит информация о печах {12: {"oven_id": 12, "status": "free"},
                                    23: {"oven_id": 23, "status": "reserved", "dish": 213},
                                    1: {"oven_id": 1, "status": "occupied", "dish": 323}}
    self.oven_id: это идентификатор физической печи, одинаоквый с контролерами
    """
    OVEN_STATUSES = ["broken", "not_available", "free", "reserved", "occupied"]

    def __init__(self, equipment_data):
        try:
            self.oven_available = equipment_data["ovens"]
            self.is_cut_station_ok = equipment_data["cut_station"]
            self.is_package_station_ok = equipment_data["package_station"]
            self.are_pick_up_points_ok = equipment_data["pick_up_points"]
            print("all good", self.oven_available)
        except KeyError:
            # тут ничего не проверяется, так как если в переменной пусто, то все равно исполнится код
            print("Ошибка, не найдена информация об оборудовании")

    # def update_oven_status(self, available_ovens_from_db):
    #     """Запрос к БД, проверяем не сломалась ли печь. Возвращает кортеж c доступными печами.
    #     Итерируем по всем печам, обновляем статус. Если статус печи "broken", "not_available, запускаем обработчик
    #     поломки печи"""
    #     # data_update()
    # этот код написан, если available_ovens список, если будет нужно подключаться к БД, переделать
    #     available_ovens_from_db = set(available_ovens_from_db)
    #     available_ovens_ids = set(i["oven_id"] for i in self.available_ovens)
    #     recently_broken_ovens = available_ovens_ids.difference(available_ovens_from_db)
    #     new_ovens = available_ovens_from_db.difference(available_ovens_ids)
    #     self.available_ovens.append({"oven_id": oven for oven in new_ovens})

    def fetch_free_oven(self):
        free_oven = [oven for oven in self.oven_available.values() if oven["status"] == "free"]
        return free_oven

    def is_able_to_cook(self):
        """Определяет, можно ли готовить на основе того, исправно ли оборудование
        учитывает ли это, сколько печей свободно и если их 0.
        Если у нас 1 работающая печь киоск все равно работает, или нет?"""
        operate_oven_qt = self.fetch_free_oven()
        # как то проверяем, работают ли узлы выдачи
        equipment_status = True if self.is_cut_station_ok and \
                                   self.is_package_station_ok and \
                                   len(operate_oven_qt) > 1 \
            else False
        return equipment_status

    def get_first_free_oven(self):
        """Этот метод получает id печи, котрая последняя в списке свободных"""
        free_oven_list = self.fetch_free_oven()
        print("Все доступные печи", free_oven_list)
        oven_id = free_oven_list.pop()["oven_id"]
        print("Выбрана печь", oven_id)
        return oven_id

    def oven_reserve(self):
        oven_id = self.get_first_free_oven()
        self.oven_available[oven_id]["status"] = "reserved"
        print("Статус изменен")
        # как связываем заказ и печь?
        # self.oven_avalable[oven_id]["dish"] = 123
        return oven_id

    def oven_broke_handler(self, oven_alarm_id):
        """Это группа функций обрабатывает поломку печи.
        - поиск назначенных блюд на печь
        - замена печи на исправную
        - смена статуса, запись в БД ? Или это контролер делает?
        """
        print("Обрабатываем сломанную печь", oven_alarm_id)
        if self.oven_available[oven_alarm_id]["status"] == "reserved":
            print("Нужно переназначить печь")
            # new_oven_id = self.get_first_free_oven()
        self.oven_available[oven_alarm_id]["status"] = "broken"
        print("Мы обработали печь")
        print("Вот такие печи", self.oven_available)
