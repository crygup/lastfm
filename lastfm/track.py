from __future__ import annotations
from dataclasses import dataclass
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .artist import MiniArtist
    from .image import Image


@dataclass(frozen=True)
class ArtistTopTrack:
    name: str
    playcount: int
    listeners: int
    url: str
    streamable: str
    artist: MiniArtist
    images: List[Image]
