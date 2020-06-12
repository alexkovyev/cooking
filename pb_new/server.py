import asyncio
from aiohttp import web
import time

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import SERVER_HOST, SERVER_PORT
from controllers.ControllerBus import ControllersEvents, event_generator
from urls import setup_routes
from views import hardware_broke_handler


class PizzaBotMain(object):

    def __init__(self):
        # в чем разница в статусе и mode
        self.status = "ready"
        self.current_object_mode = "sleeping"
        self.equipment = None
        self.cntrls_events = ControllersEvents()

    def create_server(self):
        app = web.Application()
        setup_routes(app)
        return app

    def create_scheduler(self):
        scheduler = AsyncIOScheduler()
        scheduler.add_job(self.test_scheduler, 'interval', seconds=5)
        return scheduler

    async def test_working(self):
        while True:
            print("запускается фоновая задача", time.time())
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
        pass

    async def create_tasks(self, app, scheduler):
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host=SERVER_HOST, port=SERVER_PORT)
        await site.start()
        scheduler.start()
        # Переделать потом на генерацию из списка
        controllers_bus = asyncio.create_task(event_generator(self.cntrls_events))
        test_task = asyncio.create_task(self.test_working())
        event_listener = asyncio.create_task(self.create_hardware_broke_listener())

        await asyncio.gather(controllers_bus, test_task, event_listener)

    def start_server(self):
        app = self.create_server()
        scheduler = self.create_scheduler()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.create_tasks(app, scheduler))
        loop.run_forever()
