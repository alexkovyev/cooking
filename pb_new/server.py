import asyncio
from aiohttp import web
import time
import uuid

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import SERVER_HOST, SERVER_PORT
from controllers.ControllerBus import ControllersEvents, event_generator
from discord_sender import DiscordBotSender
from equipment import Equipment
from kiosk_modes.CookingMode import CookingMode
from kiosk_modes import (TestingMode,
                         StandByMode)
from logs import PBlogs
from urls import setup_routes
from views import hardware_broke_handler


class PizzaBotMain(object):

    def __init__(self):
        self.kiosk_status = "stand_by"
        self.is_kiosk_busy = False
        self.current_instance = StandByMode.StandBy()
        self.equipment = None
        self.cntrls_events = ControllersEvents()
        self.config = None

    def create_server(self):
        app = web.Application()
        setup_routes(app)
        return app

    def create_scheduler(self):
        scheduler = AsyncIOScheduler()
        scheduler.add_job(self.test_scheduler, 'interval', seconds=5)
        # переделать на включение в определенный момент
        scheduler.add_job(self.turn_on_cooking_mode, 'cron', day_of_week='*', hour='23', minute=44, second=0)
        return scheduler

    def get_config_data(self):
        pass

    async def get_equipment_data(self):
        print("Подключаемся к БД за информацией", time.time())
        await asyncio.sleep(10)
        equipment_data = {
            "ovens": {i: {"oven_id": str(uuid.uuid4()), "status": "free"} for i in range(1, 22)},
            "cut_station": {"id": "f50ec0b7-f960-400d-91f0-c42a6d44e3d0",
                            "status": "ok"},
            "package_station": {"id": "afeb1c10-83ef-4194-9821-491fcf0aa52b",
                                "status": "ok"},
            "sauce_dispensers": {"16ffcee8-2130-4a2f-b71d-469ee65d42d0": "ok",
                                 "ab5065e3-93aa-4313-869e-50a959458439": "ok",
                                 "28cc0239-2e35-4ccd-9fcd-be2155e4fcbe": "ok",
                                 "1b1af602-b70f-42a3-8b5d-3112dcf82c26": "ok",
            },
            "dough_dispensers": {"ebf29d04-023c-4141-acbe-055a19a79afe": "ok",
                                 "2e84d0fd-a71f-4988-8eee-d0373c0bc609": "ok",
                                 "68ec7c16-f57b-43c0-b708-dfaea5c2e1dd": "ok",
                                 "75355f3c-bf05-405d-98af-f04bcba7d7e4": "ok",
                                 },
            "pick_up_points": {"1431f373-d036-4e0f-b059-70acd6bd18b9": "ok",
                              "b7f96101-564f-4203-8109-014c94790978": "ok",
                              "73b194e1-5926-45be-99ec-25e1021b96f7": "ok",
            }
        }
        print("Получили данные из БД", time.time())
        return equipment_data

    async def add_equipment_data(self):
        equipment_data = await self.get_equipment_data()
        self.equipment = Equipment(equipment_data)

    async def turn_on_cooking_mode(self):
        """Включить можно только после завершения тестов"""
        if self.kiosk_status == "stand_by":
            print("ЗАПУСКАЕМ режим ГОТОВКИ")
            self.current_instance = CookingMode.BeforeCooking()
            (is_ok, self.equipment), recipe = await CookingMode.BeforeCooking.start_pbm(self.equipment)
            self.current_instance = CookingMode.CookingMode(recipe)
            self.kiosk_status = "cooking"
            await self.current_instance.cooking()
        elif self.kiosk_status == "testing_mode":
            pass
        print("Режим готовки активирован", self.kiosk_status)

    async def test_working(self):
        while True:
            print("запускается фоновая задача", time.time())
            print("Текущий режим", self.current_instance)
            await asyncio.sleep(5)
            print("фоновая задача отработала", time.time())

    async def test_scheduler(self):
        print("Привет из расписания", time.time())

    async def create_hardware_broke_listener(self):
        event_name = "hardware_status_changed"
        event = self.cntrls_events.get_dispatcher_event(event_name)
        while True:
            event_data = await event
            _, new_data = event_data
            await hardware_broke_handler(new_data)

    async def main_worker(self):
        print("Работает основной worker")
        await asyncio.sleep(5)

    async def create_tasks(self, app, scheduler):
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host=SERVER_HOST, port=SERVER_PORT)
        await site.start()
        scheduler.start()

        # Переделать потом на генерацию из списка
        on_start_tasks = asyncio.create_task(self.add_equipment_data())
        controllers_bus = asyncio.create_task(event_generator(self.cntrls_events))
        event_listener = asyncio.create_task(self.create_hardware_broke_listener())
        main_flow = asyncio.create_task(self.main_worker())
        discord_sender = asyncio.create_task(DiscordBotSender.send_message())
        test_task = asyncio.create_task(self.test_working())
        logging_task = asyncio.create_task(PBlogs.logging_task())

        await asyncio.gather(controllers_bus, test_task, event_listener, main_flow, discord_sender, logging_task,
                             on_start_tasks)

    def start_server(self):
        app = self.create_server()
        scheduler = self.create_scheduler()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.create_tasks(app, scheduler))
        loop.run_forever()
