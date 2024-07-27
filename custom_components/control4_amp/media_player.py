import logging
from homeassistant.components.media_player import MediaPlayerEntity, MediaPlayerEntityFeature
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def setup_platform(hass, entry, udp_comm, async_add_entities):
    """Set up the media player platform."""
    device = Control4AmpMediaPlayer(
        name=entry.data['name'],
        unique_id=f"{entry.entry_id}_amp",
        udp_comm=udp_comm
    )
    async_add_entities([device])

    device.udp_comm.request_firmware_version(device.update_firmware_version)

class Control4AmpMediaPlayer(MediaPlayerEntity):
    """MediaPlayer implementation for Control4 Amp."""

    def __init__(self, name, unique_id, udp_comm):
        """Initialize the Control4 Amp media player."""
        self._name = name
        self._unique_id = unique_id
        self.udp_comm = udp_comm
        self._state = None
        self._attributes = {}

    def update_firmware_version(self, version):
        """Update firmware version attribute."""
        self._attributes['firmware_version'] = version
        self.async_write_ha_state()

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def supported_features(self):
        return MediaPlayerEntityFeature.PLAY | MediaPlayerEntityFeature.PAUSE

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""
        return self._attributes
