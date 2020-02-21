"""Этот модуль запускает работу. Работа должна быть асинхронной, модуль запускает и управляет потоками внутри(?)"""

from alert_handler import main_alert_handler


def start_working():
    """В этой функции должны быть все основные действия при запуске и работе"""
    main_alert_handler()
    # main_order_handler()
    # main_control_loop()
    pass


if __name__ == "__main__":
    start_working()
