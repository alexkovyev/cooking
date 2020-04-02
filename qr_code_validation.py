"""Этот модуль описывает процедуру валиации qr кода

Нужно написать:
- метод, вызываемый контролерами (то есть перечень всех шагов, обычно самый последний после всех входящих методов)
- перечень всех шагов, которые нужно сделать для валидации и вывода сообщения на экран

входные данные: "ref id"и номер пункта выдачи

Нужно проверить: есть ли такой заказ в TodaysOrders.current_orders_proceed, определить статус, вывести сообщение на
экран
Подумать, какие ошибки могут быть
"""

from PBM_main import TodaysOrders


class QrcodeValidations(object):
    """Этот класс валидирует полученный от конролеров qr code и возвращает сообщение для экрана выдачи."""

    ORDER_STATUSES_REPORTS = {"ready": "ваш заказ готов", "failed_to_be_cooked": "мы не смогли его приготовить"}

    def __init__(self):
        self.order_refid = None
        self.pickup_point = None
        self.order_status = None

    def qr_validation(self, message):
        """Этот метод валидирует qr код
        Получает словарь: {"rfid": int, "pickup-point": int}
        """
        try:
            self.order_refid = message["refid"]
            self.pickup_point = message["pickup-point"]
        except KeyError:
            # message read error
            # logging
            raise Exception("код не найден, делай запрос в БД")

    def order_status_evaluation(self):
        """Проверяет статус заказа"""
        self.order_status = TodaysOrders.current_orders_proceed[self.order_refid] if self.order_refid in \
                                                                                     TodaysOrders.current_orders_proceed else "Not found"

    def order_status_handler(self, ORDER_STATUSES_REPORTS):
        """Этот метод анализирует статус и запускает обработчик"""
        if self.order_status == "ready":
            self.order_delivery_handler()
            return "Сообщение о том, что заказ скоро будет доставлен"
        else:
            return ORDER_STATUSES_REPORTS[self.order_status]

    def order_delivery_handler(self):
        """Обрабатывает процедуру получения заказа (не описано)"""
        pass
