import asyncio
import random


class RAError(Exception):
    def __init__(self):
        self.text = "Возникла ошибка RA"


# это просто эмуляция работы RA, необходимая для тестирования PBM
class Movement(object):

    @staticmethod
    async def movement(n, *args):
        print("Запустилась работа робота")
        await asyncio.sleep(n)
        result = random.choice([True, True])
        print("Работа робота завершена")
        return result


class RA(Movement):

    def get_position_move_time(from_place: str, to_place: str):
        pass

    @classmethod
    async def position_move(clx, place: str, duration: int):
        """
        :param place: str
        :param duration: int
        :return: int if succeed
                 raiseError if not
                 # нужно определить типы ошибок
        """
        print("RBA двигается к печи", place)
        result = await clx.movement(duration)
        if result:
            return duration
        else:
            raise RAError

    @classmethod
    async def atomic_action(cls, **kwargs):
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
