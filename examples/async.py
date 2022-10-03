import asyncio
import lastfm


async def main():
    async with lastfm.AsyncClient("api_key_here") as client:
        oqt = await client.fetch_user("oqt")

        print(oqt.playcount)


asyncio.run(main())
