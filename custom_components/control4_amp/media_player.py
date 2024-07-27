import logging
from homeassistant.components.media_player import MediaPlayerEntity, MediaPlayerEntityFeature
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Control4 Amp MediaPlayer from a config entry."""
    udp_comm = hass.data[DOMAIN][config_entry.entry_id]
    name = config_entry.data["name"]
    device = Control4AmpMediaPlayer(
        name=name,
        unique_id=f"{config_entry.entry_id}_amp",
        udp_comm=udp_comm
    )
    async_add_entities([device], True)  # Update upon initialization

    # Request firmware version after entity is added
    device.update_firmware_version()

class Control4AmpMediaPlayer(MediaPlayerEntity):
    """MediaPlayer implementation for Control4 Amp."""

    def __init__(self, name, unique_id, udp_comm):
        """Initialize the Control4 Amp media player."""
        super().__init__()
        self._name = name
        self._unique_id = unique_id
        self.udp_comm = udp_comm
        self._state = None
        self._attributes = {}

    @property
    def name(self):
        """Return the name of the media player."""
        return self._name

    @property
    def unique_id(self):
        """Return the unique ID of the media player."""
        return self._unique_id

    @property
    def supported_features(self):
        """Return the supported features."""
        return MediaPlayerEntityFeature.PLAY | MediaPlayerEntityFeature.PAUSE

    @property
    def extra_state_attributes(self):
        """Return extra state attributes."""
        return self._attributes

    def update_firmware_version(self):
        """Request and update firmware version."""
        self.udp_comm.request_firmware_version(self.handle_firmware_response)

    def handle_firmware_response(self, version):
        """Handle the response from firmware version request."""
        self._attributes['firmware_version'] = version
        self.async_write_ha_state()
