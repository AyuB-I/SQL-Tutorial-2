from aiogram import Dispatcher
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.infrastucture.database.functions.users import create_user
from tgbot.infrastucture.database.models.users import User


async def user_start(message: Message, session: AsyncSession):
    user = await session.get(User, message.from_user.id)

    if not user:
        await create_user(
            session,
            telegram_id=message.from_user.id,
            full_name=message.from_user.full_name,
            username=message.from_user.username,
            language_code=message.from_user.language_code,
        )
        await session.commit()

    user = await session.get(User, message.from_user.id)
    user_info = (f"{user.full_name} (@{user.username}).\n"
                 f"Language: {user.language_code}.\n"
                 f"Created at: {user.created_at}.")

    await message.reply("Hello, user. \n"
                        "Your info is here: \n\n"
                        f"{user_info}")


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
