from homeassistant.components.media_player import MediaPlayerEntity
from homeassistant.components.media_player.const import (
    SUPPORT_TURN_ON, SUPPORT_TURN_OFF, SUPPORT_VOLUME_SET, SUPPORT_VOLUME_MUTE,
    MEDIA_TYPE_MUSIC, MEDIA_TYPE_CHANNEL)
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the Control4 AMP media player platform."""
    udp_client = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([Control4AMPMediaPlayer(udp_client)])

class Control4AMPMediaPlayer(MediaPlayerEntity):
    def __init__(self, udp_client):
        self._udp_client = udp_client
        self._name = "Control4 AMP"
        self._state = None

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        await self._udp_client.connect()

    async def async_will_remove_from_hass(self):
        """When entity is removed from hass."""
        await self._udp_client.close()

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    async def async_turn_on(self):
        await self._udp_client.send_command("0gha01 c4.sy.fwv\r\n")
        self._state = "on"
        self.async_write_ha_state()

    async def async_turn_off(self):
        await self._udp_client.send_command("0gha01 c4.sy.off\r\n")
        self._state = "off"
        self.async_write_ha_state()
