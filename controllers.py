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
        """Нам в PBM нужен чек-код заказа (мы пока его называем ref_id) и идентификатор пункта выдачи (uuid4),
        единый для Controllers, RA, PBM """
        print("Сработало событие qr код", time.time())
        params = {"ref_id": 65, "pickup": 1}
        cntrls_events.qr_scanned(params)

    async def hardware_status_changed(cntrls_events):
        """ ВОПРОС к контроллерам: по идее тут все оборудование. Вы просто выдаете идентификатор и статус
        или будет еще тип: "oven", "cut_station", те {"equipment_type": cut_station,
                                                      "uuid": o48932492834281,
                                                       "status": "broken"}
        """
        print("Сработало событие поломка печи", time.time())
        cntrls_events.hardware_status_changed('owen_cell_2', 'broken')

    while True:
        # это эмуляция работы контроллеров по генерации разных событий
        await asyncio.sleep(2)
        print("Выбираем событие", time.time())
        options = [qr_code_scanning_alarm, hardware_status_changed]
        my_choice = random.randint(0, 1)
        what_happened = options[my_choice]
        await what_happened(cntrls_events)
        n = random.randint(20, 40)
        print(f"Trouble-maker засыпает на {n} сек в {time.time()}")
        await asyncio.sleep(n)
        print("Trouble-maker снова с нами", time.time())


class Movement(object):
    """Это эмуляция работы контроллеров в части засыпания при выполнении методов :)"""

    @staticmethod
    async def movement(*args):
        n = random.randint(2, 20)
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
    async def give_sauce(cls, sauce_recipe):
        print("Поливаем соусом")
        print("Параметры из контроллеров считались", sauce_recipe)
        # sauce_recipe=[(1, 1), (2, 2)] для вложенного кортежа: 0 - id насосной станции, 1 - программа поливки
        result = await cls.movement()
        # нужно добавить уведомления от контроллеров, если 1-я попытка неудачна, запускается вторая.
        # Алексей сказал, что вы будете машнным зрением определять можно ли повторно полить или прокатит
        # ли "неуспешный" варант
        # уведомление дожно содержать время на 2-ю попытку и колво ингредиентов (если нужно или убираем
        # вторую попытку?)
        return result

    @classmethod
    async def cut_the_product(cls, cutting_program):
        print("Начинаем резать продукт")
        result = await cls.movement()
        # нужно добавить уведомления от контроллеров, если 1-я попытка неудачна, запускается вторая.
        # уведомление дожно содержать время на 2-ю попытку
        # Второй раз помидору не везем? в случае неудачи: на выброс?
        return result

    @classmethod
    async def turn_oven_heating_on(cls, oven_id):
        """Алексей сказал, что время прогрева печи всегда одинаковое для любой программы и
        температура (режим) тоже, поэтому в параметрах только идентификатор печи"""
        print("Включили нагрев печи", oven_id)
        result = await cls.movement()
        return result

    @classmethod
    async def evaluate_baking_time(cls, oven_unit, baking_program):
        """Метод определяет фактическое время, необходимое для выпечки с учетом загрузки печи
        :param
        oven_unit = идентификатор печи, uuid
        baking_program = 2, те программа выпечки int
        вопрос: при прогреве (до выпечки) и корочкообразовании в параметрах нужно указывать, тип операции?
        так как программы корочки и выпечки могут сопасть по цифрам или не нужно и просто номер?
        :return
        {oven_id: unix_time} для всех печей, время которых изменилось (и запрошенной тоже)
        """
        print("Считаем изменения времени")
        return {21: (time.time()+180), 20:(time.time()+80)}

    @classmethod
    async def start_baking(cls, oven_unit, baking_program):
        """Возвращает результат выпечки: успешно или нет """
        print("Начинаем выпечку")
        result = await cls.movement()
        return result
