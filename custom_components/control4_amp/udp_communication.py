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
        self.firmware_callback = None  # Ensure there's a default callback

    def connection_made(self, transport):
        """Called when the connection is made."""
        self.transport = transport
        _LOGGER.info('Connection made to %s:%s', self.ip, self.port)

def datagram_received(self, data, addr):
    """Handle received data."""
    message = data.decode()
    try:
        if 'c4.sy.fwv' in message and '"' in message:
            version = message.split('"')[1]
            _LOGGER.info('Firmware version received: %s', version)
            # Here you should define how you update the entity or state
        else:
            _LOGGER.warning('Received unexpected message format: %s', message)
    except IndexError:
        _LOGGER.error('Error processing message: %s', message)

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
            formatted_data = f"{data}\r\n".encode('utf-8')
            self.transport.sendto(formatted_data, (self.ip, self.port))
            _LOGGER.info('Sent data: %s to %s:%s', data, self.ip, self.port)

    def request_firmware_version(self):
        """Request firmware version from the amp."""
        command = "0gha00 c4.sy.fwv"
        self.send_data(command)


    # Add a method to handle the response and call the callback
    def handle_response(self, data):
        """Handle the response from the device."""
        if '"' in data:
            version = data.split('"')[1]
            _LOGGER.info('Firmware version received: %s', version)
            if self.firmware_callback:
                self.firmware_callback(version)
        else:
            _LOGGER.warning('Received unexpected message format: %s', data)
