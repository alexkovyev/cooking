"""Пока тут собрана информация о рецепте.
Каждый рецепт это исполняемый Python код (?)
"""

import RBA
import Controllers


class GetDough(object):
    """This class represents what should be done to take a vane from oven and get a dough to cut station"""

    def __init__(self):
        # сомневаюсь насчет переменных? по идее они должн быть после сортировки
        self.plan_duration = 300

    def move_to_oven(self, oven_id):
        """Этот метод описывает движение от текущего места (мы отслеживаем, где сейчас находится манипулятор? Как? до
        назнаечнной печи. Исполнитель - RBA. Какую обратную связь от RBA получаем? как обрабатывает исключение"""
        # Нужно ли тут время и какие то координаты?
        result = RBA.move_to_oven(oven_id)
        if result:
            # что возвращаем?
            return
        else:
            # эти ошибк описаны в библиотеке RBA, логируем? что делаем?
            raise RBA.Exceptions.movement_error

    def set_position_by_oven(self):
        """Этот метод отдает команду позиционирования перед печью """
        pass

    def get_vane(self):
        """Тут описывается движение возьми лопаткку. """
        pass

    def get_out_the_oven(self):
        """Тут описывается выезд из печи. Нужно ли делать отдельную команду?"""
        pass

    def move_to_dough_station(self, dough_station_number):
        """Запускает движение к станции теста"""
        pass

    def get_dough(self, dough_station_number):
        """отдает команду контролеру получить тесто"""
        Controllers.give_dough(dough_station_number)
        pass

    def control_dough_position(self):
        """отдаем команду на поправление теста"""
        pass

    def move_to_cut_station(self):
        """отдает команду на движение от станции теста на станцию нарезки"""
        pass

    def set_position_by_cut_station(self):
        """это типовая команда?"""
        pass

    def get_in_cut_station(self):
        """Заезжаем в станцию нарезки"""
        pass

    def free_capture(self):
        """Освободить захват"""
        pass



class BaseRecipe(GetDough):
    """This class represents base recipe"""
    pass


