"""Пока тут собрана информация о рецепте.
Каждый рецепт это исполняемый Python код (?)
"""
import asyncio
import time
import random

# import RBA
# import Controllers

async def movement():
    n = random.randint(1, 10)
    print("Запустилась работа робота")
    await asyncio.sleep(n)
    result = random.choice([True, True, False])
    print("Работа робота завершена")
    return result

# вариант с функциями, а не классом
async def move_to_oven(result, oven_id):
    """Эта функция описывает движение от текущего места (мы отслеживаем, где сейчас находится манипулятор? Как? до
    назнаечнной печи. Исполнитель - RBA. Какую обратную связь от RBA получаем? как обрабатывает исключение"""
    # Нужно ли тут время и какие то координаты?
    # result = RBA.move_to_oven(oven_id, duration)

    if result:
        print("RBA двигается к печи")
        # print("RBA двигается к печи", time.time())
        result = await movement()
        if result:
            print("RBA успешно подъехал к печи")
            await set_position_by_oven()
        else:
            print("Ошибка подъезда")
    # как мы получаем что RBA действительно подъехало?


async def set_position_by_oven():
    """Этот метод отдает команду позиционирования перед печью """
    print("начинаю set_position_by_oven", time.time())
    result = await movement()
    if result:
        print("set_position_by_oven is done")
        await get_vane()
    else:
        print("Ошибка позиционирования")


async def get_vane():
    """Тут описывается движение возьми лопатку. """
    print("начинаю get_vane", time.time())
    result = await movement()
    if result:
        print("get_vane is done")
        await get_out_the_oven()
    else:
        print("Ошибка при взятии лопатки")


async def get_out_the_oven():
    """Тут описывается выезд из печи. Нужно ли делать отдельную команду?"""
    print("get_out_the_oven", time.time())
    result = await movement()
    if result:
        print("get_out_the_oven")
        await move_to_dough_station()
    else:
        print("Выехали из печи с лопаткой")


async def move_to_dough_station():
    """Запускает движение к станции теста"""
    print("поехали к станции теста", time.time())
    result = await movement()
    if result:
        print("приехали к станции теста")
        await get_dough_st()
    else:
        print("ошибка подъезда на станцию теста")


async def get_dough_st():
    """отдает команду контролеру получить тесто"""
    #Controllers.give_dough(halfstuff_cell)
    #запускает функцию списать п\ф
    print("берем тесто", time.time())
    result = await movement()
    if result:
        print("взяли тесто")
        one = asyncio.create_task(turn_oven_on())
        two = asyncio.create_task(get_tomato())
        await asyncio.gather(one, two)
    else:
        print("Ошибка получения теста")


async def turn_oven_on():
    print("включаем печь", time.time())
    result = await movement()
    if result:
        print("включили печь")
    else:
        print("печь не включилась")


async def get_tomato():
    print("берем томат", time.time())
    result = await movement()
    if result:
        print("взяли томат")
    else:
        print("не ввзяли томат")


async def get_dough(order_id, oven_id, duration):
    print("Начинается chain", order_id)
    await move_to_oven(oven_id, duration)

    print(f"Chain {order_id} is over")


class GetDough(object):
    """This class represents what should be done to take a vane from oven and get a dough to cut station
    МОЖЕТ БЫТЬ НЕ ДЛАТЬ КЛАССОМ? проблемы с курутинами в инит"""

    def __init__(self):
        # сомневаюсь насчет переменных? по идее они должн быть после сортировки
        self.plan_duration = 300

    async def move_to_oven(self, oven_id, duration):
        """Эта функция описывает движение от текущего места (мы отслеживаем, где сейчас находится манипулятор? Как? до
        назнаечнной печи. Исполнитель - RBA. Какую обратную связь от RBA получаем? как обрабатывает исключение"""
        # Нужно ли тут время и какие то координаты?
        # result = RBA.move_to_oven(oven_id, duration)
        print("RBA двигается к печи", time.time())
        await asyncio.sleep(duration)
        print("RBA подъехал к печи", time.time())
        # как мы получаем что RBA действительно подъехало?

    async def set_position_by_oven(self):
        """Этот метод отдает команду позиционирования перед печью """
        DURATION = 2
        print("начинаю set_position_by_oven", time.time())
        await asyncio.sleep(DURATION)
        print("set_position_by_oven is done", time.time())

    async def get_vane(self):
        """Тут описывается движение возьми лопаткку. """
        DURATION = 1
        print("начинаю get_vane", time.time())
        await asyncio.sleep(DURATION)
        print("get_vane is done", time.time())

    async def get_out_the_oven(self):
        """Тут описывается выезд из печи. Нужно ли делать отдельную команду?"""
        DURATION = 1
        print("get_out_the_oven", time.time())
        await asyncio.sleep(DURATION)
        print("get_out_the_oven", time.time())

    async def move_to_dough_station(self, halfstuff_cell):
        """Запускает движение к станции теста"""
        DURATION = 3
        print("move_to_dough_station", time.time())
        await asyncio.sleep(DURATION)
        print("move_to_dough_station", time.time())

    # def get_dough(self, halfstuff_cell):
    #     """отдает команду контролеру получить тесто"""
    #     # Controllers.give_dough(halfstuff_cell)
    #     # запускает функцию списать п\ф
    #     pass

    # def control_dough_position(self):
    #     """отдаем команду на поправление теста"""
    #     pass
    #
    # def move_to_cut_station(self):
    #     """отдает команду на движение от станции теста на станцию нарезки"""
    #     pass
    #
    # def set_position_by_cut_station(self):
    #     """это типовая команда?"""
    #     pass
    #
    # def get_in_cut_station(self):
    #     """Заезжаем в станцию нарезки"""
    #     pass
    #
    # def free_capture(self):
    #     """Освободить захват"""
    #     pass

    async def get_dough(self):
        print("Начинается chain", self.id)
        await self.move_to_oven(self.oven_unit, duration)
        await self.set_position_by_oven()
        await self.get_vane()
        await self.get_out_the_oven()
        print(f"Chain {id} is over")
        # self.move_to_oven()
        # self.set_position_by_oven()
        # # и так далее


# class GetSauce(object):
#     """В этом классе описаны действия по добавлению соуса и добавки"""
#
#     @staticmethod
#     def get_sause(self, halfstuff_cell):
#         Controllers.sause(halfstuff_cell)