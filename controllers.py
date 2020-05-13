import asyncio
import random


class Movement(object):

    @staticmethod
    async def movement(*args):
        n = random.randint(1, 10)
        print("Запустилась работа контроллеров")
        await asyncio.sleep(n)
        result = random.choice([True, True, False])
        print("Работа контроллеров завершена")
        return result


class Controllers(Movement):

    @classmethod
    async def give_dough(cls, dough_point):
        print("Выдаем тесто из тестовой станции", dough_point)
        result = await cls.movement(dough_point)
        return result