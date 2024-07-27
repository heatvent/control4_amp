import asyncio
import logging
from homeassistant.helpers.dispatcher import async_dispatcher_send
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class UDPCommunication:
    """Class to handle UDP communication with Control4 Amp."""

    def __init__(self, hass, ip, port):
        self.hass = hass
        self.ip = ip
        self.port = port
        self.transport = None
        self.loop = asyncio.get_running_loop()
        self.sequence = 0

    def connection_made(self, transport):
        """Handle connection made event."""
        self.transport = transport
        _LOGGER.info("Connection made with %s:%s", self.ip, self.port)

    def datagram_received(self, data, addr):
        """Handle incoming UDP data."""
        message = data.decode()
        _LOGGER.info("Received from %s: %s", addr, message)
        self.handle_response(message)

    def error_received(self, exc):
        """Handle errors."""
        _LOGGER.error("UDP error received: %s", exc)

    def connection_lost(self, exc):
        """Handle connection lost."""
        _LOGGER.warning("UDP connection lost: %s", exc)
        self.transport = None

    async def start(self):
        """Start UDP server."""
        self.transport, _ = await self.loop.create_datagram_endpoint(
            lambda: self,
            remote_addr=(self.ip, self.port)
        )

    async def stop(self):
        """Stop UDP server."""
        if self.transport:
            self.transport.close()
            _LOGGER.info("UDP connection closed")

    def send_data(self, command):
        """Send data to Control4 Amp."""
        # Adjusted sequence initialization and formatting
        self.sequence = (self.sequence % 99) + 1  # Wrap around at 99 and start at 01
        data = f'0gha{self.sequence:02d} {command}\r\n'
        if self.transport:
            self.transport.sendto(data.encode(), (self.ip, self.port))
            _LOGGER.info("Sent command: %s to %s:%s", data, self.ip, self.port)

    def handle_response(self, message):
        """Handle responses from the amplifier."""
        if "c4.sy.fwv" in message:
            version = message.split('"')[1]
            _LOGGER.info("Firmware version: %s", version)
            async_dispatcher_send(self.hass, f"{DOMAIN}_update_firmware", version)

    def request_firmware_version(self):
        """Send command to request firmware version."""
        self.send_data("c4.sy.fwv")
