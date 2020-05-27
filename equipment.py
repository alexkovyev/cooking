"""Этот модуль содержит информацию об оборудовании"""


class Equipment(object):
    """Этот класс собирает информацию о оборудовании в текущий день
    Так выглядит информация о печах {12: {"oven_id": 12, "status": "free"},
                                    23: {"oven_id": 23, "status": "reserved", "dish": 213},
                                    1: {"oven_id": 1, "status": "occupied", "dish": 323}}
    oven_id:{}, во вложенном словаре oven_id нужен для функции fetch_free_oven
    """
    OVEN_STATUSES = ["broken", "not_available", "free", "reserved", "occupied"]

    def __init__(self, equipment_data):
        self.oven_available = equipment_data["ovens"]
        self.is_cut_station_ok = equipment_data["cut_station"]
        self.is_package_station_ok = equipment_data["package_station"]
        self.are_pick_up_points_ok = equipment_data["pick_up_points"]
        print("Данные о печах выглядят так", self.oven_available)

    def fetch_free_oven_list(self):
        """Этот метод получает список печей со статусом свободны"""
        free_oven = [oven for oven in self.oven_available.values() if oven["status"] == "free"]
        return free_oven

    def is_able_to_cook(self):
        """Определяет, можно ли готовить на основе того, исправно ли оборудование
        учитывает ли это, сколько печей свободно и если их 0.
        Если у нас 1 работающая печь киоск все равно работает, или нет?"""
        operate_oven_qt = self.fetch_free_oven_list()
        # как то проверяем, работают ли узлы выдачи
        equipment_status = True if self.is_cut_station_ok and \
                                   self.is_package_station_ok and \
                                   len(operate_oven_qt) > 1 \
            else False
        return equipment_status

    def get_first_free_oven(self):
        """Этот метод получает id печи, котрая последняя в списке свободных"""
        free_oven_list = self.fetch_free_oven_list()
        if free_oven_list:
            oven_id = free_oven_list.pop()["oven_id"]
            print("Выбрана печь", oven_id)
        else:
            print("Нет свободных печей")
            # нужно добавить обработчик что делать если блюда 2 а печь свободная 1 шт
        return oven_id

    def oven_reserve(self, dish_id):
        oven_id = self.get_first_free_oven()
        self.oven_available[oven_id]["status"] = "reserved"
        self.oven_available[oven_id]["dish"] = dish_id
        print("Статус изменен")
        return oven_id

    async def oven_broke_handler(self, event_data):
        """Это группа функций обрабатывает поломку печи.
        - поиск назначенных блюд на печь
        - замена печи на исправную
        - смена статуса, запись в БД ? Или это контролер делает?
        """
        print("Обрабатываем уведомление об оборудовании", event_data)
        oven_id = int(event_data["unit_name"])
        oven_status = event_data["status"]
        if self.oven_available[oven_id]["status"] == "reserved":
            print("Нужно переназначить печь")
            print("Перезначаем блюдо", self.oven_available[oven_id]["dish"])
            # new_oven_id = self.get_first_free_oven()
        self.oven_available[oven_id]["status"] = oven_status
        print("Мы обработали печь")
        print("Вот такие печи", self.oven_available)
