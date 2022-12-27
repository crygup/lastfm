from typing import Any, Dict, List, Optional

import aiohttp
from dateutil.parser import parse

__all__ = ["AsyncClient"]
from .album import Album, ArtistTopAlbum, UserRecentTrackAlbum
from .artist import (
    Artist,
    ArtistSimilar,
    MiniArtist,
    SearchArtist,
    SimilarArtist,
    UserRecentTrackArtist,
)
from .attr import UserRecentTrackAttr
from .errors import InvalidArguments
from .image import Image
from .tags import AlbumTag
from .track import ArtistTopTrack, UserRecentTrack
from .user import User
from .wiki import AlbumWiki


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

        def format_data(data: Dict[Any, Any]) -> ArtistSimilar:
            return ArtistSimilar(
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
    ) -> List[ArtistTopTrack]:
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

        def format_data(data: Dict[Any, Any]) -> ArtistTopTrack:
            return ArtistTopTrack(
                name=data["name"],
                playcount=int(data["playcount"]),
                listeners=int(data["listeners"]),
                url=data["url"],
                streamable=data["streamable"],
                artist=MiniArtist(
                    name=data["artist"]["name"],
                    musicbrainz_id=data["artist"].get("mbid"),
                    url=data["artist"]["url"],
                ),
                images=[Image(ImageData) for ImageData in data["image"]],
            )

        return [format_data(data) for data in results["toptracks"]["track"]]

    async def fetch_artist_top_albums(
        self,
        artist: Optional[str] = None,
        mbid: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
    ) -> List[ArtistTopAlbum]:
        """Fetches an artist's top albums

        Artist argument is not required if using mbid argument"""

        if not artist and not mbid:
            raise InvalidArguments(
                "You either need to provide artist OR mbid for this function."
            )

        results = await self._request(
            "GET",
            endpoint="artist.getTopAlbums",
            params={"artist": artist, "limit": limit, "page": page, "mbid": mbid},
        )

        def format_data(data: Dict[Any, Any]) -> ArtistTopAlbum:
            return ArtistTopAlbum(
                name=data["name"],
                playcount=data["playcount"],
                url=data["url"],
                artist=MiniArtist(
                    name=data["artist"]["name"],
                    musicbrainz_id=data["artist"].get("mbid"),
                    url=data["url"],
                ),
                images=[Image(ImageData) for ImageData in data["image"]],
            )

        return [format_data(data) for data in results["topalbums"]["album"]]

    async def fetch_album(
        self,
        artist: Optional[str] = None,
        album: Optional[str] = None,
        mbid: Optional[str] = None,
        username: Optional[str] = None,
    ) -> Album:
        """Fetches info on an album

        Artist and album arguments are not required if using mbid argument"""
        if not mbid:
            if not artist and not album:
                raise InvalidArguments(
                    "You either need to provide artist and album OR mbid for this function."
                )

            if (artist and not album) or (album and not artist):
                raise InvalidArguments(
                    "You need to provide artist AND album for this function"
                )

        results = await self._request(
            "GET",
            endpoint="album.getinfo",
            params={
                "artist": artist,
                "album": album,
                "mbid": mbid,
                "username": username,
            },
        )

        data: Dict[Any, Any] = results["album"]

        tag_data: Optional[Dict[Any, Any]] = data.get("tags")
        wiki_data: Optional[Dict[Any, Any]] = data.get("wiki")

        tags = (
            [AlbumTag(url=data["url"], name=data["name"]) for data in tag_data["tag"]]
            if tag_data
            else None
        )

        wiki: Optional[AlbumWiki] = None

        if wiki_data:
            try:
                published = parse(wiki_data["published"])
            except:  # blank except because last.fm api sucks and there are too many things to handle just for me to say its None
                published = None

            wiki = AlbumWiki(
                published=published,
                summary=wiki_data.get("summar"),
                content=wiki_data.get("content"),
            )

        return Album(
            artist=data["artist"],
            musicbrainz_id=data.get("mbid"),
            tags=tags,
            playcount=int(data["playcount"]),
            images=[Image(ImageData) for ImageData in data["image"]],
            url=data["url"],
            name=data["name"],
            userplaycount=data.get("userplaycount"),
            listeners=int(data["listeners"]),
            wiki=wiki,
        )

    async def fetch_user_recent_tracks(
        self,
        user: str,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        extended: Optional[bool] = None,
        to: Optional[int] = None,
    ) -> List[UserRecentTrack]:
        """Fetches a user's recent tracks

        `to` argument is in UNIX time"""

        results = await self._request(
            "GET",
            endpoint="user.getRecentTracks",
            params={
                "user": user,
                "limit": limit,
                "page": page,
                "extended": "1" if extended else None,
                "to": to,
            },
        )

        def format_data(data: Dict[Any, Any]) -> UserRecentTrack:
            artist_data: Dict[Any, Any] = data["artist"]
            album_data: Dict[Any, Any] = data["album"]
            attr_data: Dict[Any, Any] = results["recenttracks"]["@attr"]

            artist = UserRecentTrackArtist(
                musicbrainz_id=artist_data.get("mbid"),
                name=artist_data.get("name") if extended else artist_data.get("#test"),  # type: ignore
                url=artist_data.get("url"),
                images=[Image(ImageData) for ImageData in data["image"]]
                if extended
                else None,
            )

            album = UserRecentTrackAlbum(
                musicbrainz_id=album_data.get("mbid"), name=album_data["#text"]
            )

            try:
                now_playing = bool(data["@attr"]["nowplaying"])
            except KeyError:
                now_playing = False

            attr = UserRecentTrackAttr(
                user=attr_data["user"],
                total_pages=int(attr_data["totalPages"]),
                page=int(attr_data["page"]),
                per_page=int(attr_data["perPage"]),
                total_scrobbles=int(attr_data["total"]),
            )

            return UserRecentTrack(
                artist=artist,
                musicbrainz_id=data.get("mbid"),
                name=data["name"],
                url=data["url"],
                images=[Image(ImageData) for ImageData in data["image"]],
                album=album,
                now_playing=now_playing,
                loved=True if data.get("loved") == "1" else False,
                attr=attr,
            )

        return [format_data(data) for data in results["recenttracks"]["track"]]
