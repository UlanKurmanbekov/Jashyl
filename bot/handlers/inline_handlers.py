from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from bot.keyboards.inline import get_inline_buttons
from database.queries.pet_query import get_pet, check_feed_status, update_pet_experience, update_feed_time
from utils import format_timedelta

router = Router(name=__name__)


@router.message(F.text == '@JashylBot Информация')
async def get_action_info(message: Message, session: AsyncSession):
    telegram_id = message.from_user.id
    if not await get_pet(session, telegram_id):
        await message.answer('У вас еще нет питомца😣')
        return

    inline_keyboard = get_inline_buttons(
        buttons={
            'Покормить питомца': 'Покормить питомца',
            'На работу': f'На работу',
            'Мой питомец': 'Мой питомец'
        },
        sizes=(2, 1)
    )
    feed_status = await check_feed_status(session, telegram_id)
    await message.answer(
        f'🌯 {"Можно кормить" if feed_status[0] else f"Можно покормить через {format_timedelta(feed_status[1])}"}\n'
        '💼 Можно отправить на работу',
        reply_markup=inline_keyboard
    )


@router.message(F.text == '@JashylBot Инвентарь')
async def get_inventory_info(message: Message, session: AsyncSession):
    await message.answer('Инвентарь')


@router.message(F.text == '@JashylBot На работу')
async def to_wort(message: Message, session: AsyncSession):
    await message.answer('На работу')


@router.message(F.text == '@JashylBot Покормить питомца')
async def feed_pet(message: Message, session: AsyncSession):
    telegram_id = message.from_user.id
    if not await get_pet(session, telegram_id):
        await message.answer('У вас еще нет питомца😣')
        return

    feed_status = await check_feed_status(session, telegram_id)
    if not feed_status[0]:
        remaining_time = format_timedelta(feed_status[1])
        await message.answer(f'Время следующего кормления через {remaining_time}')
        return

    await update_pet_experience(session, telegram_id)
    await update_feed_time(session, telegram_id)

    await message.answer(
        f'Вы успешно покормили питомца\\!\n'
        f'✨: *\\+1 к опыту*\n'
        f'🐞: *\\+50 жучков*'
    )
