"""Пока тут собрана информация о рецепте."""
import asyncio
import time

from RA import RA
from RA import RAError
from controllers import Controllers


class ConfigMixin(object):
    """Временное хранение идентификаторов оборудования"""
    CUT_STATION_ID = 1
    CAPTURE_STATION = 2
    MOVE_TO_CAPTURE_STATION_TIME = 5
    CHANGE_CAPTURE_TIME = 2
    PRODUCT_CAPTURE_ID = 1


class Recipy(ConfigMixin):
    """Основной класс рецепта, содержит все действия по приготовлению блюда"""

    def __init__(self):
        self.is_cut_station_free = asyncio.Event()
        self.time_limit = None

    @staticmethod
    async def get_move_chain_duration(place_to):
        """ Метод получает варианты длительности передвижения, выбирает тот, который
        удовлетвоаряет условиям
        :param place_to: str
        :return: int
        """
        current_destination = await RA.get_current_position()
        forward_destination = place_to
        possible_duration = await RA.get_position_move_time(current_destination, forward_destination)
        if possible_duration:
            duration = min(possible_duration)
        else:
            raise RAError
        return duration

    @staticmethod
    async def get_atomic_chain_duration(atomic_info):
        """

        :param atomic_info:
        :return:
        """
        duration = await RA.get_atomic_action_time(**atomic_info)
        if not duration:
            raise RAError
        return duration

    def choose_moving_time(self):
        """

        """
        pass

    async def move_to_object(self, place_to):
        """Эта функция описывает движение до определенного места."""
        forward_destination = place_to

        duration = await self.get_move_chain_duration(forward_destination)
        try:
            await RA.position_move(forward_destination, duration)
            print("RBA успешно подъехал к", forward_destination)
        except RAError:
            self.status = "failed_to_be_cooked"
            # есть ли какой то метод проверки работоспособности
            # что деламем? сворачиваем работу или продолжаем дальше
        return self.status

    async def atomic_chain_execute(self, atomic_params_dict):
        duration = await self.get_atomic_chain_duration(atomic_params_dict)
        try:
            await RA.atomic_action(**atomic_params_dict)
            print("Успешно выполнили атомарное действие")
        except RAError:
            self.status = "failed_to_be_cooked"
            print("Ошибка атомарного действия")
        return self.status

    async def get_vane_from_oven(self, *args):
        """Этот метод запускает группу атомарных действий RA по захвату лопатки из печи"""
        atomic_params = {"name": "get_vane_from_oven",
                          "place": self.oven_unit}
        self.status = await self.atomic_chain_execute(atomic_params)
        return self.status

    async def controllers_get_dough(self, *args):
        """отдает команду контролеру получить тесто"""
        print("получаем тесто у контрллеров")
        dough_point = self.dough.halfstuff_cell
        chain_result = await Controllers.give_dough(dough_point)
        if chain_result:
            print("взяли тесто у контроллеров")
        else:
            print("Ошибка получения теста у контроллеров")
            self.status = "failed_to_be_cooked"
        # запускает метод списать п\ф
        return self.status

    async def control_dough_position(self, *args):
        """отдаем команду на поправление теста"""
        atomic_params = {"name": "get_dough",
                         "place": self.dough.halfstuff_cell}
        self.status = await self.atomic_chain_execute(atomic_params)
        return self.status

    async def leave_vane_in_cut_station(self, *args):
        """отдаем команду оставить лопатку в станции нарезки"""
        atomic_params = {"name": "leave_vane_at_cut_station",
                         "place": self.CUT_STATION_ID}
        self.status = await self.atomic_chain_execute(atomic_params)
        return self.status

    async def give_sauce(self):
        """Вызов метода контроллеров для поливания соусом"""
        print("Начинаем поливать соусом", time.time())
        recipe = self.sauce.sauce_cell
        print("Данные об ячейке", recipe)
        print("Время начала поливки соусом контроллерами", time.time())
        result = await Controllers.give_sauce(recipe)
        if result:
            print("успешно полили соусом")
            self.is_cut_station_free.set()
        else:
            print("Не успешно полили соусом")
            self.status = "failed_to_be_cooked"
        return self.result

    async def chain_get_dough_and_sauce(self):
        """Подумать как разделить на 2 части"""
        print("Начинается chain Возьми тесто")
        self.status = self.status_change("cooking")
        chain_list = [(self.move_to_object, self.oven_unit),
                      (self.get_vane_from_oven, None),
                      (self.move_to_object, self.CUT_STATION_ID),
                      (self.controllers_get_dough, None),
                      (self.control_dough_position, None),
                      (self.move_to_object, self.CUT_STATION_ID),
                      (self.leave_vane_in_cut_station, None),
                      ]
        try:
            for chain in chain_list:
                if self.status != "failed_to_be_cooked":
                    chain, params = chain
                    self.status = await chain(params)
                else:
                    break
            self.status = asyncio.create_task(self.give_sauce())
        except RAError:
            print("Ошибка века")


