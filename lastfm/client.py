from typing import Any, Dict, List, Optional

import aiohttp

__all__ = ["AsyncClient"]
from .user import User
from .errors import InvalidArguments
from .artist import Artist, SimilarArtist, SearchArtist, TrackArtist, MiniArtist
from .track import AritstTrack
from .image import Image


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
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[Any, Any]] = None,
        **kwargs,
    ) -> Dict[Any, Any]:

        self.session = await self._create_session()

        params = params or {}
        params.update({"api_key": self.api_key, "format": "json", "method": endpoint})
        params = {k: v for k, v in params.items() if v is not None}

        async with self.session.request(
            method, f"{self.base_url}", params=params, **kwargs
        ) as resp:
            data: Dict[Any, Any] = await resp.json()

            if data.get("error"):
                raise BaseException(data.get("message"))

            return data

    async def fetch_user(self, username: str) -> User:
        data = await self._request(
            "GET", endpoint="user.getinfo", params={"user": username}
        )

        return User(data)

    async def fetch_artist(
        self,
        artist: Optional[str] = None,
        mbid: Optional[str] = None,
        username: Optional[str] = None,
    ) -> Artist:
        """Searches an artist

        Artist argument is not required if using mbid argument"""

        if not artist and not mbid:
            raise InvalidArguments(
                "You either need to provide artist OR mbid for this function."
            )

        results = await self._request(
            "GET",
            endpoint="artist.getInfo",
            params={"artist": artist, "mbid": mbid, "username": username},
        )
        data: Dict[Any, Any] = results["artist"]
        stats: Dict[Any, Any] = data["stats"]

        userplaycount = stats.get("userplaycount")

        def format_data(data: Dict[Any, Any]) -> MiniArtist:
            return MiniArtist(
                url=data["url"],
                name=data["name"],
                images=[Image(ImageData) for ImageData in data["image"]],
            )

        return Artist(
            name=data["name"],
            musicbrainz_id=data.get("mbid"),
            url=data["url"],
            images=[Image(ImageData) for ImageData in data["image"]],
            streamable=data["streamable"],
            ontour=data["ontour"],
            listeners=int(stats["listeners"]),
            playcount=int(stats["playcount"]),
            similar=[
                format_data(SimilarData) for SimilarData in data["similar"]["artist"]
            ],
            userplaycount=int(userplaycount) if userplaycount else None,
        )

    async def fetch_similar_artists(
        self,
        artist: Optional[str] = None,
        mbid: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[SimilarArtist]:
        """Searches similar artists to one provided

        Artist argument is not required if using mbid argument"""

        if not artist and not mbid:
            raise InvalidArguments(
                "You either need to provide artist OR mbid for this function."
            )

        results = await self._request(
            "GET",
            endpoint="artist.getsimilar",
            params={"artist": artist, "mbid": mbid, "limit": limit},
        )

        def format_data(data: Dict[Any, Any]) -> SimilarArtist:
            return SimilarArtist(
                name=data["name"],
                musicbrainz_id=data.get("mbid"),
                match=data["match"],
                url=data["url"],
                images=[Image(ImageData) for ImageData in data["image"]],
                streamable=data["streamable"],
            )

        return [format_data(data) for data in results["similarartists"]["artist"]]

    async def search_artists(
        self,
        artist: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
    ) -> List[SearchArtist]:
        """Searches for an artists"""

        results = await self._request(
            "GET",
            endpoint="artist.search",
            params={"artist": artist, "limit": limit, "page": page},
        )

        def format_data(data: Dict[Any, Any]) -> SearchArtist:
            return SearchArtist(
                name=data["url"],
                listeners=int(data["listeners"]),
                musicbrainz_id=data.get("mbid"),
                url=data["url"],
                streamable=data["streamable"],
                images=[Image(ImageData) for ImageData in data["image"]],
            )

        return [
            format_data(data) for data in results["results"]["artistmatches"]["artist"]
        ]

    async def fetch_artist_top_tracks(
        self,
        artist: Optional[str] = None,
        mbid: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
    ) -> List[AritstTrack]:
        """Fetches an artist's top tracks

        Artist argument is not required if using mbid argument"""

        if not artist and not mbid:
            raise InvalidArguments(
                "You either need to provide artist OR mbid for this function."
            )

        results = await self._request(
            "GET",
            endpoint="artist.getTopTracks",
            params={"artist": artist, "limit": limit, "page": page, "mbid": mbid},
        )

        def format_data(data: Dict[Any, Any]) -> AritstTrack:
            return AritstTrack(
                name=data["name"],
                playcount=int(data["playcount"]),
                listeners=int(data["listeners"]),
                url=data["url"],
                streamable=data["streamable"],
                artist=TrackArtist(
                    name=data["artist"]["name"],
                    musicbrainz_id=data["artist"].get("mbid"),
                    url=data["artist"]["url"],
                ),
                images=[Image(ImageData) for ImageData in data["image"]],
            )

        return [format_data(data) for data in results["toptracks"]["track"]]
