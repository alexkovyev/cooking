"""Этот модуль запускает работу. Работа должна быть асинхронной, модуль запускает и управляет потоками внутри(?)"""

from ss_server_handler import start_ss_server
from new_orders_handler import get_new_order
from rba_control_loop import RoboticArmControl

def start_working():
    """В этой функции должны быть все основные действия при запуске и работе. Это отдельные потоки"""
    start_ss_server()
    get_new_order()
    RoboticArmControl.rba_execute()


if __name__ == "__main__":
    start_working()
