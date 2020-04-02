"""Этот модуль запускает работу. Работа должна быть асинхронной, модуль запускает и управляет потоками внутри(?)"""
import asyncio
import time
import random

from ss_server_handler import new_order_handler
from PBM_main import TodaysOrders
from controllers_handler import qr_code_alarm, oven_alarm
from settings import QT_DISH_PER_ORDER


def start_testing(equipment_status):
    """Тут вызываем методы контролеров по тестированию оборудования"""
    status = equipment_status
    equipment_data = {}
    return status, equipment_data


async def ss_server(today_orders):
    """Это курутина запускает сервер, мониторит и обрабатывает сообщения от SS
    ВОПРОС: запуск сервера должен быть отдельно или тут?
     - уведомление о новом заказе
     - запрос оставшегося времени работы
     """
    # эмуляция поступления заказа
    while True:
        print("Работает ss_server", time.time())
        n = random.randint(1, 50)
        print("SS Ждет", n)
        await asyncio.sleep(n)
        new_order = {"refid": (23 + n), "dishes": [(2, 4, 6, 7), (1, 2, 4, 5)]}
        await new_order_handler(new_order, today_orders, QT_DISH_PER_ORDER)


async def controllers_alert_handler(today_orders):
    """Эта курутина обрабатывает уведомления от контроллеров: отказ оборудования и qr код
     Можно тут запустить методы мониторинга Арсения."""
    while True:
        print("Переключились в контролеры", time.time())
        qr_code = asyncio.create_task(qr_code_alarm(today_orders))
        oven_alarm_id = asyncio.create_task(oven_alarm(today_orders))
        await asyncio.gather(qr_code, oven_alarm_id)
#         при приостановке нужно заблокировать qr код


async def cooking(today_orders):
    """Эта курутина обеспеивает вызов методов по приготовлению блюд и другой важной работе"""

    while True:
        print("Работает cooking", time.time())
        print("В списке на выдачу", today_orders.orders_requested_for_delivery)

        if today_orders.is_cooking_paused:
            await today_orders.cooking_pause_handler()
            # print("Приостанавливаем работу")
            # await asyncio.sleep(10)

        elif today_orders.orders_requested_for_delivery:
            await today_orders.dish_delivery()

        elif today_orders.current_dishes_proceed.keys():
            print("Начинаем готовить")
            _, current_dish = today_orders.current_dishes_proceed.popitem()
            await current_dish.start_dish_cooking(today_orders)

        else:
            print("Dancing 3 secs")
            await asyncio.sleep(3)
            print()


async def create_cooking_tasks(today_orders):
    """В этой функции курутины формируются в таски"""

    ss_task = asyncio.create_task(ss_server(today_orders))
    controllers_task = asyncio.create_task(controllers_alert_handler(today_orders))
    cooking_task = asyncio.create_task(cooking(today_orders))

    await asyncio.gather(ss_task, controllers_task, cooking_task)


def start_cooking(equipment_data):
    """Эта функция инициирует все необходимое для работы. Пока создание экземпляра класса TodaysOrders"""
    today_orders = TodaysOrders()
    if today_orders:
        asyncio.run(create_cooking_tasks(today_orders))


def pause_cooking():
    today_orders.pause_cooking = True


def start_cooking_after_pause():
    today_orders.pause_cooking = False


if __name__ == "__main__":
    equipment_data = {}
    today_orders = start_cooking(equipment_data)
    if today_orders:
        asyncio.run(create_cooking_tasks())
