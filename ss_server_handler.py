"""Этот модуль управляет работой сервера для обмена данными со смарт экраном
WSGI сервер (? или простой HTTP)
типы запросов:
- get: время освобождения манипулятора (response - str в секундах длительность занятости киоска
- put: новый заказ ref_id
"""
import socket


def start_ss_server():
    """Описать сервер"""
    serser_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serser_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serser_socket.bind(("localhost", 5001))
    serser_socket.listen()

    while True:
        client_socket, adress = serser_socket.accept()
        print("connection from", adress)

        while True:
            ss_request = client_socket.recv(4096)

            if not ss_request:
                break
            else:
                responce = "Preparation time is 673628 sec".encode()
                client_socket.send(responce)

        client_socket.close()


def fetch_time_till_ready_to_cook():
    """Этот метод возвращает сколько киоск еще будет занят."""
    pass


def new_order_handler():
    """Эта функция иницирует создание экземляров класса новый заказ"""
    pass


if __name__ == "__main__":
    start_ss_server()
