from typing import Any, Dict, Optional

from .image import Image

__all__ = ["User"]


class User:
    def __init__(self, data: Dict[Any, Any]) -> None:
        self._data = data["user"]

    @property
    def url(self) -> str:
        return self._data["url"]

    @property
    def type(self) -> str:
        return self._data["type"]

    @property
    def name(self) -> str:
        return self._data["name"]

    @property
    def realname(self) -> Optional[str]:
        return self._data["name"] if self._data["name"] != "" else None

    @property
    def country(self) -> Optional[str]:
        return self._data["country"] if self._data["country"] != "" else None

    @property
    def gender(self) -> str:
        return self._data["gender"]

    @property
    def age(self) -> int:
        return int(self._data["age"])

    @property
    def playcount(self) -> int:
        return int(self._data["playcount"])

    @property
    def artist_count(self) -> int:
        return int(self._data["artist_count"])

    @property
    def playlists(self) -> int:
        return int(self._data["playlists"])

    @property
    def track_count(self) -> int:
        return int(self._data["track_count"])

    @property
    def album_count(self) -> int:
        return int(self._data["album_count"])

    @property
    def subscriber(self) -> bool:
        return bool(int(self._data["subscriber"]))

    @property
    def registered(self) -> int:
        return self._data["registered"]["#text"]

    @property
    def images(self) -> Image:
        return Image(data=self._data["image"])
