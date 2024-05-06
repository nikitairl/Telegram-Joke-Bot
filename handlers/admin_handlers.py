import logging
import os

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from db import jokes_db_manager
from handlers.filters.filters import IsAdmin

ADMIN_ID = int(os.getenv("ADMIN_ID"))

admin_ids = [
    ADMIN_ID,
]

admin_router = Router()


class Jokes(StatesGroup):
    joke_text = State()


@admin_router.message(IsAdmin(admin_ids), Command(commands="add_joke"))
async def add_joke_first_step(message: Message, state: FSMContext):
    await state.set_state(Jokes.joke_text)
    await message.answer("Send me a joke!")


@admin_router.message(Jokes.joke_text)
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
