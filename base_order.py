import time

from recipe_class import Recipy
from settings import QT_DISH_PER_ORDER


class BaseOrder(object):
    """Этот класс представляет шаблон заказа, формируемого в среде окружения для каждого полученного заказа Статусы
    заказа (записываются в БД) "received" - получен, то есть создан экземпляр класса Order, отсортирован "cooking" -
    готовится, то есть RoboticArm уже начал с ним работу или он выпекается "ready" - выпечка завершена для обоих блюд
    "informed" - объявлено уведомление о готовности заказа на TV (название в разработке) "packed" - упакован "wait to
    delivery"- доставлен в пункт выдачи по запросу qr кода. "delivered" -  получено подтверждение о получении
    клиентом (после анализа снимка ячейки) "closed" - завершен (поле в разработке, предполагаются какие то действия
    по закрытию заказа, если нет, статус удалим) "failed_to_be_cooked" - не получилось приготовить "not_delivered" -
    заказ не получен клиентом ORDER_STATUS описывается в БД кодом
    """
    ORDER_STATUS = ["received", "cooking", "ready", "informed", "packed", "wait to delivery", "delivered", "closed",
                    "failed_to_be_cooked", "not_delivered"]

    def __init__(self, new_order, ovens_reserved):
        self.qt_dish_per_order = QT_DISH_PER_ORDER

        self.ref_id = new_order["refid"]
        self.dishes = self.dish_creation(new_order, ovens_reserved)
        self.status = "received"
        self.liquidation_time_pick_point = None
        self.pickup_point = None
        # self.delivery_time: datetime

    def dish_creation(self, new_order, ovens_reserved):
        """Creates list of dishes objects in order"""
        # сделано так, тк номер в списке придает "уникальность" id блюду
        if len(new_order["dishes"]) == self.qt_dish_per_order:
            self.dishes = [BaseDish(dish, ovens_reserved[index], index) for index, dish in enumerate(new_order[
                                                                                                         "dishes"])]
        else:
            self.dishes = [BaseDish(new_order["dishes"][0], ovens_reserved[0], index=1)]
        return self.dishes

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

    def __repr__(self):
        return f"Заказ № {self.ref_id}"


class BaseDish(Recipy):
    """Этот класс представляет собой шаблон блюда в заказе."""
    DISH_STATUSES = ["received", "cooking", "failed_to_cook", "ready", "packed"]

    def __init__(self, dish_data, free_oven_id, index):
        # создаем уникальное имя блюда
        self.id = f"{index}{round(time.time() * 1000)}"
        # распаковываем данные о том, из чего состоит блюдо
        self.dough = BaseDough(dish_data["dough"])
        self.sauce = BaseSauce(dish_data["sauce"])
        self.filling = BaseFilling(dish_data["filling"])
        self.additive = BaseAdditive(dish_data["additive"])

        self.oven_unit = free_oven_id
        self.status = "received"
        # self.chain_list = [self.get_dough(self.id, self.oven_unit, 6)]
        # (program_id, plan_duration) если плановая будет не нужна, удалить и исправить индексы контроллеров
        self.baking_program = dish_data["filling"]["cooking_program"]
        self.heating_program = dish_data["filling"]["heating_program"]
        self.stop_baking_time = None
        # у каждой ячейки выдачи есть 2 "лотка", нужно распределить в какой лоток помещает блюдо
        # self.pickup_point_unit: int
        # self.plan_duration = sum([self.dough.dough_plan_duration, self.sauce.sauce_plan_duration])

        super().__init__()

    def halfstuff_cell_evaluation(self):
        """Эта группа фнукций запускает процедуру назначения пф и назначает ячейку для каждого пф."""
        # result = do_some_great_db_procedure
        # unpack_results если нужно
        # self.dough.halfstuff_cell = result[0]
        # self.sauce.halfstuff_cell = result[0]
        # self.sauce.halfstuff_cell = result[1]
        # self.filling = None
        # self.additive.halfstuff_cell = result[3]
        pass

    def __repr__(self):
        return f"Блюдо {self.id} состоит из {self.dough}, {self.sauce}, {self.filling}, {self.additive}  " \
               f"\"Зарезервирована печь\" {self.oven_unit} Статус {self.status}"



