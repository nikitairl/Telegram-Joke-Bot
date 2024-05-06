import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from db import users_db_manager

regular_router = Router()


@regular_router.message(Command(commands=["start"]))
async def send_welcome(message: Message):
    try:
        user_id = message.from_user.id
        await users_db_manager.add_user(user_id)
    except Exception as e:
        logging.error(e)
    await message.answer(
        "Hello! I'm a dad-jokes bot. You can use /help to get help."
    )


@regular_router.message(Command(commands=["stop"]))
async def send_stop(message: Message):
    try:
        user_id = message.from_user.id
        await users_db_manager.delete_user(user_id)
    except Exception as e:
        logging.error(e)
    await message.answer("Bye!")


@regular_router.message(Command(commands=["help"]))
async def send_help(message: Message):
    await message.answer(
        "I send a random dad-joke on a regular basis."
    )
