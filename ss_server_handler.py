"""Этот модуль управляет работой сервера для обмена данными со смарт экраном
WSGI сервер (? или простой HTTP)
типы запросов:
- post: время освобождения манипулятора (response - str в секундах длительность занятости киоска)
- post: новый заказ ref_id
"""
from aiohttp import web

import asyncio


async def time_left_handler(request):
    data = request.app["today_orders"]
    time_left = data.time_to_cook_all_dishes_left
    message = f"Вот столько осталось готовить {time_left}"
    # можем вернуть json
    # message = {"time_left":time_left}
    # return web.json_response(message)
    return web.Response(text=message)


async def new_order_handler(request):
    if request.body_exists:
        request_body = await request.json()
        print(request_body)
        new_order_id = request_body["refid"]
        data = request.app["today_orders"]
        is_it_new_order = data.checking_order_for_double(new_order_id)
        print("Это новый заказ", is_it_new_order)
        if is_it_new_order:
            # data.current_orders_proceed[request_body["refid"]] = "Новый супер заказ"
            order_content = await data.get_order_content_from_db(new_order_id)
            print(order_content)
            data.create_new_order(order_content)
            return web.Response(text="новый заказ принят")


def setup_routes(app):
    app.add_routes([web.get("/", time_left_handler),
                    web.post("/new", new_order_handler),
                    ])


def create_server():
    app = web.Application()
    setup_routes(app)
    return app




# import websockets
#
# async def ss_hello(websocket, path):
#     message = await websocket.recv()
#     print(f"{message} получено, начинаем обработку")
#     await websocket.send("Отправляем сообщение")
#
# start_server = websockets.serve(ss_hello, "localhost", 8080)





# HOST_NAME = "localhost"
# PORT_NUMBER = 8080
#
# class SS_server_handler(BaseHTTPRequestHandler):
#     """Класс обертка для обработки запросов, логика обработки описывается в дочернх классах"""
#     def do_head(self):
#         """Описывает формирование заголовка ответа для запроса"""
#         self.send_response(200)
#         self.send_header("Content-type", "text/html")
#         self.end_headers()
#
#     def do_post(self):
#         pass


# def start_ss_server(today_orders):
#     """Описать сервер
#     пока эмуляция работы"""
#
#     while True:
#         print("Работает ss_server", time.time())
#         n = random.randint(1, 50)
#         print("SS Ждет", n)
#         await asyncio.sleep(n)
#         new_order = {"refid": (23 + n), "dishes": [(2, 4, 6, 7), (1, 2, 4, 5)]}
#         await new_order_handler(new_order, today_orders)

    # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # server_socket.bind(("localhost", 5001))
    # server_socket.listen(1)
    #
    # while True:
    #     client_socket, adress = server_socket.accept()
    #     print("connection from", adress)
    #
    #     while True:
    #         ss_request = client_socket.recv(4096)
    #
    #         if not ss_request:
    #             break
    #         else:
    #             responce = "Preparation time is 673628 sec".encode()
    #             client_socket.send(responce)
    #
    #     client_socket.close()

#
# def fetch_time_till_ready_to_cook():
#     """Этот метод возвращает сколько киоск еще будет занят."""
#     pass
#
#
# async def new_order_handler(new_order_refid, today_orders):
#     """Эта функция иницирует создание экземляров класса новый заказ"""
#     is_it_new_order = today_orders.checking_order_for_double(new_order_refid)
#     if is_it_new_order:
#         today_orders.create_new_order(new_order_refid)
#
#
# if __name__ == "__main__":
#     start_ss_server()
