"""Этот модуль управляет заказами и блюдами"""

import datetime


class BaseOrder(object):
    """Этот класс представляет шаблон заказа, формируемого в среде окружения для каждого полученного заказа
    ВОПРОС: что мы записываем в БД и с какой периодичностью, как выглядит запись о заказе в БД"""
    ORDER_STATUS = ["received", "cooking", "ready", "wait to delivery", "delivered", "closed", "failed_to_be_cooked",
                    "not_delivered"]

    def __init__(self):
        self.ref_id: int
        self.dish_1: object.__class__Dish__
        self.dish_2: object.__class__Dish__
        # вариант из ORDER_STATUS
        self.status: str
        self.liquidation_time_pick_point: datetime
        self.pickup_point: int
        self.delivery_time: datetime

    def is_order_ready(self):
        """Boolean. Если оба блюда готовы, то готово, можно выдавать. Поменять статус self.status на ready
        След шаг: отправь на  телевизор (inform_tv_order_is_ready) """
        pass

    def is_order_failed(self):
        """Определяет что заказ не выполнен. Поменять статус self.status на "failed_to_be_cooked". Запускает
        failed_delivery_handler    ДОПИСАТЬ!!!!"""
        pass

    def inform_tv_order_is_ready(self):
        """отправляет сигнал о готовности блюда на телевизор, Поменять статус self.status на "wait to delivery
         След шаг: запускает таймер отчета времени на забор заказа """
        pass

    def set_oven_timer_for_liquidation(self):
        """запускает таймер на ликвидацию зазака. 30 минут с момента. 30 минут хранится в переменной settings.py
        Таймер делаем отдельным воркером (потоком)? """
        pass

    def pickup_point_checking(self):
        """Проверяет забран ли заказ, вне блока
        должно посылать сигнал о том, что заказ забрали (изменить статус) УВЯЗАТЬ С ОБРАБОТЧИКОМ ПОЛУЧЕНИЯ ЗАКАЗА"""
        pass

    def order_delivered(self):
        """Меняет статус заказа доставлен, Поменять статус self.status на "delivered", обнуляет счетчик
        self.liquidation_time_pick_point, проставляет время получения self.delivery_time Нужна ли доп информация о
        заказе кроме времени получения?"""
        pass

    def order_closing(self):
        """функция обрабатывает закрытие заказа после получения покупателем. Поменять статус self.status на "closed"
         Что тут делаем по сути? Как записываем в бд, удаляем сами объект или ждем сборщика мусора?"""
        pass


class BaseDish(object):
    """Этот класс представляет собой шаблон блюда в заказе."""
    DISH_STATUSES = ["received", "cooking", "ready", "delivered", "failed_to_cook"]

    def __init__(self):
        # есть ли в БД у блюда какой то номер, присвоенный ранее. Как хранится информация о заказе в БД
        self.id = int

        self.dough: object
        self.sauce: object
        self.filling: object
        self.additive: object

        self.status: str
        self.oven_unit: object
        self.time_starting_baking: datetime
        self.pickup_point_unit: int

        # тут собираются в каком то виде все чейны, каждый элемент списка атомарен
        self.chain = []

    def oven_reserve_for_dish(self):
        """Это группа функций назначает печь для каждого блюда. ДОПИСАТЬ:
        - как смарт экран проверяет печи, есть ли кокой то резерв?
        - как в БД описывается
        - как органзована работа со временем занятости печи (когда занята, когда свободная
        """
        pass


class BasePizzaPart(object):
    """Базовый класс компонента пиццы"""

    def __init__(self):
        self.refid = int
        self.halfstuff_cell_id = int
        self.chain = ["структура данных для чейна пока не определена"]
        # нужно ли это время? где используем
        self.cooking_duration: datetime

    def upload_dough_info(self):
        """Эта функция делает select из БД. Таблица Dough, загружает:
         - чейн для теста
         - данные о времени (если они в отдельной таблице)
         - данные о том, какой п-ф нужен
         Коннект в отдельной фнукции
         """
        # database_connect()
        pass

    def checking_available(self):
        """Эта функция делает проверяет есть ли доступные полуфабрикаты и как то обновляет резерв (см вопрос про
        резерв)"""
        pass

    def halfstuff_cell_evaluation(self):
        """Эта группа фнукций определеяет и назначает ячейку пф. Возможно перенести в mixin"""
        pass

    def chain_update(self):
        """Эта функция обновляет чейн этапа с учетом назнаенного полуфабриката"""
        pass


class BaseDough(BasePizzaPart):
    """Этот класс содержит информацию о тесте, которое используется в заказанном блюде"""
    pass


class BaseFilling(BasePizzaPart):
    """Этот класс содержит информацию о начинке. НУЖНЫ ответы о начинке БД"""
    pass


class BaseSauce(BasePizzaPart):
    """Этот класс содержит инфорамцию об используемом соусе"""
    pass


class TodaysOrders(object):
    """Этот класс содержит информацию о том, какие блюда готовятся в текущий момент. После обработки заказа,
    заказ удаляется из self.current_orders_proceed"""

    def __init__(self):
        self.current_orders_proceed = {{}}
        pass

    def checking_order_for_double(self):
        """Этот метод проверяет есть ли уже заказ с таким ref id в обработке
        :return bool"""
        pass


class TodaysDishes(object):
    """Этот класс содержит информацию о том, какие блюда готовятся в текущий момент. После обработки заказа он
    удаляется"""
    pass
