import asyncio
import logging

_LOGGER = logging.getLogger(__name__)

class UDPCommunication:
    """Class to handle UDP communication with Control4 Amp."""

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.transport = None
        self.loop = asyncio.get_event_loop()
        self.firmware_callback = None  # Add default value for callback

    def connection_made(self, transport):
        """Called when the connection is made."""
        self.transport = transport
        _LOGGER.info('Connection made to %s:%s', self.ip, self.port)

    def datagram_received(self, data, addr):
        """Handle received data."""
        message = data.decode()
        _LOGGER.info('Received message: %s from %s', message, addr)
        # Ensure the message contains the expected structure before processing
        if '"' in message:
            version = message.split('"')[1]
            _LOGGER.info('Firmware version received: %s', version)
            if self.firmware_callback:
                self.firmware_callback(version)
        else:
            _LOGGER.warning('Received unexpected message format: %s', message)

    def error_received(self, exc):
        """Handle received error."""
        _LOGGER.error('Error received: %s', exc)

    def connection_lost(self, exc):
        """Handle connection lost."""
        _LOGGER.warning('Connection lost: %s', exc)
        self.transport = None

    async def start(self):
        """Start UDP server."""
        self.transport, _ = await self.loop.create_datagram_endpoint(
            lambda: self,
            remote_addr=(self.ip, self.port)
        )
        _LOGGER.info('UDP server started on %s:%s', self.ip, self.port)

    async def stop(self):
        """Stop UDP server."""
        if self.transport:
            self.transport.close()
            _LOGGER.info('UDP connection closed')

    def send_data(self, data):
        """Send data via UDP."""
        if self.transport:
            self.transport.sendto(data.encode(), (self.ip, self.port))
            _LOGGER.info('Sent data to %s:%s', self.ip, self.port)

    def request_firmware_version(self):
        """Request firmware version from the amp."""
        command = "0gha00 c4.sy.fwv\r\n"
        self.send_data(command)
