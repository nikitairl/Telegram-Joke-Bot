import logging

from db import users_db_manager, jokes_db_manager


async def send_message_to_everyone(bot):
    joke = await jokes_db_manager.get_random_document()
    user_ids = await users_db_manager.get_all_users()
    logging.info(user_ids)
    for user_id in user_ids:
        await bot.send_message(user_id['user_id'], joke[0]['text'])
