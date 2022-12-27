from dataclasses import dataclass


@dataclass(frozen=True)
class UserRecentTrackAttr:
    user: str
    total_pages: int
    page: int
    per_page: int
    total_scrobbles: int
