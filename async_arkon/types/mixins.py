from typing import List, Optional

from .abc import MixinProtocol

# from .message import Message
from .player import Player

__all__ = (
    "AdminMixin",
    "ChatMixin",
    "InfoMixin",
)


class AdminMixin:
    """Mixin that provides admin related functions."""

    async def saveworld(self: MixinProtocol) -> None:
        """Trigger a world save command."""
        await self.run("saveworld", raw=False)

    async def broadcast(self: MixinProtocol, msg: str) -> None:
        """Broadcast a message to the server."""
        await self.run("broadcast", msg, raw=False)


class ChatMixin:
    """Mixin that provides chat related functions."""

    async def chat(self: MixinProtocol, username: Optional[str] = None, *, msg: str) -> None:
        """Send a message to the server, prefix an optional username."""
        if username:
            msg = f"{username}: {msg}"

        await self.run("serverchat", msg, raw=True)

    # async def fetch_chat_buffer(self: MixinProtocol, limit: int = 50) -> None:
    #     """Fetch up to 50 messages from the RCON server's buffer."""
    #     response = await self.run("getchat")
    #     print(response)


class InfoMixin:
    """Mixin that adds server information functions."""

    async def fetch_online_players(self: MixinProtocol) -> List[Player]:
        response = await self.run("listplayers", raw=False)

        if response.strip() == "No Players Connected":
            return []

        return [Player.from_response(line) for line in response.split("\n") if line.strip()]
