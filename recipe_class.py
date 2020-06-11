"""Пока тут собрана информация о рецепте."""
import asyncio
import time

from RA import RA
from RA import RAError
from controllers import Controllers

from settings import OVEN_LIQUIDATION_TIME


class ConfigMixin(object):
    """Временное хранение идентификаторов оборудования"""
    SLICING = 1
    CAPTURE_STATION = 2
    PRODUCT_CAPTURE_ID = 1


class Recipy(ConfigMixin):
    """Основной класс рецепта, содержит все действия по приготовлению блюда"""

    def __init__(self):
        # по умолчанию значение False.
        # Меняется на False:
        # - лопатка приезжает в станцию нарезки
        # - поливаем соусом
        # - нарезаем п-ф
        self.is_cut_station_free = asyncio.Event()
        self.time_limit = None

    # RA
    async def get_move_chain_duration(self, place_to):
        """ Метод получает варианты длительности передвижения, выбирает тот, который
        удовлетвоаряет условиям
        :param place_to: str
        :return: int
        """
        current_destination = await RA.get_current_position()
        forward_destination = place_to
        possible_duration = await RA.get_position_move_time(current_destination, forward_destination)
        if possible_duration:
            return min(possible_duration)
        else:
            raise RAError

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

    async def atomic_chain_execute(self, atomic_params_dict):
        duration = await self.get_atomic_chain_duration(atomic_params_dict)
        try:
            await RA.atomic_action(**atomic_params_dict)
            print("Успешно выполнили атомарное действие")
        except RAError:
            self.status = "failed_to_be_cooked"
            print("Ошибка атомарного действия")
        return self.status

    async def move_to_object(self, move_params):
        """Эта функция описывает движение до определенного места."""
        print("Начинаем чейн движения")
        place_to, limit = move_params
        duration = await self.get_move_chain_duration(place_to)
        is_need_to_dance = False
        print("*********Есть ли лимит времени", self.time_limit)
        try:
            if limit and self.time_limit:
                place_now = await RA.get_current_position()
                delivery_time_options = await RA.get_position_move_time(place_now, place_to)
                time_left = self.time_limit - time.time()
                print("Разница лимита и чейна",time_left)
                time_options = list(filter(lambda t: t <= time_left, delivery_time_options))
                if time_options:
                    duration = max(time_options)
                is_need_to_dance = True if time_left>duration else False
                dance_time = time_left - duration
                print("Время танца", dance_time)
            await RA.position_move(place_to, duration)
            if is_need_to_dance:
                print("начинаем танцевать дополнительно", dance_time, time.time())
                result = await RA.dance_for_time(dance_time)
                if result:
                    print("RBA успешно подъехал к", place_to, time.time())
        except RAError:
            self.status = "failed_to_be_cooked"
            # есть ли какой то метод проверки работоспособности
            # что деламем? сворачиваем работу или продолжаем дальше
        return self.status

    # controllers
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

    async def controllers_give_sauce(self):
        """Вызов метода контроллеров для поливания соусом"""
        print("Начинаем поливать соусом", time.time())
        recipe = self.sauce.sauce_cell
        print("Данные об ячейке", recipe)
        print("Время начала поливки соусом контроллерами", time.time())
        result = await Controllers.give_sauce(recipe)
        if result:
            print("успешно полили соусом")
            print("Статус станции нарезки", self.is_cut_station_free.is_set())
            self.is_cut_station_free.set()
            print("Статус станции нарезки после сет", self.is_cut_station_free.is_set())
        else:
            print("---!!! Не успешно полили соусом")
            self.status = "failed_to_be_cooked"
        return self.status, self.is_cut_station_free

    async def controllers_oven(self, oven_mode, recipe):
        time_changes = asyncio.get_running_loop().create_future()
        self.time_changes_handler(time_changes)
        operation_results = await Controllers.start_baking(self.oven_id, oven_mode, recipe, time_changes)
        return operation_results

    # low-level PBM
    async def chain_execute(self, chain_list):
        try:
            for chain in chain_list:
                if self.status != "failed_to_be_cooked":
                    chain, params = chain
                    self.status = await chain(params)
                else:
                    break
        except RAError:
            self.status = "failed_to_be_cooked"
            print("Ошибка века")
        return self.status

    @staticmethod
    async def is_need_to_change_gripper(required_gripper: str):
        """метод проверяет Нужно ли менять захват
        """
        current_gripper = await RA.get_current_gripper()
        if str(current_gripper) != required_gripper:
            return True
        return False

    async def change_gripper(self, required_gripper: str):
        is_need_to_change_gripper = await self.is_need_to_change_gripper(required_gripper)
        print("Проверяем, нужно ли менять захват", is_need_to_change_gripper)
        if is_need_to_change_gripper:
            await self.move_to_object((self.CAPTURE_STATION, None))
            await self.atomic_chain_execute({"place":"get_gripper", "name":"get_gripper"})
        return self.status

    async def get_vane_from_oven(self, *args):
        """Этот метод запускает группу атомарных действий RA по захвату лопатки из печи"""
        atomic_params = {"name": "get_vane_from_oven",
                          "place": self.oven_unit}
        self.status = await self.atomic_chain_execute(atomic_params)
        return self.status

    async def set_vane_in_oven(self, *args):
        """Этот метод запускает группу атомарных действий RA по размещению лопатки в печи"""
        atomic_params = {"name": "set_shovel",
                          "place": self.oven_unit}
        self.status = await self.atomic_chain_execute(atomic_params)
        return self.status

    async def control_dough_position(self, *args):
        """отдаем команду на поправление теста"""
        atomic_params = {"name": "get_dough",
                         "place": self.dough.halfstuff_cell}
        self.status = await self.atomic_chain_execute(atomic_params)
        return self.status

    async def leave_vane_in_cut_station(self, *args):
        """отдаем команду оставить лопатку в станции нарезки"""
        atomic_params = {"name": "set_shovel",
                         "place": self.SLICING}
        self.status = await self.atomic_chain_execute(atomic_params)
        return self.status

    # не объединено с выше в 1, так как обработка ошибок может быть разная
    async def take_vane_from_cut_station(self, *args):
        """отдаем команду взять лопатку в станции нарезки"""
        atomic_params = {"name": "get_shovel",
                         "place": self.SLICING}
        self.status = await self.atomic_chain_execute(atomic_params)
        return self.status

    async def put_half_staff_in_cut_station(self, *args):
        """Этот метод опускает п-ф в станцию нарезки"""
        print("Начинаем размещать продукт в станции нарезки", time.time())
        print("Станция нарезки свободна", self.is_cut_station_free.is_set())
        atomic_params = {
            "name":"set_product",
            "place": self.SLICING
        }
        while not self.is_cut_station_free.is_set():
            print("Танцуем с продуктом")
            await asyncio.sleep(1)

        self.status = await self.atomic_chain_execute(atomic_params)
        return self.status

    async def dish_liquidation(self, *args):
        print("!!!!!!!! Ликвидируем блюдо", time.time())
        return "ОК"

    async def set_oven_timer(self):
        print("!!!!!!!!!!ставим таймер на печь", time.time())
        oven_future = asyncio.get_running_loop().create_future()
        # oven_future.add_done_callback(self.dish_liquidation)
        self.oven_future = oven_future
        print("Это футура в заказе", self.oven_future)
        await asyncio.create_task(self.oven_timer())

    async def oven_timer(self):
        print("!!!!!!!!!!!!Начинаем ждать выдачи час", time.time())
        await asyncio.sleep(OVEN_LIQUIDATION_TIME)
        print("!!!!!!!!!!! время сна завершено",time.time())
        if not self.oven_future.cancelled():
            print("!!!!!!!!!!!!!!Футура блюдо не забрали")
            self.oven_future.set_result("time is over")
            await self.dish_liquidation()

    async def time_changes_handler(self, time_futura):
        """Обрабатывает результаты футуры об изменении времени выпечки"""
        print(time_futura, time.time())

    # средняя укрупненность, так как операция с лимитом по времени от контроллеров
    async def bring_half_staff(self, cell_location_tuple):
        print("Начинаем везти продукт")
        cell_location, half_staff_position = cell_location_tuple
        atomic_params = {"name": "get_product",
                         "place": "fridge",
                         "obj": "onion",
                         "cell": cell_location,
                         "position": half_staff_position,
        }

        move_params = (cell_location, False)
        move_params_new = (self.SLICING, True)

        what_to_do = [
            (self.move_to_object, move_params),
            (self.atomic_chain_execute, atomic_params),
            (self.move_to_object, move_params_new),
        ]

        self.status = await self.chain_execute(what_to_do)
        print("*!*!*!*! Закончили с ингредиентом начинки", self.status, time.time())

    # chains PBM
    async def chain_get_dough_and_sauce(self):
        """Подумать как разделить на 2 части"""
        print("Начинается chain Возьми ТЕСТО", time.time())
        self.status = self.status_change("cooking")
        chain_list = [(self.move_to_object, (self.oven_unit, None)),
                      (self.get_vane_from_oven, None),
                      (self.move_to_object, (self.SLICING, None)),
                      (self.controllers_get_dough, None),
                      (self.control_dough_position, None),
                      (self.move_to_object, (self.SLICING, None)),
                      (self.leave_vane_in_cut_station, None),
                      ]
        await self.chain_execute(chain_list)
        print("Закончили с ТЕСТОМ",time.time(), self.status)
        if self.status != "failed_to_be_cooked":
            asyncio.create_task(self.controllers_give_sauce())
        return self.status

    async def get_filling_chain(self, storage_adress, cutting_program):
        """Чейн по доставке и нарезки 1 п\ф"""
        print("% % % Начинаем чейн НАЧИНКИ", time.time())
        print(storage_adress, cutting_program)
        # print("Адрес в холоильнике", storage_adress)
        # print("Это статус блюда в начинке",self.status)
        # print("Это программа нарезки", cutting_program)
        chain_list = [(self.change_gripper, "product"),
                      (self.bring_half_staff, storage_adress),
                      (self.put_half_staff_in_cut_station, None),
        ]
        await self.chain_execute(chain_list)
        if self.status != "failed_to_be_cooked":
            self.time_limit = time.time() + cutting_program["duration"]
            print("% % % УСТАНОВЛЕН лимит времени, начинаем нарезку", time.time())
            asyncio.create_task(self.cut_half_staff(cutting_program))
        return self.status

    async def cut_half_staff(self, cutting_program):
        print("Начинаем этап ПОРЕЖЬ продукт", time.time())
        duration = cutting_program["duration"]
        program_id = cutting_program["program_id"]
        print("Время начала нарезки п\ф", time.time())
        result = await Controllers.cut_the_product(program_id)
        if result:
            print("успешно нарезали п\ф")
            self.is_cut_station_free.set()
            self.time_limit = None
            print("СНЯТ временой ЛИМИТ", time.time())
        else:
            print("---!!! Не успешно нарезали п\ф")
            self.status = "failed_to_be_cooked"
        return self.status

    async def bring_vane_to_oven(self):
        print("Начинаем чейн Вези лопатку в печь")
        chain_list = [(self.change_gripper, "None"),
                     (self.move_to_object, (self.SLICING, None)),
                     (self.take_vane_from_cut_station, None),
                     (self.move_to_object, (self.oven_unit, None)),
                     (self.set_vane_in_oven, None),
                     ]
        await self.chain_execute(chain_list)
        print("Оставили лопатку в печи", time.time())

    async def controllers_turn_heating_on(self):
        """Метод запускает прогрев печи"""
        print("Начинаем прогрев печи", time.time())
        oven_mode = "pre_heating"
        recipe = self.pre_heating_program
        operation_result = await self.controllers_oven(oven_mode, recipe)

    async def controllers_bake(self):
        """Метод запускает выпечку"""
        print("Начинаем прогрев печи", time.time())
        oven_mode = "baking"
        recipe = self.baking_program
        self.status = "baking"
        operation_result = await self.controllers_oven(oven_mode, recipe)
        if operation_result:
            self.status = "ready"

    async def make_crust(self):
        """Этот метод делает корочку на пицце"""
        print("Начинаем делать корочку", time.time())


    # async def new_run_baking(self):
    #     print("начинаем печь", time.time())
    #     time_changes = asyncio.get_running_loop().create_future()
    #     baking_results = await Controllers.start_baking(21, 4, time_changes)
    #     print("Время перед time_changes", time.time())
    #     print(time_changes)
    #     print("Время после time_changes и перед test", time.time())
    #     print("Это результат выпечки", time.time(), baking_results)
    #     print("Выпечка зарешена", time.time())
    #     return baking_results



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


