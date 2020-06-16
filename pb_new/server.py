import asyncio
from aiohttp import web
import time

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import SERVER_HOST, SERVER_PORT
from controllers.ControllerBus import ControllersEvents, event_generator
from urls import setup_routes
from views import hardware_broke_handler
from pb_new.kiosk_modes import StandBy, CookingMode


class PizzaBotMain(object):

    def __init__(self):
        self.kiosk_status = "stand_by"
        self.is_kiosk_busy = False
        self.current_instance = StandBy()
        self.equipment = StandBy()
        self.cntrls_events = ControllersEvents()
        print(type(self.cntrls_events))
        print(isinstance(self.cntrls_events, ControllersEvents))

    def create_server(self):
        app = web.Application()
        setup_routes(app)
        return app

    def create_scheduler(self):
        scheduler = AsyncIOScheduler()
        scheduler.add_job(self.test_scheduler, 'interval', seconds=5)
        # переделать на включение в определенный момент
        scheduler.add_job(self.turn_on_cooking_mode, 'interval', seconds=24)
        return scheduler

    def get_config_data(self):
        pass

    async def turn_on_cooking_mode(self):
        """Включить можно только после завершения тестов"""
        if self.kiosk_status == "stand_by":
            self.kiosk_status = "cooking"
            self.current_instance = CookingMode()
            await self.current_instance.start_pbm()
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

    async def discord_sender(self):
        print("Работает discord отправитель")
        await asyncio.sleep(5)

    async def logging_task(self):
        print("Работает логгер")
        await asyncio.sleep(5)

    async def create_tasks(self, app, scheduler):
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host=SERVER_HOST, port=SERVER_PORT)
        await site.start()
        scheduler.start()
        # Переделать потом на генерацию из списка

        controllers_bus = asyncio.create_task(event_generator(self.cntrls_events))
        event_listener = asyncio.create_task(self.create_hardware_broke_listener())
        main_flow = asyncio.create_task(self.main_worker())
        discord_sender = asyncio.create_task(self.discord_sender())
        test_task = asyncio.create_task(self.test_working())
        logging_task = asyncio.create_task(self.logging_task())

        await asyncio.gather(controllers_bus, test_task, event_listener, main_flow, discord_sender, logging_task)


    def start_server(self):
        app = self.create_server()
        scheduler = self.create_scheduler()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.create_tasks(app, scheduler))
        loop.run_forever()
