from sqlalchemy.ext.asyncio import AsyncSession

from answers.adapters.db.db_models import User


async def get_or_crete_user(user_id: str, session: AsyncSession) -> User:

    user = await get_user(user_id=user_id, session=session)
    if user is None:
        user = User(id=user_id)
        session.add(user)
        await session.flush()
    return user


async def get_user(user_id: str, session: AsyncSession) -> User | None:
    return await session.get(User, user_id)
