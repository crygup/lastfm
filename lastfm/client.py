from typing import Any, Dict, Optional

import aiohttp
import requests

__all__ = ["AsyncClient", "SyncClient"]
from .user import User


class AsyncClient:
    def __init__(
        self, api_key: str, session: Optional[aiohttp.ClientSession] = None
    ) -> None:
        self.session = session
        self.api_key = api_key
        self.base_url = "http://ws.audioscrobbler.com/2.0"

    async def _create_session(self) -> aiohttp.ClientSession:
        if not self.session:
            self.session = aiohttp.ClientSession()

        return self.session

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args: Any):
        await self.close()

    async def close(self) -> None:
        if self.session:
            await self.session.close()

    async def _request(
        self, endpoint: str, params: Optional[Dict[Any, Any]] = None
    ) -> Dict[Any, Any]:

        self.session = await self._create_session()

        params = params or {}
        params.update({"api_key": self.api_key, "format": "json", "method": endpoint})

        async with self.session.get(f"{self.base_url}", params=params) as resp:
            # handle errors later
            if resp.status != 200:
                raise Exception(f"An error occurred, status code {resp.status}")

            return await resp.json()

    async def fetch_user(self, username: str) -> User:
        data = await self._request(endpoint="user.getinfo", params={"user": username})

        return User(data)


class SyncClient:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.base_url = "http://ws.audioscrobbler.com/2.0"

    async def __enter__(self):
        return self

    def _request(
        self, endpoint: str, params: Optional[Dict[Any, Any]] = None
    ) -> Dict[Any, Any]:

        params = params or {}
        params.update({"api_key": self.api_key, "format": "json", "method": endpoint})

        response = requests.get(self.base_url, params=params)
        return response.json()

    def fetch_user(self, username: str) -> User:
        data = self._request(endpoint="user.getinfo", params={"user": username})

        return User(data)
