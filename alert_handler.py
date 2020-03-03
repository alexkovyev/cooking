"""Этот модуль описывает поток мониторнга уведомлений от модуля Controllers.
Типы покрываемых уведомлений (требует подтверждения)
- exception (отказе оборудования, см вопрос ниже)
- данные qr кода на получение заказа (входные данные: json "ref id": номер пункта выдачи).
Вся(!) валидация qr кода реализована на стороне Controllers (а. распознан ли код,
b. истек ли срок действия, с. заказ уже выдан. Вывод на экран сообщения о результате валидации также осуществляет
модуля Controllers. НО если контролеры не валидируют готов заказ или нет, получается валиадция на обох сторонах.
    ВОПРОСЫ:
1. тип сообщения  от блока контролера (json, строка, еще что то?)
2. описать класс EquipmentExceptions, какие exceptions кроме отказа оборудования будут, структура сообщения.

"""

from main_order_handler import TodaysOrders


def main_alert_handler():
    """мониторит все уведомления от блока Controllers, определяет какое и вызывает соответствующую функцию обработчик
    :return handler()
     """
    pass





def error_handler():
    """Обрабатывает ошибки (не описано)"""
    pass


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
            raise Exception
    #
    # def setdefault(self, key, default=None):
    #     try:
    #         return self[key]
    #     except KeyError:
    #         self[key] = default
    #     return default

    def order_status_evaluation(self):
        """Проверяет статус заказа"""
        self.order_status = TodaysOrders.current_orders_proceed[self.order_refid] if self.order_refid in \
                                                                                     TodaysOrders.current_orders_proceed else "Not found"

    def order_delivery_handler(self):
        """Обрабатывает процедуру получения заказа (не описано)"""
        pass

    def order_status_handler(self,  ORDER_STATUSES_REPORTS):
        """Этот метод анализирует статус и запускает обработчик"""
        if self.order_status == "ready":
            self.order_delivery_handler()
            return "Сообщение о том, что заказ скоро будет доставлен"
        else:
            return  ORDER_STATUSES_REPORTS[self.order_status]
