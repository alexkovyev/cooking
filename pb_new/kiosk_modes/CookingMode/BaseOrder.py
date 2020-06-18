import asyncio
import time


class BaseOrder(object):
    """Этот класс представляет шаблон заказа"""
    ORDER_STATUS = ["received", "cooking", "ready", "informed", "packed", "wait to delivery", "delivered", "closed",
                    "failed_to_be_cooked", "not_delivered"]

    def __init__(self, new_order, ovens_reserved):

        self.ref_id = new_order["refid"]
        self.dishes = self.dish_creation(new_order["dishes"], ovens_reserved)
        self.status = "received"
        self.pickup_point = None
        self.order_ready_monitoring = []

    def dish_creation(self, dishes, ovens_reserved):
        """Creates list of dishes objects in order"""

        self.dishes = [BaseDish(dish_id, dishes[dish_id], ovens_reserved[index])
                       for index, dish_id in enumerate(dishes)]
        return self.dishes

    async def create_monitoring(self):
        for dish in self.dishes:
            is_dish_ready = asyncio.Event()
            dish.is_dish_ready = is_dish_ready
            self.order_ready_monitoring.append(is_dish_ready)
        return self.order_ready_monitoring

    async def dish_readiness_monitoring(self):
        print("Запущен СТОРТОВЫЙ МОНИТОРИНГ")
        while not all in self.order_ready_monitoring:
            print("Блюда все еще готовятся")
            await asyncio.sleep(1)
        print("Сработало событие ЗАКАЗ ГОТОВ", time.time())

    # Алина код
    def change_status(self, new_status):
        """Метод для смены статуса заказа
        Возвращается true, если смена статуса прошла успешно, и false, если такой статус не прдусмотрен
        Вызывается после метода can_change"""
        if new_status in self.ORDER_STATUS:
            self.status = new_status
            return True
        return False

    # Алина код
    def can_change(self, new_status):
        """Метод, который проверяет, можно ли изменить статус заказа на new_status
        Возвращается true, если сменить можно, и false, если статусы блюд не соответствуют новому статусу заказа"""
        SAME_STATUS = ["ready", "packed", "wait to delivery", "failed_to_be_cooked", "time_is_up"]
        if len(self.dishes) == 1:
            if new_status in SAME_STATUS:
                if self.dishes[0].status == new_status:
                    return True
                return False
            elif new_status == "cooking":
                if self.dishes[0].status == "cooking":
                    return True
                return False
            else:
                return True
        else:  # для двух блюд в заказе:
            if new_status in SAME_STATUS:
                if self.dishes[0].status == self.dishes[1].status == new_status:
                    return True
            else:
                if new_status == "partially_ready":
                    if (self.dishes[0].status == "ready" or self.dishes[1].status == "ready") and \
                            (self.dishes[0].status == "failed_to_be_cooked" or self.dishes[1].status
                             == "failed_to_be_cooked"):
                        return True
                    return False
                elif new_status == "cooking":
                    if self.dishes[0].status == "cooking" or self.dishes[1].status == "cooking":
                        return True
                    return False
                else:
                    return True

    def __repr__(self):
        return f"Заказ № {self.ref_id}"
