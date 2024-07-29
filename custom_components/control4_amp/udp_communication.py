import asyncio
import logging

_LOGGER = logging.getLogger(__name__)

class Control4UDP:
    """Class to handle UDP communication with Control4 C4-8AMP1-B."""

    def __init__(self, ip_address: str) -> None:
        """Initialize the UDP communication."""
        self.ip_address = ip_address
        self.port = 8750
        self._udp_client = None
        self._loop = asyncio.get_event_loop()
        self._buffer = bytearray()
        self._connect()

    def _connect(self) -> None:
        """Create a UDP client and connect to the amplifier."""
        self._udp_client = asyncio.DatagramProtocol()
        self._loop.create_datagram_endpoint(
            lambda: self._udp_client,
            remote_addr=(self.ip_address, self.port)
        )

    async def send_command(self, command: bytes) -> None:
        """Send a command to the amplifier."""
        if self._udp_client:
            self._loop.create_datagram_endpoint(
                lambda: self._udp_client,
                remote_addr=(self.ip_address, self.port)
            )
            self._udp_client.sendto(command)
            _LOGGER.debug("Sent command: %s", command)

    def close(self) -> None:
        """Close the UDP connection."""
        if self._udp_client:
            self._udp_client.close()
