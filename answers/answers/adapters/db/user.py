from sqlalchemy.ext.asyncio import AsyncSession

from answers.adapters.db.db_models import User


async def get(user_id: str, session: AsyncSession) -> User | None:
    return await session.get(User, user_id)


async def create(user_id: str, session: AsyncSession) -> User:
    user = User(id=user_id)
    session.add(user)
    await session.commit()
    return user


async def get_or_create(user_id: str, session: AsyncSession) -> User:
    user = await get(user_id=user_id, session=session)
    if user is None:
        user = await create(user_id=user_id, session=session)
    return user
