"""Этот модуль управляет заказами и блюдами"""
import asyncio
import time
import types

from base_order import BaseOrder
from equipment import Equipment
from RA import RA


class PizzaBotMain(object):
    """Это основной класс блока.
    Этот класс содержит информацию о том, какие блюда готовятся в текущий момент, содержит информацию о печах и
    показываает время работы коиска. После завешения заказа, он удаляется из self.current_orders_proceed
    """

    def __init__(self, equipment_data, recipes):
        self.equipment = Equipment(equipment_data)
        self.recipes = recipes
        self.is_cooking_paused = False
        # все заказы за текущий сеанс работы, {id: BaseOrder}
        self.current_orders_proceed = {}
        # все неприготовленые блюда
        self.current_dishes_proceed = {}
        self.time_to_cook_all_dishes_left = 0
        self.orders_requested_for_delivery = {}
        self.is_free = False
        # разные полезные очереди
        self.main_queue = asyncio.Queue()
        self.delivery_queue = asyncio.Queue()
        self.maintain_queue = asyncio.Queue()
        self.immediately_executed_queue = asyncio.Queue()

    def checking_order_for_double(self, new_order_id):
        """Этот метод проверяет есть ли уже заказ с таким ref id в обработке
        :return bool"""
        is_new_order = True if new_order_id not in self.current_orders_proceed.keys() else False
        return is_new_order

    async def get_order_content_from_db(self, new_order_id):
        """Этот метод вызывает процедуру 'Получи состав блюд в заказе' и возвращает словарь вида
        {"refid": new_order_id,
                     "dishes": {"40576654-9f31-11ea-bb37-0242ac130002":
                         {
                             "dough": {"id": 2},
                             "sauce": {"id": 2, "content": ((1, 5), (2, 25))},
                             "filling": {"id": 1, "content": (6, 2, 3, 3, 6, 8)},
                             "additive": {"id": 7}
                         }
                         ,
                         "6327ade2-9f31-11ea-bb37-0242ac130002":
                             {
                                 "dough": {"id": 1},
                                 "sauce": {"id": 2, "content": ((1, 5), (2, 25))},
                                 "filling": {"id": 1, "content": (6, 2, 3, 3, 6, 8)},
                                 "additive": {"id": 1}
                             }
                     }
                     }
        """
        new_order = dict(refid=new_order_id, dishes={"40576654-9f31-11ea-bb37-0242ac130002":
            {
                "dough": {"id": 2},
                "sauce": {"id": 2, "content": ((1, 5), (2, 25))},
                "filling": {"id": 1, "content": ("tomato", "cheese", "ham", "olive", "pepper", "bacon")},
                "additive": {"id": 7}
            },
            "6327ade2-9f31-11ea-bb37-0242ac130002":
                {
                    "dough": {"id": 1},
                    "sauce": {"id": 2, "content": ((1, 5), (2, 25))},
                    "filling": {"id": 1, "content": ("tomato", "cheese", "ham", "olive", "pepper", "bacon")},
                    "additive": {"id": 1}
                }
        })
        return new_order

    def get_recipe_data(self, new_order):
        """Этот метод добавляет в данные о блюде параметры чейнов рецепта для конкретного ингредиента
        :param словарь блюд из заказа
        {'40576654-9f31-11ea-bb37-0242ac130002':
            {'dough': {'id': 2},
            'sauce': {'id': 2, 'content': ((1, 5), (2, 25))},
            'filling': {'id': 1, 'content': (6, 2, 3, 3, 6, 8)},
            'additive': {'id': 7}},
        '6327ade2-9f31-11ea-bb37-0242ac130002':
            {'dough': {'id': 1},
            'sauce': {'id': 2, 'content': ((1, 5), (2, 25))},
            'filling': {'id': 1, 'content': (6, 2, 3, 3, 6, 8)},
            'additive': {'id': 1}}}

        Возвращаемый результат, где filling -->content tuple 0 - halfstaff_id, 1 - {cutting_program}
        {'refid': 65, 'dishes': [
        {'dough': {'id': 2, 'recipe': {1: 10, 2: 5, 3: 10, 4: 10, 5: 12, 6: 7, 7: 2}},

        'sauce': {'id': 2,
                 'content': ((1, 5), (2, 25)),
                'recipe':
                        {'duration': 20,
                        'content': {1:
                                     {'program': 1, 'sauce_station': None, 'qt': 5},
                                    2:
                                      {'program': 3, 'sauce_station': None, 'qt': 25}}}},

        'filling': {'id': 1,
        'content': ((6, {'program_id': 2, 'duration': 10}), (2, {'program_id': 1, 'duration': 12}),
        (3, {'program_id': 5, 'duration': 15}), (3, {'program_id': 8, 'duration': 8}),
        (6, {'program_id': 4, 'duration': 17}), (8, {'program_id': 9, 'duration': 9})),
        'cooking_program': (2, 180), 'make_crust_program': (2, 20), 'chain': {}},

        'additive': {'id': 7, 'recipe': {1: 5}}},

        {'dough': {'id': 1, 'recipe': {1: 10, 2: 5, 3: 10, 4: 10, 5: 12, 6: 7, 7: 2}},

        'sauce': {'id': 2,
                 'content': ((1, 5), (2, 25)),
                'recipe':
                        {'duration': 20,
                        'content': {1:
                                     {'program': 1, 'sauce_station': None, 'qt': 5},
                                    2:
                                      {'program': 3, 'sauce_station': None, 'qt': 25}}}},
        'filling': {'id': 1, 'content': ((6, {'program_id': 2, 'duration': 10}),
        (2, {'program_id': 1, 'duration': 12}), (3, {'program_id': 5, 'duration': 15}),
        (3, {'program_id': 8, 'duration': 8}), (6, {'program_id': 4, 'duration': 17}),
        (8, {'program_id': 9, 'duration': 9})),
        'cooking_program': (1, 180), 'make_crust_program': (1, 20), 'chain': {}},

        'additive': {'id': 1, 'recipe': {1: 5}}}]}
"""

        # print("Входные данные", new_order)

        def create_sauce_recipe(self, dish):
            """Этот метод выбирает рецепт для конкретного компонента соуса из общей базы рецептов"""
            sauce_id = dish["sauce"]["id"]
            dish["sauce"]["recipe"] = self.recipes["sauce"][sauce_id]
            for component, my_tuple in zip(dish["sauce"]["recipe"]["content"], dish["sauce"]["content"]):
                dish["sauce"]["recipe"]["content"][component]["qt"] = my_tuple[1]
            # print("составили рецепт соуса", dish["sauce"])

        def create_filling_recipe(self, dish):
            """Этот метод выбирает рецепт начинки для начинки в общем и для каждого компонента начинки в целом"""
            filling_id = dish["filling"]["id"]
            dough_id = dish["dough"]["id"]
            dish["filling"]["cooking_program"] = self.recipes["filling"][filling_id]["cooking_program"][dough_id]
            dish["filling"]["make_crust_program"] = self.recipes["filling"][filling_id]["make_crust_program"][dough_id]
            dish["filling"]["pre_heating_program"] = self.recipes["filling"][filling_id]["pre_heating_program"][dough_id]
            dish["filling"]["stand_by"] = self.recipes["filling"][filling_id]["stand_by_program"][dough_id]
            dish["filling"]["chain"] = self.recipes["filling"][filling_id]["chain"]
            halfstaff_content = dish["filling"]["content"]
            cutting_program = self.recipes["filling"][filling_id]["cutting_program"]
            dish["filling"]["content"] = [list(_) for _ in (zip(halfstaff_content, cutting_program))]
            print("Составили рецепт начинки", dish["filling"])

        for dish in new_order.values():
            dish["dough"]["recipe"] = self.recipes["dough"]
            create_sauce_recipe(self, dish)
            create_filling_recipe(self, dish)
            dish["additive"]["recipe"] = self.recipes["additive"]
            # print("В блюдо добавили рецепт")

    def fill_current_dishes_proceed(self, dish):
        """ Добавляет блюда заказа в self.current_dishes_proceed
        @:param order: экземпляр класса блюдо, созданный в self.create_new_order"""
        self.current_dishes_proceed[dish.id] = dish

    async def create_new_order(self, new_order):
        """Этот метод создает экземпляр класса Order и заносит его в словарь self.current_orders_proceed
        @:params:
        new_order - это словарь с блюдами, получаемый из БД в рамках метода get_order_content_from_db """

        try:
            # резервируем печи для заказа (сразу 2 шт)
            ovens_reserved = [self.equipment.oven_reserve(dish) for dish in new_order["dishes"]]
            # создаем экземпляр класса заказа
            order = BaseOrder(new_order, ovens_reserved)
            if order:
                # если заказ создан успешно, помещаем его в словарь всех готовящихся заказов
                self.current_orders_proceed[order.ref_id] = order
                # for dish in order.dishes:
                #     self.main_queue.append((1, dish))
                for dish in order.dishes:
                    self.fill_current_dishes_proceed(dish)
                    await self.put_chains_in_queue(dish)

                # перемещаем заказы в словарь всех готовящихся блюд
                # self.fill_current_dishes_proceed(order)
        # придумать ошибки какие могут быть
        except ValueError:
            pass

    # def fill_current_dishes_proceed(self, order):
    #     """ Добавляет блюда заказа в self.current_dishes_proceed
    #     @:param order: экземпляр класса заказ, созданный в self.create_new_order"""
    #
    #     for dish in order.dishes:
    #         self.current_dishes_proceed[dish.id] = dish

    async def put_chains_in_queue(self, dish):
        """Добавляет чейны рецепта в очередь готовки в виде кортежа (dish, chain)"""
        chains = dish.chain_list
        for chain in chains:
            await self.main_queue.put((dish, chain))
        self.is_free = False

    def check_if_free(self):
        """Проверяет можно ли танцеать, те все очереди пустые"""
        if not all(
                map(lambda p: p.empty(), (self.main_queue, self.maintain_queue, self.delivery_queue))):
            self.is_free = False
        else:
            self.is_free = True
        print("Можно ли танцевать? ", self.is_free)
        return self.is_free

    async def hello_from_qr_code(self, qr_code_data):
        await self.delivery_queue.put(qr_code_data)
        print("QR код обработан", time.time())

    async def wash_me(self, new_data):
        print("Получен запрос на помылку оборудования", new_data, time.time())

    async def controllers_alert_handler(self, cntrls_events):
        """Эта курутина обрабатывает уведомления от контроллеров: отказ оборудования и qr код """
        print("Переключились в контролеры", time.time())

        async def wait_for_qr_code(cntrls_events):
            """new_data - ckjdfhm {'ref_id': 65, 'pickup': 1}"""
            event_name = "qr_scanned"
            event = cntrls_events.get_dispatcher_event(event_name)
            while True:
                event_data = await event
                _, qr_code_data = event_data
                qr_code_data = qr_code_data["params"]
                await self.hello_from_qr_code(qr_code_data)

        async def wait_for_hardware_status_changed(cntrls_events):
            """new_data - словарь {'unit_name': 'owen_cell_2', 'status': 'broken'} """
            event_name = "hardware_status_changed"
            event = cntrls_events.get_dispatcher_event(event_name)
            while True:
                event_data = await event
                _, new_data = event_data
                await self.equipment.oven_broke_handler(new_data)

        async def wait_wash_requests(cntrls_events):
            """ """
            event_name = "equipment_washing_request"
            event = cntrls_events.get_dispatcher_event(event_name)
            while True:
                event_data = await event
                _, new_data = event_data
                await self.wash_me(new_data)

        qr_event_waiter = asyncio.create_task(wait_for_qr_code(cntrls_events))
        status_change_waiter = asyncio.create_task(wait_for_hardware_status_changed(cntrls_events))
        washing_request = asyncio.create_task(wait_wash_requests(cntrls_events))
        await asyncio.gather(qr_event_waiter, status_change_waiter, washing_request)

    async def cooking_immediately_execute(self):
        while True:
            while not self.immediately_executed_queue.empty():
                print("В срочной очереди появился чейн", time.time())
                print("Размер очереди", self.immediately_executed_queue.qsize())
                chain_to_do = await self.immediately_executed_queue.get()
                if isinstance(chain_to_do, tuple):
                    task, params = chain_to_do
                    print("В срочной очереди", task, time.time())
                    await asyncio.create_task(task(params))
                if isinstance(chain_to_do, types.MethodType):
                    print("В срочной очереди", chain_to_do, time.time())
                    await asyncio.create_task(chain_to_do())
            await asyncio.sleep(0.5)

    async def usual_cooking(self):
        while True:
            print("Работает cooking", time.time())
            self.is_free = self.check_if_free()
            if self.is_free:
                print("Танцуем")
                await RA.dance()
            else:
                # запустить мeтод где RA, какой захват и другую подготовительную работу
                if not self.delivery_queue.empty():
                    print("Выдаем заказ")
                    await self.delivery_queue.get()
                    await asyncio.sleep(5)
                elif not self.main_queue.empty():
                    print("Вернулись в очередь main")
                    dish, chain_to_do = await self.main_queue.get()
                    # print("Это блюдо", dish)
                    # print("Это тип чейна", type(chain_to_do))
                    if dish.status != "failed_to_be_cooked":
                        print("Готовим блюдо", dish.id)
                        if isinstance(chain_to_do, tuple):
                            chain, params = chain_to_do
                            _, cutting_program, storage_adress = params
                            print("Начинаем готовить", _.upper())
                            # await chain(dish, storage_adress, cutting_program)
                            await chain(storage_adress, cutting_program, self)
                        else:
                            # await chain_to_do(dish)
                            await chain_to_do(self)
                    else:
                        continue

                elif not self.maintain_queue.empty():
                    print("Моем или выкидываем пиццу")

    async def cooking(self):
        """Эта курутина обеспеивает вызов методов по приготовлению блюд и другой важной работе"""

        while True:
            print("Работает cooking", time.time())
            # time_limit = None

            # while not self.immediately_executed_queue.empty():
            #     chain_to_do = await self.immediately_executed_queue.get()
            #     if isinstance(chain_to_do, tuple):
            #         task, params = chain_to_do
            #         await asyncio.create_task(task(params))
            #     if isinstance(chain_to_do, types.MethodType):
            #         await asyncio.create_task(chain_to_do())

            self.is_free = self.check_if_free()
            if self.is_free:
                print("Танцуем")
                await RA.dance()
            else:
                # запустить мeтод где RA, какой захват и другую подготовительную работу
                if not self.delivery_queue.empty():
                    print("Выдаем заказ")
                    await self.delivery_queue.get()
                    await asyncio.sleep(5)
                elif not self.main_queue.empty():
                    print("Вернулись в очередь main")
                    dish, chain_to_do = await self.main_queue.get()
                    # print("Это блюдо", dish)
                    # print("Это тип чейна", type(chain_to_do))
                    if dish.status != "failed_to_be_cooked":
                        print("Готовим блюдо", dish.id)
                        if isinstance(chain_to_do, tuple):
                            chain, params = chain_to_do
                            _, cutting_program, storage_adress = params
                            print("Начинаем готовить", _.upper())
                            # await chain(dish, storage_adress, cutting_program)
                            await chain(storage_adress, cutting_program, self)
                        else:
                            # await chain_to_do(dish)
                            await chain_to_do(self)
                    else:
                        continue

                elif not self.maintain_queue.empty():
                    print("Моем или выкидываем пиццу")

    """Валиация qr кода
       входные данные: чек код заказа и номер пункта выдачи
       выходные данные: сообщение контроллеру, запускается выдача заказа, если он готов, выдача подарка, если произошла ошибка
       ORDER_STATUS = ["received", "cooking", "ready", "informed", "packed", "wait to delivery", "delivered", "closed",
                       "failed_to_be_cooked", "not_delivered"]
       добавить статус "time_is_up"
       """

    STATUS_FOR_CNTRL = {"ready": "заказ готов, скоро будет доставлен",
                        "failed_to_be_cooked": "не смогли приготовить",
                        "cooking": "находится в процессе готовки", "time_is_up": "время получения заказа истекло",
                        "delivered": "заказ уже получен", "not_found": "заказ не найден"}

    async def qr_code_alarm(self):
        """ Ожидаем получения qr кода от контроллера"""
        print("Мониторим есть ли запрос qr code")
        while True:
            # тут какая то классная команда контроллерам, ниже просто симуляция работы
            await asyncio.sleep(30)
            # {"ref_id": 12, "pickup": 1} взяты для примера
            self.check_order_status({"ref_id": 12, "pickup": 1})

    def check_order_status(self, params):
        """Этот метод проверяет, есть ли заказ с таким чек кодом в current_orders_proceed.
        Входные данные params: полученный от контроллера словарь с чек кодом заказа и окном выдачи
        "ref_id": int, "pickup": int"""
        order_check_code = params["ref_id"]
        pickup_point = params["pickup"]
        if order_check_code in self.current_orders_proceed:
            print("Валидный qr code")
            order_status = self.current_orders_proceed[order_check_code].status
            return self.order_status_handler(order_status, order_check_code)
        else:
            return self.status_to_cntrl("not found")

    def order_status_handler(self, order_status, order_check_code):
        """Этот метод анализирует статус и запускает обработчик отправляет значение контролеру"""
        if order_status == "ready":
            print("Валидный qr code, надо выдать заказ")
            self.orders_requested_for_delivery[order_check_code] = order_check_code
            return self.status_to_cntrl("ready")
        elif order_status == "packed" or order_status == "wait to delivery":
            return self.status_to_cntrl("ready")
        elif order_status == "cooking" or order_status == "received":
            return self.status_to_cntrl("cooking")
        elif order_status == "failed_to_be_cooked":
            self.present_delivery_handler()
            return self.status_to_cntrl("failed_to_be_cooked")
        else:
            return self.status_to_cntrl(order_status)

    async def status_to_cntrl(self, status_of_order):
        """Передает контроллу значение, на основании которого пользователю выводится информация о заказе"""
        print("контроллеру передано сообщение: ", self.STATUS_FOR_CNTRL[status_of_order])
        # обращеноие к контролу

    # не надо вызывать, поскольку постоянно идет проверка на наличие заказов в orders_requested_for_delivery
    # async def order_delivery_handler(self):
    # """Обрабатывает процедуру получения заказа - Настя"""
    # print("получение заказа")
    # pass

    async def present_delivery_handler(self):
        """Обрабатывает процедуру получения подарка"""
        print("получение подарка")
        pass
