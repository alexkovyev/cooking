import asyncio
import random
import time

from pydispatch import Dispatcher


class ControllersEvents(Dispatcher):
    """
    Dispatcher for controller event handlers. DON'T CREATE instances of this class, use
    cntrls_events.
    """
    _events_ = ['qr_scanned', 'hardware_status_changed']

    def qr_scanned(self, _params):
        self.emit('qr_scanned', params=_params)

    def hardware_status_changed(self, _unit_name, _status):
        self.emit('hardware_status_changed', unit_name=_unit_name, status=_status)


cntrls_events = ControllersEvents()

async def event_generator(cntrls_events):

    async def qr_code_scanning_alarm(cntrls_events):
        print("Сработало событие qr код", time.time())
        params = {"ref_id": 65, "pickup":1}
        cntrls_events.qr_scanned(params)

    async def hardware_status_changed(cntrls_events):
        print("Сработало событие поломка печи", time.time())
        cntrls_events.hardware_status_changed('owen_cell_2', 'broken')

    while True:
        await asyncio.sleep(2)
        print("Выбираем событие", time.time())
        options = [qr_code_scanning_alarm, hardware_status_changed]
        my_choice = random.randint(0, 1)
        what_happened = options[my_choice]
        await what_happened(cntrls_events)
        n = random.randint(1, 10)
        print("Trouble-maker засыпает на", n, "сек в ", time.time())
        await asyncio.sleep(n)
        print("Trouble-maker снова с нами", time.time())


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
        """params: dough_point
        return: bool """
        print("Выдаем тесто из тестовой станции №", dough_point)
        result = await cls.movement(dough_point)
        return result

    @classmethod
    async def give_sauce(cls, sauce_content):
        print("Поливаем соусом")
        # sauce_content=[(1, 5), (2, 25)] 0 - id насосной станции, 1 - колво в условных порциях (мл)
        # если PBM оперирует реептом, то передавать Id насосной станции соуса и траекторию полива
        result = await cls.movement()
        # нужно добавить уведомления от контроллеров, если 1-я попытка неудачна, запускается вторая.
        # уведомление дожно содержать время на 2-ю попытку
        return result

    @classmethod
    async def cut_the_product(cls, cutting_program):
        print("Начинаем резать продукт")
        result = await cls.movement()
        # нужно добавить уведомления от контроллеров, если 1-я попытка неудачна, запускается вторая.
        # уведомление дожно содержать время на 2-ю попытку или проверку почему не запустилось
        return result

    @classmethod
    async def turn_oven_heating_on(cls, oven_id):
        """Алексей сказал, что время прогрева печи всегда одинаковое для любой программы и
        температура (режим) тоже"""
        print("Включили нагрев печи")
        result = await cls.movement()
        # если будет ошибка печи при попытке включить разогрев. То она будет тут или в Event?
        return result