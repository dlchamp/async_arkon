from types import TracebackType
from typing import Literal, Optional, Self, Union, overload

from . import errors
from .types.abc import Packet, RCONClient
from .types.mixins import AdminMixin, ChatMixin, InfoMixin

__all__ = ("Client",)


class Client(RCONClient, AdminMixin, InfoMixin, ChatMixin):
    """
    A high-level RCON client that provides extended functionalities.

    Integrates base RCON functionalities from RCONClient and features from AdminMixin,
    ChatMixin, and InfoMixin. It facilitates interaction with an RCON server, offering tools
    for server administration, chat management, and server information retrieval.

    Parameters
    ----------
    host : str
        The host address of the RCON server.
    port : int
        The port number of the RCON server.
    password : str
        The password for RCON authentication.
    timeout : Optional[float], optional
        The timeout duration for connections in seconds.

    Inherits
    --------
    RCONClient
        Basic RCON client functionality, including connection management.
    AdminMixin
        Admin-specific functionalities such as server saving and broadcasting.
    ChatMixin
        Chat functionalities, including sending server chats.
    InfoMixin
        Server information functionalities, such as retrieving player lists.

    Supports asynchronous operations for use in async contexts.
    """

    def __init__(
        self, host: str, port: int, password: str, *, timeout: Optional[float] = None
    ) -> None:
        super().__init__(host, port, timeout=timeout)

        self.password = password
        self.logged_in: bool = False

    async def __aenter__(self) -> Self:
        """Connect to the RCON server and login."""
        await super().__aenter__()
        await self.login()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Log out and disconnect from RCON server."""
        await super().__aexit__(exc_type, exc_value, traceback)
        self.logged_in = False

    @overload
    async def run(self, command: str, *arguments: str, raw: Literal[False]) -> str:
        ...

    @overload
    async def run(self, command: str, *arguments: str, raw: Literal[True]) -> Packet:
        ...

    async def run(self, command: str, *arguments: str, raw: bool = False) -> Union[Packet, str]:
        """Build and execute and send an RCON command to the server.

        Parameters
        ----------
        command: str
            The command being sent to the RCON server.
        *arguments: str
            Extra arguments for the command.
        raw: bool, False
            Whether the response should be a raw Packet or the payload str.

        Returns
        -------
        Union[Packet, str]
            The raw response Packet or the str value of Packet.payload.
        """
        command = " ".join((command, *arguments))
        packet = Packet.from_command(command)
        response = await self.communicate(packet)
        return response if raw else response.payload

    async def login(self) -> None:
        """Execute the login command to the RCON server.

        Raises
        ------
        errors.InvalidCredentials
            The provided password was refused by the server.
        """
        if self.logged_in:
            return

        if not self._writer:
            await self.connect()

        self.logged_in = True

        packet = Packet.from_login(self.password)

        try:
            await self.communicate(packet)
        except errors.RequestIdMismatch:
            raise errors.InvalidCredentials from None

        return
