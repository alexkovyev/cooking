"""Этот модуль запускает работу. Работа должна быть асинхронной, модуль запускает и управляет потоками внутри(?)"""

from ss_server_handler import start_ss_server

from main_order_handler import TodaysOrders


def start_working():
    """В этой функции должны быть все основные действия при запуске и работе. Это отдельные потоки"""
    todays_orders = TodaysOrders()
    start_ss_server()


if __name__ == "__main__":
    start_working()
