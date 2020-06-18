import asyncio
import concurrent.futures
import multiprocessing
import time

from .BaseMode import BaseMode
from recipe_data import recipe_data


class BeforeCooking(object):

    def __init__(self):
        self.status = "getting_ready"

    @classmethod
    async def go_to_db_get_data(clx):
        print("Подключаемся к БД за информацией", time.time())
        equipment_data = ('супер важная информация об оборудовании', 'из БД')
        await asyncio.sleep(10)
        print("Получили данные из БД", time.time())
        return equipment_data

    @classmethod
    def start_testing(clx):
        """Тут вызываем методы контролеров по тестированию оборудования"""

        # вызывается какой то супер метод контроллеров на проверку, возвращает status и dict с данными об оборудовании
        is_equipment_ok = True
        equipment_data = {"ovens": {i: {"oven_id": i, "status": "free"} for i in range(1, 22)},
                          "cut_station": True,
                          "package_station": True,
                          "pick_up_points": {1: True,
                                             2: True,
                                             3: True}
                          }
        print("Начинаем тестировать оборудования", time.time())
        time.sleep(40)
        print("Оборудование протестировано, исправно", time.time())
        return is_equipment_ok, equipment_data

    @classmethod
    def parse_recipes(clx):
        """Парсит все рецепты в директории и возвращает словарь вида: описать"""
        print("Начинаем парсить рецепты", time.time())
        time.sleep(40)
        print("Рецепты спарсены", time.time())
        recipes = recipe_data
        return recipes

    @classmethod
    async def start_pbm(self):
        equipment_data = await self.go_to_db_get_data()
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count())
        my_loop = asyncio.get_running_loop()
        async def task_1():
            is_equipment_ok, equipment_data = await my_loop.run_in_executor(pool, self.start_testing)
            return is_equipment_ok, equipment_data
        async def task_2():
            recipes = await my_loop.run_in_executor(pool, self.parse_recipes)
            return recipes
        task_1 = my_loop.create_task(task_1())
        task_2 = my_loop.create_task(task_2())
        await asyncio.gather(task_1, task_2)
        self.current_instance = CookingMode()


class CookingMode(BaseMode):
    def __init__(self):
        self.status = "Ready Готовить"

    async def hello_from(self):
        print("Привет от готовки", asyncio.sleep(10))