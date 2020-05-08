"""Тут собраны служебные функции"""


def go_to_db_get_data():
    # запрос к БД если нужно контроллерам для проверки работоспособности оборудования
    equipment_data = ('супер важная информация об оборудовании', 'из БД')
    return equipment_data


def start_testing():
    """Тут вызываем методы контролеров по тестированию оборудования"""
    equipment_data = go_to_db_get_data()
    # вызывается какой то супер метод контроллеров на проверку, возвращает status и dict с данными об оборудовании
    is_equipment_ok = True
    equipment_data = {"ovens": {i: {"oven_id": i, "status": "free"} for i in range(1, 22)},
                      "cut_station": True,
                      "package_station": True,
                      "pick_up_points":{1: True,
                                        2: True,
                                        3: True}
                      }
    print("Оборудование протестировано, исправно")
    return is_equipment_ok, equipment_data


def parse_recipes(recipe_data):
    """Парсит все рецепты в директории и возвращает словарь вида: описать"""
    recipes = recipe_data
    return recipes