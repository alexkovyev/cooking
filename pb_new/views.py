from aiohttp import web


async def time_left_handler(request):
    message = f"Вот столько осталось готовить"
    # можем вернуть json
    # message = {"time_left":time_left}
    # return web.json_response(message)
    return web.Response(text=message)
