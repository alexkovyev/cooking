"""Этот модуль управляет событиями от контроллеров"""

import asyncio


controllers_alarm = asyncio.Event()

async def controllers_alarm_handler():
    controllers_alarm.set()