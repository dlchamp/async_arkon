import re
from typing import NamedTuple, Self

from async_arkon import errors

__all__ = ("Player",)


class Player(NamedTuple):
    """Online player information."""

    id: int
    name: str

    @classmethod
    def from_response(cls, line: str) -> Self:
        """Create player information from a line in the server response."""
        match = re.match(r"(\d+)\.\s+(.+?),\s+(\d+)", line)

        if not match:
            msg = "Unable to parse online players from response."
            raise errors.InvalidPacketStructure(msg)

        id = int(match.group(1))
        name = match.group(2)
        return cls(id, name)
