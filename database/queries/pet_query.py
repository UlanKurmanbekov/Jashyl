from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from database.models.pet import Pet


async def create_pet(session: AsyncSession, telegram_id: int):
    obj = Pet(telegram_id=telegram_id)
    session.add(obj)
    await session.commit()


async def get_pet(session: AsyncSession, telegram_id: int) -> Pet:
    query = select(Pet).where(Pet.telegram_id == telegram_id)
    result = await session.execute(query)
    return result.scalar()

