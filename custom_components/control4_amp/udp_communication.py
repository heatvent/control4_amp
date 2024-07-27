import asyncio
import logging

_LOGGER = logging.getLogger(__name__)

class UDPCommunication:
    """UDP Communication handler for Control4 Amp."""

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.loop = asyncio.get_event_loop()
        self.transport = None

    async def start(self):
        """Start the UDP server."""
        self.transport, _ = await self.loop.create_datagram_endpoint(
            lambda: self,
            remote_addr=(self.ip, self.port)
        )
        _LOGGER.info("UDP server started on %s:%s", self.ip, self.port)

    def send_data(self, data):
        """Send data to the UDP endpoint."""
        self.transport.sendto(data.encode(), (self.ip, self.port))
        _LOGGER.info("Sent data: %s", data)

    def request_firmware_version(self, callback):
        """Request firmware version from the amp."""
        self.send_data("0gha00 c4.sy.fwv")
        self.firmware_callback = callback

    def datagram_received(self, data, addr):
        """Handle received datagrams."""
        message = data.decode()
        _LOGGER.info("Received message: %s", message)
        if 'c4.sy.fwv' in message:
            version = message.split('"')[1]
            if self.firmware_callback:
                self.firmware_callback(version)

    async def stop(self):
        """Stop the UDP server."""
        if self.transport:
            self.transport.close()
            _LOGGER.info("UDP server stopped.")
