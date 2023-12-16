"""Information about log lines."""

import re
from typing import List, NamedTuple, Self

__all__ = ("LogLine",)


REGEX = re.compile(r"(\d{4}\.\d{2}\.\d{2}_\d{2}\.\d{2}\.\d{2}): (.*)\n")


class LogLine(NamedTuple):
    """Log information."""

    time: str
    log: str

    @classmethod
    def from_response(cls, text: str) -> List[Self]:
        """Create log lines from a server response."""
        if text == "Server received, But no response!! \n ":
            return []

        return [cls(match.group(1), match.group(2)) for match in REGEX.finditer(text) if match]
