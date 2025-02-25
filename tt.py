from AI import AI
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
base_url = os.getenv("BASE_URL")
api_key = os.getenv("API_KEY")
model = os.getenv("MODEL")

ai = AI(
    base_url=base_url,
    api_key=api_key,
    model=model # ep-20250219163101-p5zk6
)


async def callback(file, t, isEnd):
    print(t)


async def main():
    asyncio.create_task(ai.send("你是谁", callback))
    await asyncio.sleep(19)


asyncio.run(main())