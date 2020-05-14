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
        print("Выдаем тесто из тестовой станции №", dough_point)
        result = await cls.movement(dough_point)
        return result

    @classmethod
    async def give_sauce(cls, sauce_content):
        print("Поливаем соусом")
        # sauce_content=[(1, 5), (2, 25)] 0 - id насосной станции, 1 - колво в условных порциях (мл)
        result = await cls.movement()
        # нужно добавить уведомления от контроллеров, если 1-я попытка неудачна, запускается вторая.
        # уведомление дожно содержать время на 2-ю попытку
        return result