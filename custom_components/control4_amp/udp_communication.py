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
        self.sequence = 0

    def connection_made(self, transport):
        self.transport = transport
        _LOGGER.info('Connection made to %s:%s', self.ip, self.port)

    def datagram_received(self, data, addr):
        message = data.decode()
        _LOGGER.info('Received message: %s from %s', message, addr)
        # Process response here
        if "c4.sy.fwv" in message:
            version = message.split('"')[1]
            _LOGGER.info('Firmware version received: %s', version)
            # Update Home Assistant state here

    def error_received(self, exc):
        _LOGGER.error('Error received: %s', exc)

    def connection_lost(self, exc):
        _LOGGER.warning('Connection lost: %s', exc)
        self.transport = None

    async def start(self):
        self.transport, _ = await self.loop.create_datagram_endpoint(
            lambda: self,
            remote_addr=(self.ip, self.port)
        )

    async def stop(self):
        if self.transport:
            self.transport.close()
            _LOGGER.info('UDP connection closed')

    def send_data(self, command):
        data = f'0g{self.sequence:02d}ha00 {command}\r\n'
        if self.transport:
            self.transport.sendto(data.encode(), (self.ip, self.port))
            _LOGGER.info('Sent command: %s to %s:%s', data, self.ip, self.port)
        self.sequence = (self.sequence + 1) % 100  # wrap around at 99

    def request_firmware_version(self):
        self.send_data("c4.sy.fwv")
