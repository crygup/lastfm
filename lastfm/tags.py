from dataclasses import dataclass


@dataclass(frozen=True)
class AlbumTag:
    url: str
    name: str
