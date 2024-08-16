from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from sqlalchemy.ext.asyncio import AsyncSession

from database.queries.pet_query import create_pet, get_pet
from database.models.pet import Pet
from bot.keyboards.inline import get_inline_buttons

router = Router()


@router.message(F.text.casefold() == 'секретное слово')
async def take_pet(message: Message, session: AsyncSession):
    telegram_id = message.from_user.id
    pet = await get_pet(session, telegram_id)
    if not pet:
        await create_pet(session, telegram_id)
        await message.answer('Congratulations\\!')
        return
    await message.answer('У вас уже есть питомец\\. Можете посмотреть командой "мой пэт"')


async def generate_pet_caption(pet: Pet) -> str:
    return (
        f'🦎*Имя*: {pet.name}\n⭐️*Уровень*: {pet.level}\n✨*Опыт*: {pet.experience}/{pet.max_experience}\n'
        f'❤️*Состояние*: {"Здоровый" if pet.state else "Ранен"}\n🦗*Жучки*: {pet.money}\n\n*Достижения*:\n\n'
        f'🎖*Победы*: 0\n☠️*Поражения*: 0'
    )


@router.message(F.text.casefold() == 'мой пэт')
async def send_pet_info(message: Message, session: AsyncSession):
    telegram_id = message.from_user.id
    pet = await get_pet(session, telegram_id)
    if not pet:
        await message.answer('У вас еще нет питомца😶‍🌫️\n Его можно получить написав секретное слово')
        return

    image = pet.image
    if not pet.image.startswith('file_id_'):
        image = FSInputFile(pet.image)

    caption = await generate_pet_caption(pet)
    inline_keyboard = get_inline_buttons(
        buttons={
            'Информация': f'/info_{pet.id}',
            'Инвентарь': f'/inventory_{pet.id}',
            'На работу': f'/work_{pet.id}',
        },
        sizes=(2, 1)
    )

    await message.answer_photo(
        image,
        caption=caption,
        reply_markup=inline_keyboard
    )
