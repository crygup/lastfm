from __future__ import annotations
from dataclasses import dataclass
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .artist import TrackArtist
    from .image import Image


@dataclass(frozen=True)
class AritstTrack:
    name: str
    playcount: int
    listeners: int
    url: str
    streamable: str
    artist: TrackArtist
    images: List[Image]
