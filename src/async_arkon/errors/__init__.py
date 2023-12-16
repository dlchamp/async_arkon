"""RCON exceptions."""
from __future__ import annotations

__all__ = ["InvalidPacketStructure", "RequestIdMismatch", "InvalidCredentials"]


class InvalidPacketStructure(Exception):
    """Indicate an invalid packet structure."""


class RequestIdMismatch(Exception):
    """Indicates that the sent and received request IDs do not match."""

    def __init__(self: RequestIdMismatch, sent: int, received: int) -> None:
        """Set the sent and received request IDs."""
        msg = (
            f"Sent packet ID [{sent}] does not match received packet ID [{received}]. "
            "Are you sure you are logged in to the server?"
        )
        super().__init__(msg)
        self.sent = sent
        self.received = received


class InvalidCredentials(Exception):
    """Indicate invalid RCON password."""


class NotConnectedError(Exception):
    """Indicate client is not connected."""


class NotLoggedIn(Exception):
    """Indicate the client has not logged in to the RCON server."""


class ConnectionTimedOut(Exception):
    """Indicate the connection to the RCON host timed out."""
