import logging
from homeassistant.components.media_player import MediaPlayerEntity
from homeassistant.components.media_player.const import (
    SUPPORT_TURN_ON,
    SUPPORT_TURN_OFF,
    SUPPORT_VOLUME_SET,
)
from homeassistant.const import STATE_OFF, STATE_ON

_LOGGER = logging.getLogger(__name__)

SUPPORT_CONTROL4_AMP = SUPPORT_TURN_ON | SUPPORT_TURN_OFF | SUPPORT_VOLUME_SET

async def async_setup_entry(hass, config_entry, async_add_entities):
    async_add_entities([Control4Amp(config_entry.data)])

class Control4Amp(MediaPlayerEntity):
    def __init__(self, config):
        self._host = config["host"]
        self._port = config["port"]
        self._state = STATE_OFF
        self._volume = 0

    @property
    def name(self):
        return "Control4 Amplifier"

    @property
    def state(self):
        return self._state

    @property
    def supported_features(self):
        return SUPPORT_CONTROL4_AMP

    async def async_turn_on(self):
        self._state = STATE_ON
        # Add code to send turn on command to the amplifier
        self.async_write_ha_state()

    async def async_turn_off(self):
        self._state = STATE_OFF
        # Add code to send turn off command to the amplifier
        self.async_write_ha_state()

    async def async_set_volume_level(self, volume):
        self._volume = volume
        # Add code to set volume on the amplifier
        self.async_write_ha_state()
