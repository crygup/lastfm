import asyncio
import lastfm


async def main():
    async with lastfm.AsyncClient("api_key_here") as client:
        user = await client.fetch_user("crygup")

        print(user.playcount)


asyncio.run(main())
