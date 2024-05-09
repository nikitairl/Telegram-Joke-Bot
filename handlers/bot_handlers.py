import logging

from db import users_db_manager, jokes_db_manager


async def send_message_to_everyone_and_shuffle(bot):
    # joke = await jokes_db_manager.get_random_document()
    joke = await jokes_db_manager.get_first_joke()
    logging.info(joke)
    user_ids = await users_db_manager.get_all_users()
    for user_id in user_ids:
        await bot.send_message(user_id["user_id"], joke[0]["text"])
    logging.info("Joke sent")
    await jokes_db_manager.delete_document(joke[0]["_id"])
    logging.info("Joke deleted")
    await jokes_db_manager.add_document(joke[0]["text"])
    logging.info("Joke put back")
