"""Этот модуль управляет заказами и блюдами"""
import time
import asyncio

from base_order import BaseOrder
from equipment import Equipment


class TodaysOrders(Equipment):
    """Этот класс содержит информацию о том, какие блюда готовятся в текущий момент, содержит информацию о печах и
    показываает время работы коиска. После завешения заказа, он удаляется из self.current_orders_proceed
    """

    def __init__(self):
        print("Start!")
        super().__init__()
        self.is_cooking_paused = False
        # все заказы до того, как получены
        self.current_orders_proceed = {}
        # все неприготовленые блюда
        self.current_dishes_proceed = {}
        self.time_to_cook_all_dishes_left = 0
        self.orders_requested_for_delivery = {}


    def checking_order_for_double(self):
        """Этот метод проверяет есть ли уже заказ с таким ref id в обработке ил в БД (разбить на 2 или 3 метода)
        :return bool"""
        pass

    def create_new_order(self, new_order, QT_DISH_PER_ORDER):
        """Этот метод создает экземпляр класса Order и заносит его в словарь self.current_orders_proceed
        @:params:
        new_order - это словарь с блюдами вида {"refid": 32131, "dishes": [(2, 4, 6, 7), (1, 2, 4, 5)]}, получаемый
        из БД
        QT_DISH_PER_ORDER - это максимально возможное кол-во блюд в заказе."""

        try:
            # резервируем печи для заказа
            ovens_reserved = [self.oven_reserve() for dish in new_order["dishes"]]
            # создаем экземпляр класса заказа
            order = BaseOrder(new_order, ovens_reserved, QT_DISH_PER_ORDER)
            print("Создан заказ", order)
            print("Блюда в заказе", order.dishes)
            if order:
                # если заказ создан успешно, помещаем его в словарь всех готовящихся заказов
                self.current_orders_proceed[order.ref_id] = order
                # перемещаем заказы в словарь всех готовящихся блюд
                self.fill_current_dishes_proceed(order)
        # придумать ошибки какие могут быть
        except ValueError:
            pass

    def fill_current_dishes_proceed(self, order):
        """ Добавляет блюда заказа в self.current_dishes_proceed
        @:param order: экземпляр класса заказ, созданный в self.create_new_order"""

        for dish in order.dishes:
            self.current_dishes_proceed[dish.id] = dish

    def total_cooking_update(self):
        pass

    async def cooking_pause_handler(self):
        print("Приостанавливаем работу")
        #Controllers.disable_qrcode_validator()
        #RBA.go_to_transport_position()
        await asyncio.sleep(10)
        pass

    async def dish_delivery(self):
        print("Cooking: Обрабатываем сообщение от контроллера")
        print("классное сообщение от контролера - ВЫДАЧА заказа",
        self.orders_requested_for_delivery.popitem())
        await asyncio.sleep(5)
        print("ВЫДАЧА заказа завершена")
        print(time.time())
