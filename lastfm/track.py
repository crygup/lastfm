from __future__ import annotations
from dataclasses import dataclass
from typing import List, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .artist import MiniArtist
    from .image import Image
    from .artist import UserRecentTrackArtist
    from .album import UserRecentTrackAlbum
    from .attr import UserRecentTrackAttr


@dataclass(frozen=True)
class ArtistTopTrack:
    name: str
    playcount: int
    listeners: int
    url: str
    streamable: str
    artist: MiniArtist
    images: List[Image]


@dataclass(frozen=True)
class UserRecentTrack:
    artist: UserRecentTrackArtist
    musicbrainz_id: Optional[str]
    name: str
    url: str
    images: List[Image]
    album: UserRecentTrackAlbum
    now_playing: Optional[bool]
    loved: Optional[bool]
    attr: UserRecentTrackAttr
