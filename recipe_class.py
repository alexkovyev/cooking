"""Пока тут собрана информация о рецепте."""
import asyncio
import time
import random

from RBA import RBA
from controllers import Controllers


class ConfigMixin(object):
    CUT_STATION_ID = 1

class GetDough(ConfigMixin):
    """This class represents what should be done to take a vane from oven and get a dough to cut station"""

    def __init__(self):
        super().__init__()

    async def move_to_oven(self):
        """Эта функция описывает движение до назначенной печи. Исполнитель - RBA."""
        # добавить изменение статуса блюда

        CHAIN_ID = 1

        duration = self.dough.recipe_data[CHAIN_ID]
        destination = self.oven_unit
        print(duration, destination)
        result = await RBA.move_time(duration, destination)
        if result:
            print("RBA успешно подъехал к печи")
            await self.set_position_by_oven()
        else:
            print("Ошибка подъезда")

    async def set_position_by_oven(self):
        """Этот метод отдает команду позиционирования перед печью """
        CHAIN_ID = 2

        duration = self.dough.recipe_data[CHAIN_ID]
        print("начинаю set_position_by_oven")
        result = await RBA.set_position(duration)
        if result:
            print("спозиционировались перед печью")
            await self.get_vane()
        else:
            print("Ошибка позиционирования")

    async def get_vane(self):
        """Тут описывается движение возьми лопатку. """
        CHAIN_ID = 3

        duration = self.dough.recipe_data[CHAIN_ID]
        print("начинаю get_vane")
        result = await RBA.get_vane(duration)
        if result:
            print("get_vane is done")
            await self.get_out_the_oven()
        else:
            print("Ошибка при взятии лопатки")

    async def get_out_the_oven(self):
        """Тут описывается выезд из печи"""
        CHAIN_ID = 4
        duration = self.dough.recipe_data[CHAIN_ID]

        print("get_out_the_oven")
        result = await RBA.get_out_the_oven(duration)
        if result:
            print("get_out_the_oven")
            await self.move_to_dough_station()
        else:
            print("Выехали из печи с лопаткой")

    async def move_to_dough_station(self):
        """Запускает движение к станции теста"""
        CHAIN_ID = 5
        duration = self.dough.recipe_data[CHAIN_ID]
        destination = self.CUT_STATION_ID
        print("поехали к станции теста")
        result = await RBA.move_time(duration, destination)
        if result:
            print("приехали к станции теста")
            # Нужно ли тут запустить паралельно танец? так как у RA простой пока тесто выдается
            await self.controllers_get_dough()
        else:
            print("ошибка подъезда на станцию теста")

    async def controllers_get_dough(self):
        """отдает команду контролеру получить тесто"""
        print("берем тесто")
        dough_point = self.dough.halfstuff_cell
        result = await Controllers.give_dough(dough_point)
        if result:
            print("взяли тесто")
            await self.control_dough_position()
        else:
            print("Ошибка получения теста")
        # запускает функцию списать п\ф

    async def control_dough_position(self):
        """отдаем команду на поправление теста"""
        print("поправляем тесто", time.time())
        result = await self.movement()
        if result:
            print("успешно поправили тесто")
            await self.move_to_cut_station()
        else:
            print("Ошибка поправления теста")

    async def move_to_cut_station(self):
        """отдает команду на движение от станции теста на станцию нарезки"""
        print("едем к станции нарезки", time.time())
        result = await self.movement()
        if result:
            print("успешно доехали до станции нарезки")
            await self.set_position_by_cut_station()
        else:
            print("Не доехали до станции нарезки")

    async def set_position_by_cut_station(self):
        """типовая команда для нескольких классов"""
        print("позиционируемся относительно станции нарезки", time.time())
        result = await self.movement()
        if result:
            print("успешно спозиционировались относительно станции нарезки")
            await self.get_into_cut_station()
        else:
            print("Не успешно спозиционировались относительно станции нарезки")

    async def get_into_cut_station(self):
        """Заезжаем в станцию нарезки"""
        print("заезжаем в станцию нарезки", time.time())
        result = await self.movement()
        if result:
            print("успешно заехали в станцию нарезки")
            await self.free_capture()
        else:
            print("Не успешно заехали в станцию нарезки")

    async def free_capture(self):
        """Освободить захват"""
        print("освобождаем захват", time.time())
        result = await self.movement()
        if result:
            print("успешно освободили захват")
            # await self.set_position_by_cut_station()
        else:
            print("Не успешно освободии захват")

    async def get_dough(self):
        print("Начинается chain")
        await self.move_to_oven()

        print(f"Chain возьми тесто заказа is over")


class GetSauce(object):
    """В этом классе описаны действия по добавлению соуса. """

    def __init__(self):
        self.sauce_plan_duration = 100

    async def get_sauce(self):
        # Controllers.sauce()
        print("Начинаем чейн соус", time.time())
        result = await self.movement()
        if result:
            print("успешно полили соусом")
            # await self.set_position_by_cut_station()
        else:
            print("Не успешно полили соусом")


class Filling(object):
    """В этом классе собираются данные о том, как готовить начинку"""

    async def change_capture(self):
        """Меняем захват на тот, которым нужно брать п\ф. ВОПРОС: зависит ли захват от типа п\ф"""
        pass

    async def go_to_fridge(self):
        """Едем от точки Х к холодильнику"""
        pass

    async def set_position_by_fridge(self):
        "Позиционирование напротив холодильника"
        pass


class Recipy(GetDough, GetSauce):

    def __init__(self):
        super().__init__()
        self.recipy_list = [self.get_dough, self.get_sauce, self.get_dough, self.get_sauce]
        # self.plan_duration = sum([self.dough_plan_duration, self.sauce_plan_duration])

    async def start_dish_cooking(self):
        for chain in self.recipy_list:
            print("Начинается 1 чейн")
            result = await chain()
            if not result:
                break
            # if not today_orders.is_cooking_paused or today_orders.orders_requested_for_delivery:
            #     print("Начинается 1 чейн")
            #     result = await chain()
            #     if not result:
            #         break
            # if today_orders.is_pause_cooking:
            #     await today_orders.cooking_pause_handler()
            # elif today_orders.orders_requested_for_delivery:
            #     await today_orders.dish_delivery()

    #
    # async def get_dough_st(self):
    #     """отдает команду контролеру получить тесто"""
    #     # Controllers.give_dough(halfstuff_cell)
    #     # запускает функцию списать п\ф
    #     print("берем тесто", time.time())
    #     result = await self.movement()
    #     if result:
    #         print("взяли тесто")
    #         one = asyncio.create_task(self.turn_oven_on())
    #         two = asyncio.create_task(self.get_tomato())
    #         await asyncio.gather(one, two)
    #     else:
    #         print("Ошибка получения теста")
    # #
    # async def turn_oven_on(self):
    #     print("включаем печь", time.time())
    #     result = await self.movement()
    #     if result:
    #         print("включили печь")
    #     else:
    #         print("печь не включилась")
    #
    # async def get_tomato(self):
    #     print("берем томат", time.time())
    #     result = await self.movement()
    #     if result:
    #         print("взяли томат")
    #     else:
    #         print("не ввзяли томат")
    #
    # def get_dough(self, halfstuff_cell):
    #     """отдает команду контролеру получить тесто"""
    #     # Controllers.give_dough(halfstuff_cell)
    #     # запускает функцию списать п\ф
    #     pass
