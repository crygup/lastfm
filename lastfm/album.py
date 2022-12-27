from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from .artist import MiniArtist
    from .image import Image
    from .tags import AlbumTag
    from .wiki import AlbumWiki


@dataclass(frozen=True)
class Album:
    artist: str
    musicbrainz_id: Optional[str]
    tags: Optional[List[AlbumTag]]
    playcount: int
    images: Image
    url: str
    name: str
    userplaycount: Optional[int]
    listeners: int
    wiki: Optional[AlbumWiki]


@dataclass(frozen=True)
class ArtistTopAlbum:
    name: str
    playcount: int
    url: str
    artist: MiniArtist
    images: Image


@dataclass(frozen=True)
class UserRecentTrackAlbum:
    musicbrainz_id: Optional[str]
    name: str
