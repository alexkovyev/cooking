import asyncio
from aiohttp import web
import time


async def time_left_handler(request):
    message = f"Вот столько осталось готовить"
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

async def hardware_broke_handler(event_data):
    print("Обрабатываем уведомление об поломке оборудования", time.time())
    oven_id = int(event_data["unit_name"])
    oven_status = event_data["status"]
    print("Обработали", oven_id, oven_status)


