"""Этот модуль запускает работу PBM."""

import asyncio
import random
import time
from contextvars import ContextVar

from aiohttp import web

from controllers import cntrls_events, event_generator

# from ss_server_handler import new_order_handler
from ss_server_handler import create_server
from PBM_main import PizzaBotMain
# from controllers_handler import qr_code_alarm, oven_alarm
from settings import QT_DISH_PER_ORDER


async def hello_from_qr_code():
    print("QR код обработан", time.time())


async def hello_from_broken_oven():
    print("Изменение статуса оборудования обработано", time.time())


async def controllers_alert_handler(cntrls_events):
    """Эта курутина обрабатывает уведомления от контроллеров: отказ оборудования и qr код """

    print("Переключились в контролеры", time.time())

    async def wait_for_qr_code(cntrls_events):
        event_name = "qr_scanned"
        event = cntrls_events.get_dispatcher_event(event_name)
        while True:
            result = await event
            await hello_from_qr_code()

    async def wait_for_hardware_status_changed(cntrls_events):
        event_name = "hardware_status_changed"
        event = cntrls_events.get_dispatcher_event(event_name)
        while True:
            result = await event
            await hello_from_broken_oven()

    qr_event_waiter = asyncio.create_task(wait_for_qr_code(cntrls_events))
    status_change_waiter = asyncio.create_task(wait_for_hardware_status_changed(cntrls_events))
    await asyncio.gather(qr_event_waiter, status_change_waiter)


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
            print("Начнаем готовить")
            _, current_dish = today_orders.current_dishes_proceed.popitem()
            print(current_dish)
            await current_dish.start_dish_cooking()

        # elif today_orders.current_dishes_proceed.keys():
        #     print("Начинаем готовить")
        #     _, current_dish = today_orders.current_dishes_proceed.popitem()
        #     print(current_dish)
        #     # await current_dish.start_dish_cooking(today_orders)

        else:
            print("Dancing 3 secs")
            today_orders.time_to_cook_all_dishes_left += 55
            await asyncio.sleep(3)
            print()


async def create_tasks(app, today_orders, cntrls_events):
    # добавляем асинхонный запуск сервера
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host='127.0.0.1', port=8080)
    await site.start()
    print("Сервер запущен на 127.0.0.1:8080")

    # запускаем работу бесконечных тасков cooking и controllers
    # events разовый такс для проверки работоспособности и имитации работы контроллеров
    events = asyncio.create_task(event_generator(cntrls_events))
    controllers_task = asyncio.create_task(controllers_alert_handler(cntrls_events))
    cooking_task = asyncio.create_task(cooking(today_orders))
    await asyncio.gather(controllers_task, cooking_task, events)


def start(equipment_data, recipes):
    """Эта функция инициирует все необходимое для работы. Пока создание экземпляра класса TodaysOrders
    Добавить создание event-loop и инициацию класса контролеры"""
    today_orders = PizzaBotMain(equipment_data, recipes)
    print("Начинается код start cooking")
    app = create_server()
    app["today_orders"] = today_orders
    asyncio.run(create_tasks(app, today_orders, cntrls_events))

# # Event handlers
# def qr_handler(guid):
#     print('QR has been scanned. GUID:', guid)
#
#
# def status_handler(unit_name, status):
#     print(unit_name, 'status changed. Now:', status)
#
#
# # bind handlers to a corresponding event
# cntrls_events.bind(qr_scanned=qr_handler)
# cntrls_events.bind(hardware_status_changed=status_handler)
