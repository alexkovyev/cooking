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
        print()
        n = random.randint(1, 50)
        print("SS Ждет", n)
        await asyncio.sleep(n)
        new_order = {"refid": (23+n), "dishes": [(2, 4, 6, 7), (1, 2, 4, 5)]}
        today_orders.create_new_order(new_order, QT_DISH_PER_ORDER)
        # for dish in today_orders.current_dishes_proceed.keys():
        #     print("Добавляю в очередь блюдо", dish)
        #     new_job = await get_dough(dish, 3, 6)
        #     cooking_quere.put((1, new_job))
        print("1 sec ss", time.time())


controllers_alarm = asyncio.Event()

async def controllers_alarm_handler():
    controllers_alarm.set()
#     в какой таск добавить:  await event.wait(), event.clear()

async def controllers_alert_handler():
    """Эта курутина обрабатывает уведомления от контроллеров: отказ оборудования и qr код
     Можно тут запустить методы мониторинга Арсения.
     ВОПРОС: !!! как сделать блокировку на cooking? !!! """
    while True:
        print("Работает controllers_alert_handler", time.time())
        print()
        #Controllers.qr_code_monitoring()
        #Controllers.errors_monitoring()
        await asyncio.sleep(2)
        print("2 sec controllers_alert_handler", time.time())


async def cooking():
    """Эта курутина обеспеивает вызов методов по приготовлению блюд и другой важной работе"""
    while True:
        print("Работает cooking", time.time())
        if today_orders.current_dishes_proceed.keys():
            print("Начинаем готовить")
            _, current_order = today_orders.current_dishes_proceed.popitem()
            await get_dough(current_order.id, current_order.oven_unit, 6)
        else:
            print("Dancing 3 secs")
            await asyncio.sleep(3)




        # while not cooking_quere.empty():
        #     new_task = asyncio.create_task(cooking_quere.get())
        #     print(new_task)
        #     cooking_tasks.append(new_task)
        # else:
        #     print("Dancing 3 secs")
        #     await asyncio.sleep(3)
        # print("3 sec cooking", time.time())


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
    cooking_quere = asyncio.PriorityQueue()
    if today_orders:
        asyncio.run(start_working())
