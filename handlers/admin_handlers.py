import logging
import os

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from bot_init import bot
from db import jokes_db_manager, users_db_manager
from handlers.filters.filters import IsAdmin
from keyboards import admin_keyboard

ADMIN_ID = int(os.getenv("ADMIN_ID"))

admin_ids = [
    ADMIN_ID,
]

admin_router = Router()


@admin_router.message(Command(commands=["admin"]))
async def send_admins(message: Message):
    await message.answer("Admin panel:", reply_markup=admin_keyboard)


class Jokes(StatesGroup):
    joke_text = State()


class SendMessage(StatesGroup):
    message_text = State()


@admin_router.message(IsAdmin(admin_ids), Command(commands="add_joke"))
async def add_joke_first_step(message: Message, state: FSMContext):
    await state.set_state(Jokes.joke_text)
    await message.answer("Send me a joke!")


@admin_router.message(IsAdmin(admin_ids), Jokes.joke_text)
async def add_joke_second_step(message: Message, state: FSMContext):
    await state.update_data(joke_text=message.text)
    data = await state.get_data()
    await message.answer(f"Done. Joke: {data['joke_text']}.")
    try:
        new_doc = await jokes_db_manager.add_document(data["joke_text"])
        await message.answer(new_doc)
        await state.clear()
    except Exception as e:
        logging.error(e)
        await message.answer("Something went wrong. Try again later.")


@admin_router.message(
    IsAdmin(admin_ids), Command(commands="send_custom_message")
)
async def send_message_first_step(message: Message, state: FSMContext):
    await state.set_state(SendMessage.message_text)
    await message.answer("Send me a message!")


@admin_router.message(IsAdmin(admin_ids), SendMessage.message_text)
async def send_message_second_step(message: Message, state: FSMContext):
    await state.update_data(message_text=message.text)
    data = await state.get_data()
    await message.answer(f"Message: {data['message_text']}.")
    user_ids = await users_db_manager.get_all_users()
    for user_id in user_ids:
        await bot.send_message(user_id["user_id"], data["message_text"])
    await message.answer("Message sent!")
    await state.clear()
