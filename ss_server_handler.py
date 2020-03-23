"""Этот модуль управляет работой сервера для обмена данными со смарт экраном
WSGI сервер (? или простой HTTP)
типы запросов:
- get: время освобождения манипулятора (response - str в секундах длительность занятости киоска
- put: новый заказ ref_id
"""
import asyncio
from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver


HOST_NAME = "localhost"
PORT_NUMBER = 8080

class SS_server_handler(BaseHTTPRequestHandler):
    """Класс обертка для обработки запросов, логика обработки описывается в дочернх классах"""
    def do_head(self):
        """Описывает формирование заголовка ответа для запроса"""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_post(self):
        pass


def start_ss_server():
    """Описать сервер"""

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


def fetch_time_till_ready_to_cook():
    """Этот метод возвращает сколько киоск еще будет занят."""
    pass


async def new_order_handler():
    """Эта функция иницирует создание экземляров класса новый заказ"""
    pass


if __name__ == "__main__":
    start_ss_server()
