import datetime

class BaseOrder(object):
    """Этот класс представляет шаблон заказа, формируемого в среде окружения для каждого полученного заказа
    Статусы заказа (записываются в БД)
    "received" - получен, то есть создан экземпляр класса Order, отсортирован
    "cooking" - готовится, то есть RoboticArm уже начал с ним работу или он выпекается
    "ready" - выпечка завершена для обоих блюд
    "informed" - объявлено уведомление о готовности заказа на TV (название в разработке)
    "packed" - упакован
    "wait to delivery"- доставлен в пункт выдачи по запросу qr кода.
    "delivered" -  получено подтверждение о получении клиентом (после анализа снимка ячейки)
    "closed" - завершен (поле в разработке, предполагаются какие то действия по закрытию заказа, если нет, статус удалим)
    "failed_to_be_cooked" - не получилось приготовить
    "not_delivered" - заказ не получен клиентом
    ORDER_STATUS описывается в БД кодом
    """
    ORDER_STATUS = ["received", "cooking", "ready", "informed", "packed", "wait to delivery", "delivered", "closed",
                    "failed_to_be_cooked", "not_delivered"]

    def __init__(self, new_order, ovens_reserved):
        self.ref_id = new_order["refid"]
        self.dishes = self.dish_creation(new_order, ovens_reserved)
        # вариант из ORDER_STATUS

        # self.status: str
        # self.oven_liquidation_time: datetime
        # self.liquidation_time_pick_point: datetime
        # self.pickup_point: int
        # self.delivery_time: datetime

    def dish_creation(self, new_order, ovens_reserved):
        """Creates list of dishes in order"""
        if len(new_order["dishes"]) == 2:
            self.dishes = [BaseDish(dish, ovens_reserved[index]) for index, dish in enumerate(new_order["dishes"])]
        else:
            self.dishes = [BaseDish(new_order["dishes"][0], ovens_reserved[0])]
        return self.dishes

    def upload_data_from_db(self):
        """Запускается процедура загрузки данных из БД для блюд и компонентов. Или нужно в дочернем классе сделать? """
        pass

    def is_order_ready(self):
        """Boolean. Если оба блюда готовы, то готово, можно выдавать. Поменять статус self.status на ready
        След шаг: отправь на  телевизор (inform_tv_order_is_ready) """
        pass

    def is_order_failed(self):
        """Определяет что заказ не выполнен. Поменять статус self.status на "failed_to_be_cooked". Запускает
        failed_delivery_handler    ДОПИСАТЬ!!!!"""
        pass

    def inform_tv_order_is_ready(self):
        """отправляет сигнал о готовности блюда на телевизор, Поменять статус self.status на "informed"
         След шаг: запускает таймер отчета времени на забор заказа """
        pass

    def set_oven_timer_for_liquidation(self):
        """запускает таймер на ликвидацию зазака. 30 минут с момента. 30 минут хранится в переменной settings.py
        Таймер делаем отдельным воркером (потоком)? """
        pass

    def is_order_packed(self):
        """Проверяет все ли блюда упакованы, меняет статус на "packed"
         ВОПРОС: как происходит сообщение контролерам о том, что заказ можно выдавать?"""
        pass

    def is_order_in_pickup_point(self):
        """Проверяет доставлен ли все блюда заказа в ячейку выдачи. Меняет статус на "wait to delivery.
        Дожен сообщить контролеру о том, что можно сообщение выводить
        Запускает таймер на время забора заказа клиентом"""
        pass

    def pickup_point_checking(self):
        """Проверяет забран ли заказ, вне блока
        должно посылать сигнал о том, что заказ забрали (изменить статус) """
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

    def __str__(self):
        return f"Заказ {self.ref_id}"


class BaseDish(object):
    """Этот класс представляет собой шаблон блюда в заказе."""
    DISH_STATUSES = ["received", "cooking", "failed_to_cook", "ready", "packed"]

    def __init__(self, dish_data, free_oven):
        self.dough = BaseDough(halfstuff_id=dish_data[0])
        self.sauce = dish_data[1]
        self.filling = dish_data[2]
        self.additive = dish_data[3]

        self.oven_unit = free_oven

    # def oven_reserve_for_dish(self, free_oven):
    #     """ Метод вызываем equipment.oven_reserve()"""
    #     self.oven_unit = free_oven.get_first_free_oven()
    #     free_oven.oven_reserve(self.oven_unit)
    #     return self.oven_unit

    def __str__(self):
        return f"Тесто {self.dough}"

    def __repr__(self):
        return f"Блюдо состоит из {self.dough} \n Зарезервирована печь {self.oven_unit}"

# class BaseDish(object):
#     """Этот класс представляет собой шаблон блюда в заказе."""
#     DISH_STATUSES = ["received", "cooking", "failed_to_cook", "ready", "packed"]
#
#     def __init__(self):
#         self.dough: object
#         self.sauce: object
#         self.filling: object
#         self.additive: object
#
#         self.status: str
#         self.oven_unit: int
#         self.time_starting_baking: datetime
#         # у каждой ячейки выдачи есть 2 "лотка", нужно распределить в какой лоток помещает блюдо
#         self.pickup_point_unit: int
#         # тут собираются в каком то виде все чейны, каждый элемент списка атомарен
#         self.chain = []
#
#     def oven_reserve_for_dish(self):
#         """ Метод вызываем equipment.oven_reserve()
#         """
#         pass
#
#     def dish_chain_create(self):
#         """Тут собираем вызов функций по готовке блюда"""
#         pass
#
#
class BasePizzaPart(object):
    """Базовый класс компонента пиццы.
    self.halfstuff_cell: строка, передаваемая robotic Arm
    считаем, что за искл начинки всего по 1 порции (указано в portion_qt"""

    PORTION_QT = 1

    def __init__(self, halfstuff_id = 23,
                 halfstuff_cell="ячейка A1 3 из 6"):
        # нужен ли id?
        # self.refid = int
        self.halfstuff_id = halfstuff_id
        self.halfstuff_cell = halfstuff_cell
        # self.chain = ["структура данных для чейна пока не определена"]
        # нужно ли это время? где используем
        # self.cooking_duration: datetime


    def checking_available(self):
        """Эта функция делает проверяет есть ли доступные полуфабрикаты и как то обновляет резерв (см вопрос про
        резерв)"""
        pass

    def halfstuff_cell_evaluation(self):
        """Эта группа фнукций определеяет и назначает ячейку пф."""
        pass

    def chain_update(self):
        """Эта функция обновляет чейн этапа с учетом назнаенного полуфабриката"""
        pass


class BaseDough(BasePizzaPart):
    """Этот класс содержит информацию о тесте, которое используется в заказанном блюде"""

    def __init__(self, halfstuff_id):
        super().__init__(halfstuff_id)

    def __repr__(self):
        return f"Тесто {self.halfstuff_id}"


class BaseFilling(BasePizzaPart):
    """Этот класс содержит информацию о начинке. НУЖНЫ ответы о начинке БД"""

    def __init__(self):
        super().__init__()
        # тут хранится словарь? с перечнем ингредиентов и кол-вом по рецепту
        self.halfstuff_cell_id = []

    def halfstuff_cell_evaluation(self):
        """Отдельная группа функций по назначению пф, так как он не один, а несколько """
        pass


class BaseSauce(BasePizzaPart):
    """Этот класс содержит инфорамцию об используемом соусе"""

    def __init__(self):
        super().__init__()
    pass

class BaseAdditive(BasePizzaPart):
    """Этот класс описывает добавку"""

    def __init__(self):
        super().__init__()
    pass