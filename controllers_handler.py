"""Этот модуль управляет событиями от контроллеров"""

import asyncio
import random
import time


async def qr_code_alarm(today_orders):
    print("Мониторим есть ли запрос qr code")
    while True:
        # тут какая то классная команда контроллерам, ниже просто симуляция работы
        qr_code_waiting_sec = random.randint(1, 50)
        await asyncio.sleep(qr_code_waiting_sec)
        is_qr_code_good = random.choice([True, False])
        if is_qr_code_good:
            print("Валидный qr code, давай заказ")
            order_number = round(time.time() * 1000)
            today_orders.orders_requested_for_delivery[order_number] = order_number


async def oven_alarm(today_orders):
    print("Мониторинг работоспособности печи")
    while True:
        # тут какая то классная команда контроллерам, ниже просто симуляция работы
        oven_broken_waiting_sec = random.randint(30, 60)
        await asyncio.sleep(oven_broken_waiting_sec)
        broken_oven_id = random.randint(1, 21)
        print("Сломалась печь", broken_oven_id)
        today_orders.oven_broke_handler(broken_oven_id)
