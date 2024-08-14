import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from core.config import settings, configure_logging


bot = Bot(token=settings.run.bot_token)
dp = Dispatcher()


@dp.message(Command('start'))
async def start(message: Message):
    await message.answer('УРА!')


async def main():
    configure_logging()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    asyncio.run(main())
