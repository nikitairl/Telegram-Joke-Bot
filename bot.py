import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from db import jokes_db_manager
from handlers.admin_handlers import admin_router
from handlers.user_handlers import regular_router
from handlers.bot_handlers import send_message_to_everyone


PATH = os.path.dirname(__file__)

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=PATH + "/logs/bot.log", encoding="utf-8", level=logging.DEBUG
)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


default = DefaultBotProperties(
    parse_mode="HTML",
)
bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()
dp.include_routers(admin_router, regular_router)


async def main():
    logger.info("Bot starting...")
    scheduler = AsyncIOScheduler(
        gconfig={"apscheduler.timezone": "Europe/Moscow"}
    )
    scheduler.add_job(
        send_message_to_everyone, "cron", hour="18", args=[bot]
    )

    try:
        await jokes_db_manager.db_init()
    except Exception as e:
        logger.error(e)
    await bot.delete_webhook(drop_pending_updates=True)
    scheduler.start()
    await dp.start_polling(bot, skip_updates=True)
    logger.info("Bot started.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("RIP.")
