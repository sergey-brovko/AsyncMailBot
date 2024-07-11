import motor.motor_asyncio
from dotenv import load_dotenv
import os

load_dotenv()

cluster = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('MONGODB'))
collection = cluster.testdb.testcoll
