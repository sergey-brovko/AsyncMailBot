import motor.motor_asyncio
import os


cluster = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('MONGODB_URL'))
collection = cluster.testdb.testcoll


async def write_html(html_id: str, html: str) -> None:
    await collection.insert_one({'id': html_id, 'html': html})
