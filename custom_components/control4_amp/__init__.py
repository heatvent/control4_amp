# TEST CHANGE
import asyncio
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN
from .udp_communication import Control4AMP

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Control4 AMP from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    amplifier = Control4AMP(entry.data["ip_address"], entry.data["port"])
    hass.data[DOMAIN][entry.entry_id] = amplifier

    # Start the UDP communication
    asyncio.create_task(amplifier.run())

    # Forward the setup to the media player platform
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "media_player")
    )
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    amplifier = hass.data[DOMAIN].pop(entry.entry_id)
    await amplifier.stop()

    return await hass.config_entries.async_forward_entry_unload(entry, "media_player")
