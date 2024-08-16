import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.middlewares.data_base_session import DataBaseSession
from core.config import settings
from database.db_helper import db_helper
from bot.handlers.start import router
from utils.logger import configure_logging


bot = Bot(token=settings.run.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2))
dp = Dispatcher()
dp.include_router(router)


async def main():
    configure_logging()
    dp.update.middleware(DataBaseSession(session_pool=db_helper.session_factory))
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    asyncio.run(main())
