"""Этот модуль управляет заказами и блюдами"""


class TodaysOrders(object):
    """Этот класс содержит информацию о том, какие блюда готовятся в текущий момент. После обработки заказа,
    заказ удаляется из self.current_orders_proceed"""

    def __init__(self):
        self.current_orders_proceed = {"refid": "object_order"}
        pass

    def checking_order_for_double(self):
        """Этот метод проверяет есть ли уже заказ с таким ref id в обработке
        :return bool"""
        pass

    def qr_validation(self):
        """Этот метод валидирует qr-code """
        pass


class TodaysDishes(object):
    """Этот класс содержит информацию о том, какие блюда готовятся в текущий момент. После обработки заказа он
    удаляется"""

    def __init__(self):
        self.current_dishes_proceed = {{}}
    pass


class CurrentSituation(object):
    """Этот класс содержит информацию о том, что сейчас происходит в киоске"""

    def __init__(self):

        pass