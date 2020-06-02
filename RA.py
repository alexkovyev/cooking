import asyncio
import random
import time


class RAError(Exception):
    """Класс ошибок RA"""

    def __init__(self):
        self.text = "Возникла ошибка RA"


# это просто эмуляция работы RA, необходимая для тестирования PBM
class Movement(object):
    """Эмуляция работы RA для нужд PBM"""

    @staticmethod
    async def movement(n):
        print("RA начал работу")
        await asyncio.sleep(n)
        result = random.choice([True, True])
        print("Работа RA завершена")
        return result


class RA(Movement):

    @classmethod
    async def get_position_move_time(clx, from_place: str, to_place: str):
        """ метод рассчитывает время на перемещение между точками.
        Эмуляция работы: возвращает случайным образом список
        из вариантов или пустой если точка не найдена.
        :param
           from_place: str
           to_place: srt
        :return: possible_duration (list[int])
        """
        result_choice = random.choice([[9, 15, 16, 8, 10], [9, 15, 16, 8, 10], [9, 15, 16, 8, 10], []])
        print(result_choice)
        return result_choice

    @classmethod
    async def position_move(cls, place: str, duration: int):
        """
        :param place: str
        :param duration: int
        :return: int if succeed
                 raiseError if not
                 # нужно определить типы ошибок
        """
        print(f"RA двигается к {place} за {duration} сек")
        result = await cls.movement(duration)
        if result:
            return duration
        else:
            raise RAError

    @classmethod
    async def get_atomic_action_time(clx, **kwargs):
        """
        :param name: имя пакета атомарных действий, str
        :param place: id оборудования
        :return: int если успешно
        :raise RAError
        """
        print("Атомарное действие", kwargs["name"])
        return random.randint(1,10)

    @classmethod
    async def atomic_action(cls, **kwargs):
        place = kwargs["place"]
        atomic_name = kwargs["name"]
        print("RA выполняет атомарное действие", atomic_name)
        duration = random.randint(1, 10)
        result = await cls.movement(duration)
        return result

    @classmethod
    async def dance(cls):
        print("Танцуем", time.time())
        await asyncio.sleep(1)

    @classmethod
    async def get_current_position(cls):
        """Возвращает текущее местоположение RA"""
        return "oven 1"

    @classmethod
    async def get_current_gripper(cls):
        return

    @classmethod
    async def is_capture_is_gripper(cls):
        """Проверяет является ли текущий захват гриппером"""
        return random.choice([False, False, False])
