from typing import Any, Dict, Optional

__all__ = ["Image"]


class Image:
    def __init__(self, data: Dict[Any, Any]) -> None:
        self._data = data

    def small(self) -> Optional[str]:
        try:
            return self._data[0]["#text"]
        except (KeyError, IndexError):
            return None

    def medium(self) -> Optional[str]:
        try:
            return self._data[1]["#text"]
        except (KeyError, IndexError):
            return None

    def large(self) -> Optional[str]:
        try:
            return self._data[2]["#text"]
        except (KeyError, IndexError):
            return None

    def extralarge(self) -> Optional[str]:
        try:
            return self._data[3]["#text"]
        except (KeyError, IndexError):
            return None
