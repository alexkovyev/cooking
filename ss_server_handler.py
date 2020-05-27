"""Этот модуль управляет работой сервера для обмена данными со смарт экраном
WSGI сервер (? или простой HTTP)
типы запросов:
- post: время освобождения манипулятора (response - str в секундах длительность занятости киоска)
- post: новый заказ ref_id
"""
import asyncio
import time

from aiohttp import web


async def time_left_handler(request):
    data = request.app["today_orders"]
    time_left = data.time_to_cook_all_dishes_left
    message = f"Вот столько осталось готовить {time_left}"
    # можем вернуть json
    # message = {"time_left":time_left}
    # return web.json_response(message)
    return web.Response(text=message)


async def new_order_handler(request):
    print("Получили запрос от SS на новый заказ", time.time())
    if request.body_exists:
        request_body = await request.json()
        print("Тело запроса от SS", request_body)
        new_order_id = request_body["refid"]
        data = request.app["today_orders"]
        is_it_new_order = data.checking_order_for_double(new_order_id)
        print("Это новый заказ", is_it_new_order)
        if is_it_new_order:
            order_content = await data.get_order_content_from_db(new_order_id)
            print("Состав заказа", order_content)
            data.get_recipe_data(order_content["dishes"])
            print("С рецептом", order_content)
            lock = asyncio.Lock()
            async with lock:
                await data.create_new_order(order_content)
            return web.Response(text="новый заказ принят")


def setup_routes(app):
    app.add_routes([web.get("/", time_left_handler),
                    web.post("/new", new_order_handler),
                    ])


def create_server():
    app = web.Application()
    setup_routes(app)
    return app
