from sqlalchemy.ext.asyncio import AsyncSession
from database.models.user import User


async def create_user(session: AsyncSession, data: dict):
    user = User(
        first_name=data['first_name'],
        username=data['username'],
        telegram_id=data['telegram_id']
    )
    session.add(user)
    await session.commit()
