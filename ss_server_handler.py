"""Этот модуль управляет работой сервера для обмена данными со смарт экраном
WSGI сервер (? или простой HTTP)
типы запросов:
- post: время освобождения манипулятора (response - str в секундах длительность занятости киоска)
- post: новый заказ ref_id
"""
from aiohttp import web
import asyncio


async def index(request):
    return web.Response(text="mdsjjdal dskdjalkjsal;jd;a")

def setup_routes(app):
    app.router.add_get('/', index)

def create_server():
    app = web.Application()
    setup_routes(app)
    return app

async def start_server(app):
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host='127.0.0.1', port=8080)
    await site.start()
    print("Serving up app on")



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