class Filling(ConfigMixin):

    def __init__(self):
        self.result = True

    async def move_to_capture_station(self):
        """Едем до места хранения захватов"""
        print("Поехали к месту хранения захватов")
        CHAIN_ID = 1

        duration = self.MOVE_TO_CAPTURE_STATION_TIME
        destination = self.CAPTURE_STATION

        result = await RA.position_move(destination, duration)
        if result:
            print("RA успешно подъехал к станции захватов")
            # await self.take_capture()
            await Baking.new_run_baking(self)
        else:
            print("Ошибка подъезда к станции захватов")

    async def take_capture(self):
        """Меняем захват на тот, которым нужно брать п\ф. ВОПРОС: зависит ли захват от типа п\ф"""
        print("Берем захват для продукта")
        CHAIN_ID = 2

        launch_params = {"atomic_name": "change_capture",
                         "place":self.CAPTURE_STATION,
                         "capture_type": self.PRODUCT_CAPTURE_ID,
                         "duration": self.CHANGE_CAPTURE_TIME}

        # print(self.is_cut_station_ready)
        print("Ждем завершения станции нарезки", time.time())
        await self.is_cut_station_free.wait()
        print("Начинаем движение после контролеров соуса")
        result = await RA.atomic_action(**launch_params)
        if result:
            print("RA успешно подъехал к станции захватов")
            await self.get_vane_from_oven()
        else:
            print("Ошибка подъезда")

    async def get_product_capture(self):
        """Это метод-аккумулятор для запуска ВОЗЬМИ захват """
        print("Начинаем чейн возьми захват")
        await self.move_to_capture_station()
        print("Чейн возьми захват закончилися")

    async def go_to_fridge(self):
        """Едем к холодильнику за продуктом"""
        print("Поехали к холодильнику за продуктом")
        CHAIN_ID = 1

        duration = self.MOVE_TO_CAPTURE_STATION_TIME
        destination = self.CAPTURE_STATION

        self.result = await RA.position_move(destination, duration)
        if self.result:
            print("RA успешно подъехал к холодильнику")
            await self.get_product_from_fridge()
        else:
            print("ERROR Ошибка подъезда к холодильнику")
        return self.result

    async def get_product_from_fridge(self):
        """Группа действий по доставанию продукта из холодильника """
        CHAIN_ID = 2
        print("берем продукт из холодильника")

        self.result = await RA.atomic_action()
        if self.result:
            await self.go_to_cut_station()
        else:
            print("Ошибка в холодильнике")
        return self.result

    async def go_to_cut_station(self):
        print("Едем в станцию нарезки")
        self.result = await RA.atomic_action()
        if self.result:
            await self.put_product_into_cut_station()
        else:
            print("Ошибка при поездке к станции нарезки")
        return self.result

    async def put_product_into_cut_station(self):
        print("Скалдываем продукт в станцию нарезки")
        self.result = await RA.atomic_action()
        if not self.result:
            print("Ошибка при складывании продукта в станцию нарезки")
            # await self.cut_the_product(duration=10, cutting_program=2)
            # запустить метод установка лимита? как бы так сделать :(
        return self.result

    async def cut_the_product(self, duration, cutting_program):
        """Нарезка продукта"""
        CHAIN_ID = 6
        print("запустили команду нарежь продукт")
        result = await Controllers.cut_the_product(cutting_program)

    async def start_filling(self):
        print("Начинаем чейн привези и порежь продукт", time.time())
        is_gripper = await RA.is_capture_is_gripper()
        if not is_gripper:
            self.result = await self.get_product_capture()
        self.result = await self.go_to_fridge()
        return self.result


