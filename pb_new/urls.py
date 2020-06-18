from aiohttp import web
from views import time_left_handler


def setup_routes(app):
    app.add_routes([web.get("/", time_left_handler),
                    web.post("/new_order", time_left_handler),
                    web.post("/start_pbm", time_left_handler)
                    ])