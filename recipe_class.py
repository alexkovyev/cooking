"""Пока тут собрана информация о рецепте."""
import asyncio
import time
import random

from RBA import RBA
from controllers import Controllers


class ConfigMixin(object):
    CUT_STATION_ID = 1
    CAPTURE_STATION = 2
    MOVE_TO_CAPTURE_STATION_TIME = 5
    CHANGE_CAPTURE_TIME = 2
    PRODUCT_CAPTURE_ID = 1


class GetDough(ConfigMixin):
    """This class represents what should be done to take a vane from oven and get a dough to cut station"""

    def __init__(self):
        super().__init__()
        self.duration = 30
        self.result = False

    async def move_to_oven(self):
        """Эта функция описывает движение до назначенной печи. Исполнитель - RBA."""

        current_destination = await RBA.get_current_destination()
        forward_destination = self.oven_unit

        duration = await RBA.calculate_time(current_destination, forward_destination)

        self.result = await RBA.move_to_position(forward_destination, duration)
        if self.result:
            print("RBA успешно подъехал к печи")
            await self.get_vane_from_oven(current_destination=forward_destination)
        else:
            print("Ошибка подъезда")
        return self.result

    async def get_vane_from_oven(self, current_destination):
        """Этот метод запускает группу атомарных действий RA по захвату лопатки из печи"""
        CHAIN_ID = 2

        launch_params = {"name": "get_vane_from_oven",
                         "place": self.oven_unit}

        self.result = await RBA.atomic(**launch_params)
        if self.result:
            print("RBA взял лопатку")
            await self.move_to_dough_station(current_destination)
        else:
            print("Ошибка взятия лопатки")
        return self.result

    async def move_to_dough_station(self, current_destination):
        """Запускает движение к станции теста"""

        current_destination = current_destination
        forward_destination = self.dough.halfstuff_cell

        duration = await RBA.calculate_time(current_destination, forward_destination)

        print("поехали к станции теста")
        self.result = await RBA.move_to_position(forward_destination, duration)

        if self.result:
            print("приехали к станции теста")
            await self.controllers_get_dough(current_destination=forward_destination)
        else:
            print("ошибка подъезда на станцию теста")
        return self.result

    async def controllers_get_dough(self, current_destination):
        """отдает команду контролеру получить тесто"""

        print("берем тесто у контрллеров")
        dough_point = self.dough.halfstuff_cell
        self.result = await Controllers.give_dough(dough_point)
        if self.result:
            print("взяли тесто у контроллеров")
            await self.control_dough_position(current_destination)
        else:
            print("Ошибка получения теста у контроллеров")
        # запускает метод списать п\ф
        return self.result

    async def control_dough_position(self, current_destination):
        """отдаем команду на поправление теста"""
        print("поправляем тесто")

        launch_params = {"name": "get_dough",
                         "place": self.dough.halfstuff_cell}
        self.result = await RBA.atomic(**launch_params)
        if self.result:
            print("успешно поправили тесто")
            await self.move_to_cut_station(current_destination)
        else:
            print("Ошибка поправления теста")
        return self.result

    async def move_to_cut_station(self, current_destination):
        """отдает команду на движение от станции теста на станцию нарезки"""
        print("едем к станции нарезки")

        current_destination = current_destination
        forward_destination = self.CUT_STATION_ID

        duration = await RBA.calculate_time(current_destination, forward_destination)

        self.result = await RBA.move_to_position(forward_destination, duration)
        if self.result:
            print("успешно доехали до станции нарезки")
            await self.leave_vane_at_cut_station(forward_destination)
        else:
            print("Не доехали до станции нарезки")
        return self.result

    async def leave_vane_at_cut_station(self, current_destination):
        print("Отцепляем лопатку на станции нарезки")

        launch_params = {"name": "leave_vane_at_cut_station",
                         "place": self.CUT_STATION_ID}

        self.result = await RBA.atomic(**launch_params)
        if self.result:
            print("успешно лопатка в станции нарезки")
        else:
            print("Ошибка: лопатка не в станции нарезки")
        return self.result

    async def get_dough(self):
        print("Начинается chain Возьми тесто")
        self.result = await self.move_to_oven()
        print(f"Chain возьми тесто заказа is over", self.result)
        return self.result

    async def calculate_chain_time(self, destination, destination_to):
        """Этот метод запрашивает время доезда от-до печи, до станции теста """
        pass


class GetSauce(object):
    """В этом классе описаны действия по добавлению соуса. """

    async def get_sauce(self):
        print("Начинаем поливать соусом")
        recipe = self.sauce.sauce_cell
        print("Данные об ячейке", recipe)
        self.result = await Controllers.give_sauce(recipe)
        if self.result:
            print("успешно полили соусом")
        else:
            print("Не успешно полили соусом")
        return self.result

    async def start_sauce(self):
        futura = asyncio.ensure_future(GetDough.get_dough(self))
        self.result = await futura
        if self.result:
            self.result = await self.get_sauce()
        return self.result


