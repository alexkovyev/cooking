"""Этот модуль управляет заказами и блюдами"""
import time
import asyncio

from base_order import BaseOrder
from equipment import Equipment


class PizzaBotMain(object):
    """Это основной класс блока.
    Этот класс содержит информацию о том, какие блюда готовятся в текущий момент, содержит информацию о печах и
    показываает время работы коиска. После завешения заказа, он удаляется из self.current_orders_proceed
    """

    def __init__(self, equipment_data, recipes):
        self.equipment = Equipment(equipment_data)
        # super().__init__(equipment_data)
        self.is_cooking_paused = False
        # все заказы за текущий сеанс работы, {id: BaseOrder}
        self.current_orders_proceed = {}
        # все неприготовленые блюда
        self.current_dishes_proceed = {}
        self.time_to_cook_all_dishes_left = 2300
        self.orders_requested_for_delivery = {}
        self.recipes = recipes

    def checking_order_for_double(self, new_order_id):
        """Этот метод проверяет есть ли уже заказ с таким ref id в обработке
        :return bool"""
        is_new_order = True if new_order_id not in self.current_orders_proceed.keys() else False
        return is_new_order

    async def get_order_content_from_db(self, new_order_id):
        """Этот метод вызывает процедуру 'Получи состав блюд в заказе' и возвращает словарь вида
        {"refid": 32131, "dishes": [(2, {"sauce_id":2, "sauce_content":[("id","qt"), ("id","qt")]},
                                   {"filling_id":1, "filling_content":((6,1),(4,1),(6,1),(9,2))}, 7),
                                    (1, 2, {"filling_id":2, "filling_content":((6,1),(4,1),(6,1),(9,2))}, 5)]}
        """
        new_order = {"refid": new_order_id,
                     "dishes": [
                         (2,
                          {"sauce_id": 2, "sauce_content": [(1, 5), (2, 25)]},
                         {"filling_id": 1, "filling_content": ((6, 1), (4, 1), (6, 1), (9, 2))},
                          7),
                         (1,
                          {"sauce_id": 1, "sauce_content": [(2, 10), (3, 20)]},
                          {"filling_id": 2, "filling_content": ((6, 1), (4, 1), (6, 1), (9, 2))},
                          5)
                     ]
                     }
        return new_order

    def create_new_order(self, new_order):
        """Этот метод создает экземпляр класса Order и заносит его в словарь self.current_orders_proceed
        @:params:
        new_order - это словарь с блюдами вида
        {"refid": 32131, "dishes": [(2, {"sauce_id":2, "sauce_content":[("id","qt"), ("id","qt")]},
                                   {"filling_id":1, "filling_content":((6,1),(4,1),(6,1),(9,2))}, 7),
                                    (1, 2, {"filling_id":2, "filling_content":((6,1),(4,1),(6,1),(9,2))}, 5)]}
        получаемый из БД в рамках метода get_order_content_from_db """

        try:
            # резервируем печи для заказа
            ovens_reserved = [self.equipment.oven_reserve() for dish in new_order["dishes"]]
            # создаем экземпляр класса заказа
            order = BaseOrder(new_order, ovens_reserved)
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

    def get_dish_recipe(self):

        pass


    #
    # def total_cooking_update(self):
    #     pass
    #
    # async def cooking_pause_handler(self):
    #     print("Приостанавливаем работу")
    #     #Controllers.disable_qrcode_validator()
    #     #RBA.go_to_transport_position()
    #     await asyncio.sleep(10)
    #     pass
    #
    # async def dish_delivery(self):
    #     print("Cooking: Обрабатываем сообщение от контроллера")
    #     print("классное сообщение от контролера - ВЫДАЧА заказа",
    #     self.orders_requested_for_delivery.popitem())
    #     await asyncio.sleep(5)
    #     print("ВЫДАЧА заказа завершена")
    #     print(time.time())
