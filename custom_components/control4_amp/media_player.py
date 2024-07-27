import logging
from homeassistant.components.media_player import MediaPlayerEntity, MediaPlayerEntityFeature
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Setup media player platform."""
    udp_comm = hass.data[DOMAIN][entry.entry_id]
    name = entry.data["name"]
    entities = [Control4AmpMediaPlayer(name, f"{entry.entry_id}_amp", udp_comm)]
    for i in range(1, 5):
        entities.append(Control4AmpMediaPlayer(f"{name} Zone {i}", f"{entry.entry_id}_zone{i}", udp_comm))
    async_add_entities(entities)

class Control4AmpMediaPlayer(MediaPlayerEntity):
    """Representation of a Control4 Amp media player."""

    def __init__(self, name, unique_id, udp_comm):
        """Initialize the media player."""
        self._name = name
        self._unique_id = unique_id
        self._state = None
        self._udp_comm = udp_comm

    @property
    def unique_id(self):
        """Return the unique ID."""
        return self._unique_id

    @property
    def name(self):
        """Return the name."""
        return self._name

    @property
    def state(self):
        """Return the state."""
        return self._state

    @property
    def supported_features(self):
        """Return the supported features."""
        return MediaPlayerEntityFeature.PLAY | MediaPlayerEntityFeature.PAUSE
