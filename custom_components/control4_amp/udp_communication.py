import asyncio
import logging

_LOGGER = logging.getLogger(__name__)

class UDPClient:
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._transport = None
        self._protocol = None
        self._loop = asyncio.get_event_loop()

    async def connect(self):
        self._transport, self._protocol = await self._loop.create_datagram_endpoint(
            lambda: UDPProtocol(self._loop),
            remote_addr=(self._host, self._port)
        )
        _LOGGER.debug("Connection made to %s:%s", self._host, self._port)

    async def send_command(self, command):
        if self._transport:
            self._transport.sendto(command.encode())
            _LOGGER.debug("Sending command: %s", command)

    async def close(self):
        if self._transport:
            self._transport.close()
            _LOGGER.debug("Connection closed")

class UDPProtocol:
    def __init__(self, loop):
        self.loop = loop

    def connection_made(self, transport):
        _LOGGER.debug("Connection made")
        self.transport = transport

    def datagram_received(self, data, addr):
        _LOGGER.debug("Received response: %s", data.decode())
        # Add your response handling logic here

    def error_received(self, exc):
        _LOGGER.error('Error received:', exc)

    def connection_lost(self, exc):
        _LOGGER.debug("Connection lost")
