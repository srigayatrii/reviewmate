import asyncio

from app.ai.client import AIClient


async def main():

    client = AIClient()

    patch = """
diff --git a/main.py b/main.py
index 123..456 100644

- password = "123456"
+ password = os.getenv("PASSWORD")
"""

    result = await client.review_patch(patch)

    print(result)


asyncio.run(main())