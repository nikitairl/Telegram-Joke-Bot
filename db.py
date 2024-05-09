from bson.objectid import ObjectId
import json
import logging
import os

import motor.motor_asyncio
from constants import DESC


client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_URL"))
db = client["jokes"]
collection_jokes = db["jokes"]
collection_users = db["users"]


class JokesDatabaseManager:
    async def db_init(self):
        if not await self.check_db("jokes"):
            logging.info("Jokes db not found, creating from jokes.json...")
            with open("jokes.json") as f:
                file_data = json.load(f)
                await collection_jokes.insert_many(file_data)
            logging.info("Jokes db created")
        else:
            logging.info("Skipping db creation")

    async def check_db(self, db_name: str):
        try:
            db_list = await client.list_database_names()
            return db_name in db_list
        except Exception as e:
            logging.error(f"Error checking database: {e}")
            return False

    async def get_document(self, order: str = DESC):
        try:
            cursor = (
                collection_jokes.find({})
                .sort("_id", int(order))
                .limit(1)
            )
            return await cursor.to_list(length=1)
        except Exception as e:
            logging.error(f"Error getting document: {e}")

    async def get_all_documents(self, order: str = DESC):
        try:
            cursor = collection_jokes.find({}, {"_id": False}).sort(
                "_id", order
            )
            return await cursor.to_list(length=None)
        except Exception as e:
            logging.error(f"Error getting documents: {e}")

    async def add_document(self, text: str):
        try:
            if text in [doc["text"] for doc in await self.get_all_documents()]:
                return 'Document already exists'
            document = {"text": text}
            await collection_jokes.insert_one(document)
            return f'Document {document["_id"]} added with text: "{text}"'
        except Exception as e:
            logging.error(f"Error adding document: {e}")

    async def delete_document(self, id):
        try:
            await collection_jokes.delete_one({'_id': ObjectId(id)})
        except Exception as e:
            logging.error(f"Error deleting document: {e}")

    async def get_random_document(self):
        try:
            cursor = collection_jokes.aggregate(
                [{"$sample": {"size": 1}}, {"$project": {"_id": False}}]
            )
            return await cursor.to_list(length=1)
        except Exception as e:
            logging.error(f"Error getting random document: {e}")

    async def get_last_ten_documents(self):
        try:
            cursor = (
                collection_jokes.find({}, {"_id": False})
                .sort("_id", DESC)
                .limit(10)
            )
            return await cursor.to_list(length=10)
        except Exception as e:
            logging.error(f"Error getting last ten documents: {e}")

    async def get_first_joke(self):
        try:
            first_document = await self.get_document()
            return first_document
        except Exception as e:
            logging.error(f"Error getting first document and shuffling: {e}")


class UsersDatabaseManager:
    async def add_user(self, user_id: int):
        try:
            if await self.check_user(user_id) is not None:
                return logging.info("User already exists")
            await collection_users.insert_one({"user_id": user_id})
        except Exception as e:
            logging.error(f"Error adding user: {e}")

    async def delete_user(self, user_id: int):
        try:
            await collection_users.delete_one({"user_id": user_id})
        except Exception as e:
            logging.error(f"Error deleting user: {e}")

    async def get_all_users(self):
        try:
            cursor = collection_users.find({}, {"_id": False})
            return await cursor.to_list(length=None)
        except Exception as e:
            logging.error(f"Error getting all users: {e}")

    async def check_user(self, user_id: int):
        try:
            return await collection_users.find_one({"user_id": user_id})
        except Exception as e:
            logging.error(f"Error checking user: {e}")


jokes_db_manager = JokesDatabaseManager()
users_db_manager = UsersDatabaseManager()

# TESTING GROUND

# async def main():
#     db_manager = JokesDatabaseManager()
#     sample = await db_manager.delete_document("6")
#     print(sample)
#     print(await db_manager.get_all_documents())
# import asyncio
# asyncio.run(main())
