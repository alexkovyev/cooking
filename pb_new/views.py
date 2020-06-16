import asyncio
from aiohttp import web
import time


async def time_left_handler(request):
    message = f"Вот столько осталось готовить"
    # можем вернуть json
    # message = {"time_left":time_left}
    # return web.json_response(message)
    return web.Response(text=message)

async def hardware_broke_handler(event_data):
    print("Обрабатываем уведомление об поломке оборудования", time.time())
    oven_id = int(event_data["unit_name"])
    oven_status = event_data["status"]
    print("Обработали", oven_id, oven_status)


