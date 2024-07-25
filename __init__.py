from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
import logging
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    _LOGGER.debug("Setting up entry: %s", entry.data)
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    try:
        # Forward setup to the media player platform
        await hass.config_entries.async_forward_entry_setups(entry, ["media_player"])
        _LOGGER.debug("Forwarded entry setup to media_player")
    except Exception as e:
        _LOGGER.error("Error setting up entry: %s", e)
        return False

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    _LOGGER.debug("Unloading entry: %s", entry.data)
    try:
        await hass.config_entries.async_forward_entry_unload(entry, "media_player")
        _LOGGER.debug("Unloaded entry from media_player")
        hass.data[DOMAIN].pop(entry.entry_id)
    except Exception as e:
        _LOGGER.error("Error unloading entry: %s", e)
        return False

    return True
