from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .image import Image

__all__ = ["Artist", "MiniArtist", "SimilarArtist", "SearchArtist"]


@dataclass(frozen=True)
class Artist:
    """Artist's details"""

    name: str
    musicbrainz_id: Optional[str]
    url: str
    images: List[Image]
    streamable: str
    ontour: str
    listeners: int
    playcount: int
    userplaycount: Optional[int]
    similar: List[MiniArtist]


@dataclass(frozen=True)
class MiniArtist:
    """Artist from 'similar' attribute in Arist"""

    url: str
    name: str
    name: str
    images: List[Image]


@dataclass(frozen=True)
class SimilarArtist:
    """Artist from client.fetch_similar_artists"""

    name: str
    musicbrainz_id: Optional[str]
    match: str
    url: str
    images: List[Image]
    streamable: str


@dataclass(frozen=True)
class SearchArtist:
    """Artist from client.search_artists"""

    name: str
    listeners: int
    musicbrainz_id: Optional[str]
    url: str
    streamable: str
    images: List[Image]


@dataclass(frozen=True)
class TrackArtist:
    name: str
    musicbrainz_id: Optional[str]
    url: str
