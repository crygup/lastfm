from typing import Any, Dict, Optional

__all__ = ["Tag"]


class Tag:
    def __init__(self, data: Dict[Any, Any]) -> None:
        self._data = data

    @property
    def name(self) -> str:
        return self._data["name"]

    @property
    def url(self) -> str:
        return self._data["url"]

    @property
    def count(self) -> Optional[int]:
        """This is only present with User.get_tags()"""
        try:
            return int(self._data["count"])
        except KeyError:
            return None
