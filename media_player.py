import logging
from homeassistant.components.media_player import MediaPlayerEntity
from homeassistant.components.media_player.const import (
    SUPPORT_TURN_ON,
    SUPPORT_TURN_OFF,
    SUPPORT_VOLUME_SET,
)
from homeassistant.const import STATE_OFF, STATE_ON
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    amplifier = hass.data[DOMAIN][entry.entry_id]
    entities = [Control4AMPMediaPlayer(amplifier)]
    async_add_entities(entities)

class Control4AMPMediaPlayer(MediaPlayerEntity):
    def __init__(self, amplifier):
        self._amplifier = amplifier
        self._name = "Control4 Amplifier"
        self._state = STATE_OFF
        self._volume = 0

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def supported_features(self):
        return SUPPORT_TURN_ON | SUPPORT_TURN_OFF | SUPPORT_VOLUME_SET

    @property
    def volume_level(self):
        return self._volume

    async def async_turn_on(self):
        await self._amplifier.send_command("turn_on")
        self._state = STATE_ON
        self.async_write_ha_state()

    async def async_turn_off(self):
        await self._amplifier.send_command("turn_off")
        self._state = STATE_OFF
        self.async_write_ha_state()

    async def async_set_volume_level(self, volume):
        await self._amplifier.send_command(f"set_volume {volume}")
        self._volume = volume
        self.async_write_ha_state()
