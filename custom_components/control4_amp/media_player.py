import logging
from homeassistant.components.media_player import MediaPlayerEntity, MediaPlayerEntityFeature
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Control4 Amp MediaPlayer from a config entry."""
    udp_comm = hass.data[DOMAIN][config_entry.entry_id]['udp_comm']
    devices = [Control4AmpMediaPlayer(name=config_entry.data['name'], unique_id=f"{config_entry.entry_id}_amp", udp_comm=udp_comm)]
    async_add_entities(devices)

class Control4AmpMediaPlayer(MediaPlayerEntity):
    """MediaPlayer implementation for Control4 Amp."""

    def __init__(self, name, unique_id, udp_comm):
        """Initialize the Control4 Amp media player."""
        super().__init__()
        self._name = name
        self._unique_id = unique_id
        self.udp_comm = udp_comm
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def supported_features(self):
        return MediaPlayerEntityFeature.PLAY | MediaPlayerEntityFeature.PAUSE

    async def async_added_to_hass(self):
        """When entity is added to HA, request the firmware version."""
        self.udp_comm.request_firmware_version(callback=self.update_firmware_version)

    def update_firmware_version(self, version):
        """Handle the response for firmware version."""
        self._state = version
        self.async_write_ha_state()
