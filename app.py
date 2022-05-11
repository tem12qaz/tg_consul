import asyncio

from aiogram import executor

from blocker import blocker
from db.db import db_init
from handlers import dp


async def on_startup(dp):
    await db_init()
    asyncio.get_running_loop().create_task(blocker)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
