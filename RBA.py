import asyncio
import random


class Movement():

    async def movement(self):
        n = random.randint(1, 10)
        print("Запустилась работа робота")
        await asyncio.sleep(n)
        result = random.choice([True, True, False])
        print("Работа робота завершена")
        return result


class RBA(Movement):

    async def move_to_oven(self):
        print("RBA двигается к печи")
