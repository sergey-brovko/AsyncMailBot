import motor.motor_asyncio
from dotenv import load_dotenv
import os

load_dotenv()

cluster = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('MONGODB'))
collection = cluster.testdb.testcoll


async def write_html(html_id: str, html: str) -> None:
    await collection.insert_one({'id': html_id, 'html': html})
