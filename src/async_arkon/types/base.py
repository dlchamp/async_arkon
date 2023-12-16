from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Optional, Self, Type

from async_arkon import errors

from .packet import Packet

if TYPE_CHECKING:
    import types

__all__ = ("RCONClient",)


class RCONClient:
    """
    A basic client for handling RCON connections.

    Parameters
    ----------
    host : str
        The host address of the RCON server.
    port : int
        The port number of the RCON server.
    timeout : Optional[float], optional
        The timeout duration for connections in seconds.

    Attributes
    ----------
    _reader : Optional[asyncio.StreamReader]
        StreamReader object for reading data from the server.
    _writer : Optional[asyncio.StreamWriter]
        StreamWriter object for sending data to the server.
    """

    def __init__(self, host: str, port: int, timeout: Optional[float] = None) -> None:
        self.host = host
        self.port = port
        self.timeout = timeout

        self._reader: Optional[asyncio.StreamReader] = None
        self._writer: Optional[asyncio.StreamWriter] = None

        self.logged_in: bool = False

    async def __aenter__(self) -> Self:
        """Connect to the server via context manager."""
        await self.connect()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[types.TracebackType],
    ) -> None:
        """Close the connection when the context manager has finished."""
        await self.close()

    async def reconnect(self) -> None:
        """Reconnect to the server."""
        await self.close()
        await self.connect()

    async def connect(self) -> None:
        """Connect to the server."""
        connect_coro = asyncio.open_connection(host=self.host, port=self.port)
        if self.timeout:
            connect_coro = asyncio.wait_for(connect_coro, timeout=self.timeout)

        try:
            self._reader, self._writer = await connect_coro
        except asyncio.TimeoutError:
            raise errors.ConnectionTimedOut from None

    async def close(self) -> None:
        """Close the server connection."""
        if not self._writer:
            return

        self._writer.close()
        await self._writer.wait_closed()

        self._writer = None
        self._reader = None

    async def communicate(self, packet: Packet) -> Packet:
        """Send and receive an RCON Packet to the server.

        Parameters
        ----------
        packet: Packet
            The packet being sent to the server

        Raises
        ------
        errors.NotConnectedError
            The client is not connected to the RCON server
        errors.NotLoggedIn
            The client is connected, but is not logged in.
        errors.RequestIDMismatch
            The sent and received packets do not have matching IDs.

        Returns
        -------
        Packet
            The packet response from the server.
        """
        if not self._writer or not self._reader:
            msg = "Client not is connected to the host. Please connect before logging in."
            raise errors.NotConnectedError(msg)

        if not self.logged_in:
            msg = "You connected to the RCON server but have not logged in."
            raise errors.NotLoggedIn(msg)

        self._writer.write(bytes(packet))
        await self._writer.drain()
        header = await self._reader.read(4)
        length = int.from_bytes(header, "little")
        payload = await self._reader.read(length)
        response = Packet.from_bytes(payload)

        if response.request_id != packet.request_id:
            raise errors.RequestIdMismatch(packet.request_id, response.request_id)

        return response
