import asyncio
import time

from recipe_class import Recipy
import PbmError


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

        self.ref_id = new_order["refid"]
        self.dishes = self.dish_creation(new_order["dishes"], ovens_reserved)
        self.status = "received"
        self.liquidation_time_pick_point = None
        self.pickup_point = None
        # self.delivery_time: datetime

    def dish_creation(self, dishes, ovens_reserved):
        """Creates list of dishes objects in order"""

        self.dishes = [BaseDish(dish_id, dishes[dish_id], ovens_reserved[index])
                       for index, dish_id in enumerate(dishes)]

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


class BaseDish(Recipy):
    """Этот класс представляет собой шаблон блюда в заказе."""
    DISH_STATUSES = ["received", "cooking", "failed_to_be_cooked", "ready",
                     "packed", "wait to delivery", "time_is_up"]

    def __init__(self, dish_id, dish_data, free_oven_id):
        super().__init__()
        self.id = dish_id
        # распаковываем данные о том, из чего состоит блюдо
        self.dough = BaseDough(dish_data["dough"])
        self.sauce = BaseSauce(dish_data["sauce"])
        self.filling = BaseFilling(dish_data["filling"])
        self.additive = BaseAdditive(dish_data["additive"])

        self.oven_unit = free_oven_id
        self.status = "received"
        self.chain_list = self.recipe_chain_creation()
        self.baking_program = dish_data["filling"]["cooking_program"]
        self.heating_program = dish_data["filling"]["heating_program"]
        self.stop_baking_time = None
        # у каждой ячейки выдачи есть 2 "лотка", нужно распределить в какой лоток помещает блюдо
        # self.pickup_point_unit: int

    def recipe_chain_creation(self):
        chain_list = []
        chain_list.append(Recipy.chain_get_dough_and_sauce)
        filling_chain = []
        for filling_item in self.filling.filling_content:
            filling_chain.append((Recipy.get_filling_chain, filling_item))
        return chain_list+filling_chain


    def status_change(self, new_status):
        """Метод меняет статус блюда.
        что то коряво, переделать
        """
        try:
            if new_status in self.DISH_STATUSES:
                self.status = new_status
                return self.status
            else:
                raise PbmError.PbmFatalError("Предлагаемый статус блюда не найден ")
        except PbmError.PbmFatalError:
            assert PbmError.PbmFatalError
        try:
            print("Запысываем статус в БД")
            # обновление статуса в БД
        except PbmError.DataBaseError:
            print("Ошибка БД")


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
    """Этот класс содержит информацию о начинке.
    filling_data["content"] содержит кортеж котреж словарей
    Вложенный словарь содержит информцию об id_пф и словарь для нарезки
    (halfstaff_id, {"cutting_program_id":str, "duration": int})
    """

    def __init__(self, filling_data):
        self.filling_id = filling_data["id"]
        self.filling_content = filling_data["content"]
        self.cell_data_unpack()

    def cell_data_unpack(self):
        """Элемент списка начинки выглядит вот так, последний элемент - это место хранения
        [6, {'program_id': 2, 'duration': 10}, ('d4', (3, 4))]"""
        input_data = (
                      ("d4", (3,4)), ("a4", (3,4)), ("t4", (3,4)),
                      ("b4", (1,1)), ("a4", (1,1)), ("c4", (2,1))
                      )

        self.filling_content = [item + [value] for item, value in zip(self.filling_content, input_data)]

    def __repr__(self):
        return f"Начинка {self.filling_id}"


class BaseAdditive(BasePizzaPart):
    """Этот класс описывает добавку"""

    def __init__(self, additive_data):
        self.halfstuff_id = additive_data["id"]
        self.halfstuff_cell = None

    def __repr__(self):
        return f"Добавка {self.halfstuff_id}"

