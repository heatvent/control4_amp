import asyncio
import logging

_LOGGER = logging.getLogger(__name__)

class Control4AMP:
    def __init__(self, ip_address, port):
        self._ip_address = ip_address
        self._port = port
        self._transport = None
        self._protocol = None
        self._sequence = 0
        self._command_queue = asyncio.Queue()
        self._response_queue = asyncio.Queue()

    async def run(self):
        loop = asyncio.get_event_loop()
        listen = loop.create_datagram_endpoint(
            lambda: self, local_addr=("0.0.0.0", 0)
        )
        self._transport, self._protocol = await listen

        # Start the command processing loop
        asyncio.create_task(self._process_commands())

    async def stop(self):
        if self._transport:
            self._transport.close()

    async def send_command(self, command):
        self._sequence += 1
        sequence_str = f"{self._sequence:02}"
        full_command = f"0gha{sequence_str} {command}\r\n".encode()
        _LOGGER.debug(f"Sending command: {full_command}")
        self._transport.sendto(full_command, (self._ip_address, self._port))
        response = await self._response_queue.get()
        return response

    async def _process_commands(self):
        while True:
            command = await self._command_queue.get()
            response = await self.send_command(command)
            self._command_queue.task_done()
            await self._response_queue.put(response)

    def datagram_received(self, data, addr):
        _LOGGER.debug(f"Received response: {data}")
        asyncio.create_task(self._response_queue.put(data))

    def error_received(self, exc):
        _LOGGER.error(f"Error received: {exc}")

    def connection_lost(self, exc):
        _LOGGER.warning("Connection lost")
