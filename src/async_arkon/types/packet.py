from __future__ import annotations

import random
from enum import Enum
from typing import NamedTuple

from async_arkon import errors

__all__ = ("Packet",)

TAIL = b"\0\0"


def _rand_uint32() -> int:
    """Create a random integer and return it."""
    return random.randint(0, 4_294_967_295 + 1)


class PacketType(int, Enum):
    """Represents a packet type."""

    LOGIN = 3
    COMMAND = 2
    RESPONSE = 0

    def __bytes__(self) -> bytes:
        """Return integer value as bytes."""
        return self.value.to_bytes(4, "little")


class Packet(NamedTuple):
    """An RCON packet."""

    request_id: int
    type: PacketType
    payload: str

    def __bytes__(self) -> bytes:
        """Return the packet as bytes."""
        payload = self.request_id.to_bytes(4, "little")
        payload += bytes(self.type)
        payload += self.payload.encode()
        payload += TAIL
        size = len(payload).to_bytes(4, "little")
        return size + payload

    @classmethod
    def from_bytes(cls, bytes_: bytes) -> Packet:
        """Create a packet from the respective bytes."""
        request_id = int.from_bytes(bytes_[:4], "little")
        type_ = int.from_bytes(bytes_[4:8], "little")
        payload = bytes_[8:-2]
        tail = bytes_[-2:]

        if tail != TAIL:
            raise errors.InvalidPacketStructure

        return cls(request_id, PacketType(type_), payload.decode())

    @classmethod
    def from_command(cls, command: str) -> Packet:
        """Create a command packet."""
        return cls(_rand_uint32(), PacketType.COMMAND, command)

    @classmethod
    def from_login(cls, passwd: str) -> Packet:
        """Create a login packet."""
        return cls(_rand_uint32(), PacketType.LOGIN, passwd)
