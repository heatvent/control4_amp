import asyncio
import logging

_LOGGER = logging.getLogger(__name__)

class UDPCommunication:
    """Manage UDP communication."""

    def __init__(self, ip, port):
        self._ip = ip
        self._port = port
        self.loop = asyncio.get_event_loop()
        self.transport = None

    async def start(self):
        """Start the UDP server."""
        self.transport, _ = await self.loop.create_datagram_endpoint(
            lambda: self,
            remote_addr=(self._ip, self._port)
        )
        _LOGGER.info("UDP server started on %s:%s", self._ip, self._port)

    def send_data(self, data):
        """Send data to the UDP server."""
        self.transport.sendto(data.encode(), (self._ip, self._port))
        _LOGGER.info("Sent data: %s", data)

    def connection_made(self, transport):
        """Called when connection is made."""
        self.transport = transport
        _LOGGER.info("Connection made to %s:%s", self._ip, self._port)

    def datagram_received(self, data, addr):
        """Handle received data."""
        message = data.decode()
        _LOGGER.info("Received message: %s from %s", message, addr)

    def connection_lost(self, exc):
        """Handle connection lost."""
        _LOGGER.warning("Connection lost: %s", exc)
        self.transport = None
