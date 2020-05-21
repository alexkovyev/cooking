import asyncio
import random


class Movement(object):

    @staticmethod
    async def movement(n, *args):
        print("Запустилась работа робота")
        await asyncio.sleep(n)
        result = random.choice([True, True, True])
        print("Работа робота завершена")
        return result


class RBA(Movement):

    @classmethod
    async def move_to_position(clx, destination, duration):
        # в качестве destination указываем конечный пункт назначения, текущее положение 'запоминает' RA
        # нужно вернуть время фактическое ? нужно ли уведомляь о том, что запускается несколько попыток?
        print("RBA двигается к печи", destination, "Время движения", duration)
        result = await clx.movement(duration)
        return result

    @classmethod
    async def atomic(cls, **kwargs):
        duration = kwargs["duration"]
        atomic_name = kwargs["atomic_name"]
        print("RA выполняет атомарное действие", atomic_name)
        result = await cls.movement(duration)
        return result

    # @classmethod
    # async def set_position(cls, duration):
    #     print("Начинается позиционирование")
    #     result = await cls.movement(duration)
    #     return result
    #
    # @classmethod
    # async def get_vane(cls, duration):
    #     # нужно ли указывать тип захвата?
    #     print("Примагничиваем захват")
    #     result = await cls.movement(duration)
    #     return result
    #
    # @classmethod
    # async def get_out_the_oven(cls, duration):
    #     # нужна ли эта команда или это часть общей? Поездка на станцию нарезки отдельно.
    #     # Какие парамеры кроме времени?
    #     print("Выезжаем из печи")
    #     result = await cls.movement(duration)
    #     return result