class BasePizzaPart(object):
    """Базовый класс компонента пиццы.
    self.halfstuff_id идентификационный номер полуфабриката
    self.halfstuff_cell: строка, передаваемая robotic Arm или контроллерам 'ячейка A1 3 из 6'
    считаем, что за искл начинки всего по 1 порции (указано в portion_qt"""

    def cell_evaluation(self):
        pass


class BaseDough(BasePizzaPart):
    """Этот класс содержит информацию о тесте, которое используется в заказанном блюде"""

    def __init__(self, dough_data):
        self.halfstuff_id = dough_data["id"]
        # self.halfstuff_cell хранит только место ячейки, при инициации None
        self.halfstuff_cell = 21
        self.recipe_data = dough_data["recipe"]

    def __repr__(self):
        return f"Тесто {self.halfstuff_id}"


class BaseSauce(BasePizzaPart):
    """Этот класс содержит инфорамцию об используемом соусе"""

    def __init__(self, sauce_data):
        self.sauce_id = sauce_data["id"]
        self.sauce_content = sauce_data["content"]
        # sauce_cell=[(1, 1), (2, 2)] 0 - id насосной станции, 1 - программа запуска
        # переписать название
        self.sauce_cell = self.unpack_data(sauce_data)
        self.sauce_recipe = sauce_data["recipe"]

    def unpack_data(self, sauce_data):
        """выводт данные в виде [(cell_id, program_id), (None, 3)]"""
        # переписать, временно

        a = sauce_data["recipe"]["content"]
        for_controllers = [(a[i]["sauce_station"], a[i]["program"]) for i in a]
        return for_controllers

    def __repr__(self):
        return f"Соус {self.sauce_id}"


class BaseFilling(object):
    """Этот класс содержит информацию о начинке."""

    def __init__(self, filling_data):
        self.filling_id = filling_data["id"]
        self.filling_content = filling_data["content"]
        # тут хранится словарь? с перечнем ингредиентов и кол-вом по рецепту
        self.filling_halfstuffs = {"halfstuff_1": ("расположение", "тип нарезки"),
                          "halfstuff_2": ("расположение", "тип нарезки")}

    def __repr__(self):
        return f"Начинка {self.filling_id}"


class BaseAdditive(BasePizzaPart):
    """Этот класс описывает добавку"""

    def __init__(self, additive_data):
        self.halfstuff_id = additive_data["id"]
        self.halfstuff_cell = None

    def __repr__(self):
        return f"Добавка {self.halfstuff_id}"

#
# class BaseDish(Recipy):
#     """Этот класс представляет собой шаблон блюда в заказе."""
#     DISH_STATUSES = ["received", "cooking", "failed_to_cook", "ready", "packed"]
#
#     def __init__(self, dish_data, free_oven_id, index):
#         super().__init__()
#         # создаем уникальное имя блюда
#         self.id = f"{index}{round(time.time() * 1000)}"
#         # распаковываем данные о том, из чего состоит блюдо
#         dough_id, sauce_id, filling_id, additive_id = dish_data
#         self.dough = BaseDough(halfstuff_id=dough_id)
#         self.sauce = BaseSauce(halfstuff_id=sauce_id)
#         self.filling = filling_id
#         self.additive = BaseAdditive(halfstuff_id=additive_id)
#
#         self.oven_unit = free_oven_id
#         self.status = "received"
#         # self.chain_list = [self.get_dough(self.id, self.oven_unit, 6)]
#         self.time_starting_baking = None
#         # у каждой ячейки выдачи есть 2 "лотка", нужно распределить в какой лоток помещает блюдо
#         # self.pickup_point_unit: int
#         self.plan_duration = sum([self.dough.dough_plan_duration, self.sauce.sauce_plan_duration])
#
#     def halfstuff_cell_evaluation(self):
#         """Эта группа фнукций запускает процедуру назначения пф и назначает ячейку для каждого пф."""
#         # result = do_some_great_db_procedure
#         # unpack_results если нужно
#         # self.dough.halfstuff_cell = result[0]
#         # self.sauce.halfstuff_cell = result[0]
#         # self.sauce.halfstuff_cell = result[1]
#         # self.filling = None
#         # self.additive.halfstuff_cell = result[3]
#         pass
#
#     def __repr__(self):
#         return f"Блюдо {self.id} состоит из {self.dough}, {self.sauce}, {self.filling}, {self.additive}  " \
#                f"\"Зарезервирована печь\" {self.oven_unit} Статус {self.status}"