class Baking(ConfigMixin):
    """Этот класс выполняет действия по разогреву, доставки товаров до выпекания, выпекание"""

    async def get_vane_from_cut_station(self):
        """Это группа атомарных действий по получению лопатки из станции нарезки"""
        CHAIN_ID = 1

        print("Отправляем команду примагнить лопатку в станции нарезки")

    async def turn_oven_heating_on(self):
        """Этот метод запускает прогрев печи"""

        print("Включаем прогрев печи")
        result = await Controllers.turn_oven_heating_on(self.oven_unit)
        if result:
            print("разогрев успешно включился")
        else:
            print("Ошибка печи")

    async def move_to_oven(self):
        """Движение от станции нарезки к печи"""
        pass

    async def put_vane_to_oven(self):
        """Добавтим лопатку в печь"""
        pass

    async def evaluate_baking_time(self):
        """Запускаем метод посчитай время выпечки
        возвращает словарь {oven_id: unix_time} для всех печей, время которых изменилось (и запрошенной тоже)
        """
        print("вызываем расчет времени")
        result = await Controllers.evaluate_baking_time(oven_unit=self.oven_unit,
                                                        baking_program=self.baking_program[0])

        return result

    async def time_change_handler(self):
        # как то запусть метод поменяй время во всех печах
        pass

    async def start_baking(self, result):
        duration = result[self.oven_unit]
        result = Controllers.start_baking(oven_unit=self.oven_unit,
                                          baking_program=self.baking_program[0])

    async def run_baking(self):
        """Это группа методов запускает выпекание"""
        time_changes = await self.evaluate_baking_time(self)
        await self.time_change_handler(self, time_changes)
        await self.start_baking(self, time_changes)


    async def new_run_baking(self):
        print("начинаем печь", time.time())
        time_changes = asyncio.get_running_loop().create_future()
        baking_results = await Controllers.start_baking(21, 4, time_changes)
        print("Время перед time_changes", time.time())
        print(time_changes)
        print("Время после time_changes и перед test", time.time())
        print("Это результат выпечки", time.time(), baking_results)
        print("Выпечка зарешена", time.time())
        return baking_results


class MakeCrust(ConfigMixin):
    """ ПЕРЕделать как будет данные о типе операции от контроллеров"""
    def __init__(self):
        self.result = False

    async def turn_oven_heating_on(self):
        print("Включаем подогрев печи")
        self.result = await Controllers.turn_oven_heating_on(self.oven_unit)
        pass

class DishPacking(ConfigMixin):
    """Запускает действия по упаковке товара"""
    def __init__(self):
        self.result = False

    async def go_to_oven(self):
        """Доедь до печи"""
        pass

    async def get_the_vane_from_oven(self):
        pass

    async def give_the_paper(self):
        pass

    async def go_to_package_station(self):
        pass

    async def pack_pizza(self):
        pass

    async def go_to_pick_up_point(self):
        pass

    async def deliver_pizza(self):
        pass

    async def go_to_package_station(self):
        pass

    async def switch_vanes(self):
        pass

    async def go_to_oven(self):
        pass

    async def put_vane_in_oven(self):
        pass