class Capture(ConfigMixin):
    """В этом классе собираются данные о том, как готовить каждый ингредиент начинки"""

    async def move_to_capture_station(self):
        """Едем до места хранения захватов"""
        print("Поехали к месту хранения захватов")
        CHAIN_ID = 1

        duration = self.MOVE_TO_CAPTURE_STATION_TIME
        destination = self.CAPTURE_STATION

        result = await RBA.move_to_position(destination, duration)
        if result:
            print("RA успешно подъехал к станции захватов")
            await self.change_capture()
        else:
            print("Ошибка подъезда к станции захватов")

    async def change_capture(self):
        """Меняем захват на тот, которым нужно брать п\ф. ВОПРОС: зависит ли захват от типа п\ф"""
        print("Берем захват для продукта")
        CHAIN_ID = 2

        launch_params = {"atomic_name": "change_capture",
                         "capture_type": self.PRODUCT_CAPTURE_ID,
                         "duration": self.CHANGE_CAPTURE_TIME}

        result = await RBA.atomic(**launch_params)
        if result:
            print("RA успешно подъехал к станции захватов")
            await self.get_vane_from_oven()
        else:
            print("Ошибка подъезда")

    async def get_product_capture(self):
        """Это метод аккумулятор для запуска ВОЗЬМИ захват """
        print("Начинаем чейн возьми захват")
        await self.move_to_capture_station()
        print("Чейн возьми захват закончилися")


class Filling(ConfigMixin):

    async def go_to_fridge(self):
        """Едем к холодильнику за продуктом"""
        print("Поехали к холодильнику за продуктом")
        CHAIN_ID = 1

        duration = self.MOVE_TO_CAPTURE_STATION_TIME
        destination = self.CAPTURE_STATION

        result = await RBA.move_to_position(destination, duration)
        if result:
            print("RA успешно подъехал к станции захватов")
            await self.change_capture()
        else:
            print("Ошибка подъезда к станции захватов")

    async def get_product_from_fridge(self):
        """Группа действий по доставанию продукта из холодильника """
        CHAIN_ID = 2
        print("берем продукт из холодильника")
        pass

    async def go_to_cut_station(self):
        CHAIN_ID = 4
        pass

    async def put_product_into_cut_station(self):
        CHAIN_ID = 5
        pass

    async def cut_the_product(self, duration, cutting_program):
        """Нарезка продукта"""
        CHAIN_ID = 6
        print("запустили команду нарежь продукт")
        result = await Controllers.cut_the_product(cutting_program)


class Baking(ConfigMixin):
    """Этот класс выполняет действия по разогреву, доставки товаров до выпекания, выпекание"""

    async def get_vane_from_cut_station(self):
        """Это группа атомарных действий по получению лопатки из станции нарезки"""
        CHAIN_ID = 1

        print("Отправляем команду примагнить лопатку в станции нарезки")

    async def turn_oven_heating_on(self):
        """Этот метод запускает прогрев печи"""

        print("Включаем прогрев печи")
        result = await Controllers.turn_oven_heating_on(self.oven_unit)
        if result:
            print("разогрев успешно включился")
        else:
            print("Ошибка печи")

    async def move_to_oven(self):
        """Движение от станции нарезки к печи"""
        pass

    async def put_vane_to_oven(self):
        """Добавтим лопатку в печь"""
        pass

    async def evaluate_baking_time(self):
        """Запускаем метод посчитай время выпечки
        возвращает словарь {oven_id: unix_time} для всех печей, время которых изменилось (и запрошенной тоже)
        """
        print("вызываем расчет времени")
        result = await Controllers.evaluate_baking_time(oven_unit=self.oven_unit,
                                                        baking_program=self.baking_program[0])

        return result

    async def time_change_handler(self):
        # как то запусть метод поменяй время во всех печах
        pass

    async def start_baking(self, result):
        duration = result[self.oven_unit]
        result = Controllers.start_baking(oven_unit=self.oven_unit,
                                          baking_program=self.baking_program[0])

    async def run_baking(self):
        """Это группа методов запускает выпекание"""
        time_changes = await self.evaluate_baking_time(self)
        await self.time_change_handler(self, time_changes)
        await self.start_baking(self, time_changes)


class Recipy(GetDough, GetSauce):

    def __init__(self):
        super().__init__()


class MakeCrust(ConfigMixin):
    def __init__(self):
        self.result = False

    async def turn_oven_heating_on(self):
        print("Включаем подогрев печи")
        self.result = await Controllers.turn_oven_heating_on(self.oven_unit)
        pass