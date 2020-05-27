import asyncio
import random


class Movement(object):

    @staticmethod
    async def movement(n, *args):
        print("Запустилась работа робота")
        await asyncio.sleep(n)
        result = random.choice([True, True])
        print("Работа робота завершена")
        return result


class RA(Movement):

    @classmethod
    async def move_to_position(clx, destination, duration):
        # в качестве destination указываем конечный пункт назначения, текущее положение 'запоминает' RA
        # нужно вернуть время фактическое ? нужно ли уведомляь о том, что запускается несколько попыток?
        print("RBA двигается к печи", destination, "Время движения", duration)
        result = await clx.movement(duration)
        return result

    @classmethod
    async def atomic(cls, **kwargs):
        place = kwargs["place"]
        atomic_name = kwargs["name"]
        print("RA выполняет атомарное действие", atomic_name)
        duration = random.randint(1, 10)
        result = await cls.movement(duration)
        return result

    @classmethod
    async def get_current_location(cls):
        """Возвращает текущее местоположение RA"""
        return "oven 1"

    @classmethod
    async def is_capture_is_gripper(cls):
        """Проверяет является ли текущий захват гриппером"""
        return random.choice([False, False, False])

    @classmethod
    async def calculate_time(cls, current_destination, forward_destination):
        """Считает время доезда от точки А до Б в миллисекундах"""
        return 12

    async def get_atomic_action_time(name="get_vane_from_oven", place="oven 17"):
        pass
