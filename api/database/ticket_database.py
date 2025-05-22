from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://root:example@mongodb:27017/?authSource=admin")

client = AsyncIOMotorClient(MONGO_URL)
database = client["ticketapi"]
ticket_collection = database["ticket"]
