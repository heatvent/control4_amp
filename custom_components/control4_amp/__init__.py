"""The Control4 C4-8AMP1-B integration."""

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_platform

from .const import DOMAIN

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Control4 C4-8AMP1-B component."""
    # Initialize the UDP communication
    hass.data[DOMAIN] = {}
    # Set up the configuration flow and options
    hass.config_entries.async_setup_platforms(hass.config_entries.async_entries(DOMAIN), ["media_player"])
    return True

async def async_setup_entry(hass: HomeAssistant, entry: config_entries.ConfigEntry) -> bool:
    """Set up Control4 C4-8AMP1-B from a config entry."""
    # Create the UDP communication instance and store it
    from .udp_communication import Control4UDP

    hass.data[DOMAIN][entry.entry_id] = Control4UDP(entry.data["ip_address"])

    # Set up the media player platform
    await hass.config_entries.async_forward_entry_setup(entry, "media_player")
    return True

async def async_unload_entry(hass: HomeAssistant, entry: config_entries.ConfigEntry) -> bool:
    """Unload a config entry."""
    # Unload the media player platform
    await hass.config_entries.async_forward_entry_unload(entry, "media_player")
    # Clean up
    if entry.entry_id in hass.data[DOMAIN]:
        hass.data[DOMAIN][entry.entry_id].close()
        del hass.data[DOMAIN][entry.entry_id]
    return True
