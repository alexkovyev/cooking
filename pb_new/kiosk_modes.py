import asyncio
# from utils import start_testing, parse_recipes
# from recipe_data import recipe_data
# from start_PBM import create_tasks


class BaseMode(object):
    def __init__(self):
        self.is_busy = False
        self.time_left = None

    def is_ok_to_del(self):
        return True if not self.is_busy else False

class CookingMode(BaseMode):
    def __init__(self):
        self.status = "Ready Готовить"

    async def hello_from(self):
        print("Привет от готовки", asyncio.sleep(10))

    async def start_pbm(self):
        test_result, equipment_data = start_testing()
        recipes = parse_recipes(recipe_data)
        if test_result and recipes:
            cooking = asyncio.create_task(create_tasks(test_result, equipment_data))
        else:
            raise ValueError("Оборудование неисправно, нельзя работать")


class TestingMode(object):
    def __init__(self):
        self.status = "Тестируем"

    async def hello_from(self):
        print("Привет из теста", asyncio.sleep(10))

class StandBy(object):
    def __init__(self):
        self.status = "В режиме ожидания"

    async def hello_from(self):
        print("Привет из stand by", asyncio.sleep(10))
