"""Этот модуль управляет заказами и блюдами"""

from base_order import BaseOrder
from equipment import Oven

from settings import QT_DISH_PER_ORDER


class TodaysOrders(Oven):
    """Этот класс содержит информацию о том, какие блюда готовятся в текущий момент, содержит информацию о печах и
    показываает время работы коиска. После завешения заказа, он удаляется из self.current_orders_proceed
    """

    def __init__(self):
        print("Start!")
        # self.current_orders_proceed = {"refid": "object_order"}
        super().__init__()
        self.current_orders_proceed = {}
        self.current_dishes_proceed = []
        self.time_to_cook_all_dishes_left = 0
        # self.ovens_available = {i:{"oven_id":i, "status": "free"} for i in range (1,22)}

    def checking_order_for_double(self):
        """Этот метод проверяет есть ли уже заказ с таким ref id в обработке ил в БД (разбить на 2 или 3 метода)
        :return bool"""
        pass

    def create_new_order(self, new_order, QT_DISH_PER_ORDER):
        """Этот метод создает экземпляр класса Order и заносит его в словарь self.current_orders_proceed"""
        try:
            ovens_reserved = [self.oven_reserve() for dish in new_order["dishes"]]
            order = BaseOrder(new_order, ovens_reserved, QT_DISH_PER_ORDER)
            print("Создан заказ", order)
            print("Блюда в заказе", order.dishes)
            if order:
                self.current_orders_proceed[order.ref_id] = order
        # придумать ошибки какие могут быть
        except ValueError:
            pass

    def fill_current_dishes_proceed(self):
        """ Добавляет блюда заказа в self.current_dishes_proceed"""
        pass

    def func_name(self):
        pass

