"""Этот модуль запускает работу PBM."""

import asyncio
import random
import time
from aiohttp import web
from contextvars import ContextVar


# from ss_server_handler import new_order_handler
from ss_server_handler import create_server
from PBM_main import PizzaBotMain
# from controllers_handler import qr_code_alarm, oven_alarm
from settings import QT_DISH_PER_ORDER


async def controllers_alert_handler():
    """Эта курутина обрабатывает уведомления от контроллеров: отказ оборудования и qr код
     Можно тут запустить методы мониторинга Арсения."""
    while True:
        print("Переключились в контролеры", time.time())
        await asyncio.sleep(5)
        print("Контролеры отработали")


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

        elif today_orders.current_orders_proceed.keys():
            print("Начнаем готовить")
            _, current_dish = today_orders.current_orders_proceed.popitem()
            print(current_dish)

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


async def create_tasks(app, today_orders):
    # добавляем асинхонный запуск сервера
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host='127.0.0.1', port=8080)
    await site.start()
    print("Сервер запущен на 127.0.0.1:8080")

    # запускаем работу бесконечных тасков cooking и controllers
    controllers_task = asyncio.create_task(controllers_alert_handler())
    cooking_task = asyncio.create_task(cooking(today_orders))
    await asyncio.gather(controllers_task, cooking_task)


def start(equipment_data, recipes):
    """Эта функция инициирует все необходимое для работы. Пока создание экземпляра класса TodaysOrders
    Добавить создание event-loop и инициацию класса контролеры"""
    today_orders = PizzaBotMain(equipment_data, recipes)
    print("Начинается код start cooking")
    app = create_server()
    app["today_orders"]=today_orders
    asyncio.run(create_tasks(app, today_orders))

