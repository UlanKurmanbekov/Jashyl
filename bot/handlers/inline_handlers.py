import random
from datetime import timedelta

from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from bot.keyboards.inline import get_inline_buttons
from database.queries.pet_query import get_pet, check_feed_status, update_pet_experience, update_next_feed_time
from database.queries.work_query import (
    check_work_status,
    complete_work,
    assign_work_to_pet,
    update_next_work_time,
    get_available_works,
    get_pet_work_time,
    get_work
)
from utils import format_timedelta

router = Router(name=__name__)


@router.message(F.text == '@JashylBot Информация')
async def get_action_info(message: Message, session: AsyncSession):
    telegram_id = message.from_user.id
    if not await get_pet(session, telegram_id):
        await message.answer('У вас еще нет питомца😣')
        return

    feed_status = await check_feed_status(session, telegram_id)
    can_feed_pet = feed_status[0]

    can_start_new_work, can_finish_work, time_since_start_work, time_until_next_work = await check_work_status(session, telegram_id)

    if can_finish_work:
        work_message = 'Можно завершить работу'
    elif not can_start_new_work:
        if time_since_start_work < timedelta(hours=2):  # Если питомец сейчас работает
            remaining_work_time = timedelta(hours=2) - time_since_start_work
            work_message = f'Осталось {format_timedelta(remaining_work_time)} до конца работы'
        else:
            work_message = f'Следующая работа будет доступна через {format_timedelta(time_until_next_work)}'
    else:
        work_message = 'Можно отправить на работу'

    buttons = {}
    if can_feed_pet:
        buttons['Покормить питомца'] = 'Покормить питомца'
    if can_start_new_work and not can_finish_work:
        buttons['На работу'] = 'На работу'
    elif can_finish_work:
        buttons['Завершить работу'] = 'Завершить работу'
    buttons['Мой питомец'] = 'Мой питомец'

    inline_keyboard = get_inline_buttons(
        buttons=buttons,
        sizes=(2, 1),
        switch_inline=True
    )

    await message.answer(
        f'🍎 {"Можно кормить" if can_feed_pet else f"Можно покормить через {format_timedelta(feed_status[1])}"}\n'
        f'💼 {work_message}',
        reply_markup=inline_keyboard
    )


@router.message(F.text == '@JashylBot Инвентарь')
async def get_inventory_info(message: Message, session: AsyncSession):
    await message.answer('Инвентарь скоро будет')


@router.message(F.text == '@JashylBot На работу')
async def to_work(message: Message, session: AsyncSession):
    telegram_id = message.from_user.id

    if not await get_pet(session, telegram_id):
        await message.answer('У вас еще нет питомца😣')
        return

    can_start_new_work, can_finish_work, time_since_start_work, time_until_next_work = await check_work_status(session, telegram_id)

    if can_finish_work:
        await message.answer(
            'Ваш питомец завершил работу\\. Пожалуйста, завершите работу перед началом новой',
            reply_markup=get_inline_buttons(
                buttons={'Завершить работу': 'Завершить работу'},
                switch_inline=True
            )
        )
        return

    if not can_start_new_work:
        if time_since_start_work < timedelta(hours=2):
            remaining_work_time = timedelta(hours=2) - time_since_start_work
            await message.answer(
                f'Ваш питомец сейчас работает\\. Осталось {format_timedelta(remaining_work_time)} до конца работы'
            )
        else:
            await message.answer(
                f'Ваш питомец отдыхает после работы\\. Следующая работа будет доступна через {format_timedelta(time_until_next_work)}'
            )
        return

    works = await get_available_works(session)
    buttons = {}
    template_text = ''

    for index, work in enumerate(works):
        name = ''
        if index == 0:
            name = f'🕴️*{work.name}*'
            buttons[f'{work.name}'] = f'Работа стояльщик в очереди'
        elif index == 1:
            name = f'🦀*{work.name}*'
            buttons[f'{work.name}'] = f'Работа ловец крабов'
        elif index == 2:
            name = f'☕*{work.name}*'
            buttons[f'{work.name}'] = f'Работа в кофейне'

        description = work.description.replace('.', '\\.').replace(',', '\\,')
        template_text += f'{name}\n{description}\n\n'

    reply_markup = get_inline_buttons(
        buttons=buttons,
        sizes=(1,),
        switch_inline=True
    )

    await message.answer(template_text, reply_markup=reply_markup)


@router.message(F.text.startswith('@JashylBot Работа'))
async def select_work(message: Message, session: AsyncSession):
    telegram_id = message.from_user.id
    if not await get_pet(session, telegram_id):
        await message.answer('У вас еще нет питомца😣')
        return

    work_id = 0
    if message.text == '@JashylBot Работа стояльщик в очереди':
        work_id = 1
    elif message.text == '@JashylBot Работа ловец крабов':
        work_id = 2
    elif message.text == '@JashylBot Работа в кофейне':
        work_id = 3
    else:
        await message.answer('Выбранная работа не найдена')
        return

    work = await get_work(session, work_id)
    pet_work_time = await get_pet_work_time(session, telegram_id)

    if pet_work_time:
        can_start_new_work, _, _, _ = await check_work_status(session, telegram_id)
        if not can_start_new_work:
            work_status = await check_work_status(session, telegram_id)
            remaining_time = format_timedelta(work_status[3])
            await message.answer(f'Вам нужно подождать ещё {remaining_time} перед тем как начать новую работу')
            return

        await update_next_work_time(session, telegram_id)
        await assign_work_to_pet(session, telegram_id, work.id)  # Добавлено сюда для верности
        await message.answer(f'Вы успешно выбрали работу: {work.name}')
    else:
        await assign_work_to_pet(session, telegram_id, work.id)
        await message.answer(f'Вы успешно выбрали работу: {work.name}')


@router.message(F.text == '@JashylBot Завершить работу')
async def finish_work(message: Message, session: AsyncSession):
    telegram_id = message.from_user.id
    can_start_new_work, can_finish_work, _, _ = await check_work_status(session, telegram_id)

    if not can_finish_work:
        await message.answer('Вы не можете завершить работу сейчас')
        return

    pet_work_time = await get_pet_work_time(session, telegram_id)
    if not pet_work_time or not pet_work_time.work_id:
        await message.answer('Не найдена информация о текущей работе питомца')
        return

    work_id = pet_work_time.work_id
    work = await get_work(session, work_id)
    if not work:
        await message.answer('Не найдена информация о работе')
        return

    reward = random.randint(work.min_reward, work.max_reward)
    experience_gain = 0
    no_reward = False
    injury = False

    if work.work_type_id == 1:
        experience_gain = 1 if random.randint(0, 100) <= 15 else 0
    elif work.work_type_id == 2:
        no_reward = True if random.randint(0, 100) <= work.chance_no_reward else False
    elif work.work_type_id == 3:
        injury = True if random.randint(0, 100) <= work.chance_injury else False

    success = await complete_work(session, telegram_id, reward, experience_gain, no_reward, injury)
    message_template = f'🐞: *\\+{reward} жучков*\n'
    if experience_gain:
        message_template += f'✨: *\\+1 к опыту*\n'

    if success:
        await message.answer('Работа завершена успешно\\!\n' + message_template)
    else:
        await message.answer('Произошла ошибка при завершении работы')


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
    await update_next_feed_time(session, telegram_id)

    await message.answer(
        f'Вы успешно покормили питомца\\!\n'
        f'✨: *\\+1 к опыту*\n'
        f'🐞: *\\+50 жучков*'
    )
