"""Этот модуль запускает работу PBM."""

import asyncio

from aiohttp import web

from controllers.ControllerBus import cntrls_events, event_generator
from ss_server_handler import create_server
from PBM_main import PizzaBotMain
from settings import QT_DISH_PER_ORDER, SS_SERVER_PORT as port, SS_SERVER_HOST as host


async def create_tasks(today_orders, cntrls_events):
    # добавляем асинхонный запуск сервера. не получилось быстро выделить в отдельный такс, не работает сервер
    # runner = web.AppRunner(app)
    # await runner.setup()
    # site = web.TCPSite(runner, host=host, port=port)
    # await site.start()
    # print(f"Сервер запущен на {host}:{port}")

    # запускаем работу бесконечных тасков cooking и controllers
    # events разовый такс для проверки работоспособности и имитации работы контроллеров
    events = asyncio.create_task(event_generator(cntrls_events))
    controllers_task = asyncio.create_task(today_orders.controllers_alert_handler(cntrls_events))
    cooking_task = asyncio.create_task(today_orders.cooking())
    super_speedy = asyncio.create_task(today_orders.cooking_immediately_execute())
    await asyncio.gather(controllers_task, cooking_task, events, super_speedy)


def start(equipment_data, recipes):
    """Эта функция инициирует все необходимое для работы. Пока создание экземпляра класса TodaysOrders
    Добавить создание event-loop и инициацию класса контролеры"""
    today_orders = PizzaBotMain(equipment_data, recipes)
    app = create_server()
    app["today_orders"] = today_orders
    asyncio.run(create_tasks(app, today_orders, cntrls_events))