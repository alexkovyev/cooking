"""Этот модуль запускает работу. Работа должна быть асинхронной, модуль запускает и управляет потоками внутри(?)"""
import asyncio
import time
import random

# from ss_server_handler import start_ss_server
from main_order_handler import TodaysOrders
from settings import QT_DISH_PER_ORDER
from recipe import get_dough


async def ss_server():
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
        new_order = {"refid": (23+n), "dishes": [(2, 4, 6, 7), (1, 2, 4, 5)]}
        today_orders.create_new_order(new_order, QT_DISH_PER_ORDER)
        print("1 sec ss", time.time())


async def controllers_alert_handler():
    """Эта курутина обрабатывает уведомления от контроллеров: отказ оборудования и qr код
     Можно тут запустить методы мониторинга Арсения.
     ВОПРОС: !!! как сделать блокировку на cooking? !!! """
    while True:
        print("Работает controllers_alert_handler", time.time())
        await asyncio.sleep(2)
        print("2 sec controllers_alert_handler", time.time())


async def cooking():
    """Эта курутина обеспеивает вызов методов по приготовлению блюд и другой важной работе"""
    while True:
        print("Работает cooking", time.time())
        while today_orders.current_orders_proceed:
            my_order = today_orders.current_orders_proceed.keys()
            for dish in today_orders.current_dishes_proceed.keys():
                print("Начинаю готовить блюдо", dish)
                await get_dough(dish, 3, 6)
                print("Остались печи", today_orders.oven_available)
        else:
            print("Dancing 3 secs")
            await asyncio.sleep(3)
        print("Это заказы в current_orders_proceed", today_orders.current_orders_proceed)
        print("3 sec cooking", time.time())


async def start_working():
    """В этой функции курутины формируются в таски"""
    ss_task = asyncio.create_task(ss_server())
    controllers_task = asyncio.create_task(controllers_alert_handler())
    cooking_task = asyncio.create_task(cooking())

    await asyncio.gather(ss_task, controllers_task, cooking_task)


def work_init():
    """Эта функция инициирует все необходимое для работы. Пока создание экземпляра класса TodaysOrders"""
    today_orders = TodaysOrders()
    if today_orders.is_able_to_cook():
        return today_orders
    else:
        raise ValueError ("Оборудование неисправно! Что делаем с ошибкой дальше")

if __name__ == "__main__":
    today_orders = work_init()
    if today_orders:
        asyncio.run(start_working())
