import asyncio
import random


class Movement():

    @staticmethod
    async def movement(n, *args):
        print("Запустилась работа робота")
        await asyncio.sleep(n)
        result = random.choice([True, True, False])
        print("Работа робота завершена")
        return result


class RBA(Movement):

    @classmethod
    async def move_time(clx, time, destination):
        # в качестве destination указываем конечный пункт назначения, текущее положение 'запоминает' RA
        print("RBA двигается к печи", destination, "Время движения", time)
        result = await clx.movement(time)
        return result

    @classmethod
    async def set_position(cls, time):
        print("Начинается позиционирование")
        result = await cls.movement(time)
        return result

    @classmethod
    async def get_vane(cls, time):
        # нужно ли указывать тип захвата?
        print("Примагничиваем захват")
        result = await cls.movement(time)
        return result

