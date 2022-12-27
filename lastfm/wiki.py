import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class AlbumWiki:
    published: Optional[datetime.datetime]
    summary: Optional[str]
    content: Optional[str]
