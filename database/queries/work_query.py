import random
from datetime import timedelta, datetime
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Pet
from database.models.work import Work, PetWorkTime


async def get_pet_work_time(session: AsyncSession, telegram_id: int) -> PetWorkTime:
    query = select(PetWorkTime).where(PetWorkTime.telegram_id == telegram_id)
    result = await session.execute(query)
    return result.scalar()


async def check_work_status(session: AsyncSession, telegram_id: int) -> tuple[bool, bool, timedelta, timedelta]:
    pet_work_time = await get_pet_work_time(session, telegram_id)
    now = datetime.utcnow()

    if not pet_work_time or not pet_work_time.work_time:
        return True, False, timedelta(0), timedelta(0)

    time_since_start_work = now - pet_work_time.work_time
    time_until_next_work = pet_work_time.next_work_time - now

    can_finish_work = time_since_start_work >= timedelta(hours=2)
    can_start_new_work = time_since_start_work >= timedelta(hours=6)

    if pet_work_time.next_work_time > now:
        time_remaining_work = pet_work_time.next_work_time - now
        return False, can_finish_work, time_since_start_work, time_remaining_work

    return can_start_new_work, can_finish_work, time_since_start_work, time_until_next_work


async def update_next_work_time(session: AsyncSession, telegram_id: int, interval: timedelta = timedelta(hours=6)) -> bool:
    pet_work_time = await get_pet_work_time(session, telegram_id)
    now = datetime.utcnow()

    if pet_work_time and pet_work_time.work_time:
        time_since_work_started = now - pet_work_time.work_time
    else:
        time_since_work_started = timedelta(3)

    if time_since_work_started >= timedelta(hours=2):
        new_next_work_time = now + interval

        query = (
            update(PetWorkTime)
            .where(PetWorkTime.telegram_id == telegram_id)
            .values(
                work_time=None,
                next_work_time=new_next_work_time
            )
        )
        await session.execute(query)
        await session.commit()
        return True

    return False


async def get_available_works(session: AsyncSession):
    query = select(Work)
    result = await session.execute(query)
    return result.scalars().all()


async def get_work(session: AsyncSession, work_id: int):
    query = select(Work).where(Work.id == work_id)
    result = await session.execute(query)
    return result.scalar()


async def assign_work_to_pet(session: AsyncSession, telegram_id: int, work_id: int) -> bool:
    can_start_new_work, _, _, _ = await check_work_status(session, telegram_id)

    if not can_start_new_work:
        return False

    pet_work_time_query = select(PetWorkTime).where(PetWorkTime.telegram_id == telegram_id)
    pet_work_time_result = await session.execute(pet_work_time_query)
    pet_work_time = pet_work_time_result.scalar()

    now = datetime.utcnow()
    if pet_work_time:
        update_query = (
            update(PetWorkTime)
            .where(PetWorkTime.telegram_id == telegram_id)
            .values(
                work_id=work_id,
                work_time=now,
                next_work_time=now + timedelta(hours=6)
            )
        )
        await session.execute(update_query)
    else:
        pet_work_time = PetWorkTime(
            telegram_id=telegram_id,
            work_id=work_id,
            work_time=now,
            next_work_time=now + timedelta(hours=6)
        )
        session.add(pet_work_time)

    await session.commit()

    pet_work_time_result = await session.execute(pet_work_time_query)
    pet_work_time = pet_work_time_result.scalar()
    print(f'Assigned work: {pet_work_time.work_id}')

    return True


async def complete_work(session: AsyncSession, telegram_id: int, reward: int, experience_gain: int, no_reward: bool, injury: bool) -> bool:
    try:
        _, can_finish_work, _, _ = await check_work_status(session, telegram_id)

        if not can_finish_work:
            print("Cannot finish work: can_finish_work is False")
            return False

        pet_work_time = await get_pet_work_time(session, telegram_id)
        if pet_work_time:
            work_id = pet_work_time.work_id

            if not work_id:
                print("Work ID is None")
                return False

            query = select(Work).where(Work.id == work_id)
            result = await session.execute(query)
            work = result.scalar()

            if not work:
                print("No work found with ID:", work_id)
                return False

            update_pet_query = (
                update(Pet)
                .where(Pet.telegram_id == telegram_id)
                .values(
                    money=Pet.money + (reward if not no_reward else 0),
                    experience=Pet.experience + (experience_gain if experience_gain is not None else 0),
                    state=False if injury else True
                )
            )
            await session.execute(update_pet_query)
            await session.commit()

            next_work_time = datetime.utcnow() + timedelta(hours=6)

            clear_work_time_query = (
                update(PetWorkTime)
                .where(PetWorkTime.telegram_id == telegram_id)
                .values(
                    work_time=None,
                    next_work_time=next_work_time,
                    work_id=None
                )
            )
            await session.execute(clear_work_time_query)
            await session.commit()
            print("Work completed successfully")
            return True

        print("No pet_work_time found for telegram_id:", telegram_id)
        return False

    except Exception as e:
        print(f"Error completing work: {e}")
        return False


