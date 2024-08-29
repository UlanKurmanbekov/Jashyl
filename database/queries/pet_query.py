from datetime import datetime, timedelta

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from database.models.pet import Pet, PetFeedTime
from database.models.work import PetWorkTime


async def create_pet(session: AsyncSession, telegram_id: int):
    pet = Pet(telegram_id=telegram_id)
    now = datetime.utcnow()
    pet_feed_time = PetFeedTime(
        telegram_id=telegram_id,
        feed_time=now,
        next_feed_time=now
    )

    session.add(pet)
    session.add(pet_feed_time)

    await session.commit()


async def get_pet(session: AsyncSession, telegram_id: int) -> Pet:
    query = select(Pet).where(Pet.telegram_id == telegram_id)
    result = await session.execute(query)
    return result.scalar()


async def check_feed_status(session: AsyncSession, telegram_id: int) -> tuple[bool, timedelta]:
    query = select(PetFeedTime).where(PetFeedTime.telegram_id == telegram_id)
    result = await session.execute(query)
    pet_feed_time = result.scalar()

    now = datetime.utcnow()
    time_until_feed = pet_feed_time.next_feed_time - now
    can_feed = time_until_feed <= timedelta(seconds=0)

    return can_feed, time_until_feed


async def update_pet_experience(session: AsyncSession, telegram_id: int, experience_gain: int = 1, money: int = 50):
    query = update(Pet).where(Pet.telegram_id == telegram_id).values(
        experience=Pet.experience + experience_gain,
        money=Pet.money + money
    )
    await session.execute(query)
    await session.commit()


async def update_next_feed_time(session: AsyncSession, telegram_id: int, interval: timedelta = timedelta(hours=6)):
    query = (
        update(PetFeedTime)
        .where(PetFeedTime.telegram_id == telegram_id)
        .values(
            feed_time=datetime.utcnow(),
            next_feed_time=datetime.utcnow() + interval
        )
    )
    await session.execute(query)
    await session.commit()

