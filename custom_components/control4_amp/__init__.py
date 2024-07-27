import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers import aiohttp_client
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType
from .udp_communication import UDPClient
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Control4 AMP component."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Control4 AMP from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    session = aiohttp_client.async_get_clientsession(hass)
    udp_client = UDPClient(entry.data["host"], entry.data["port"])
    hass.data[DOMAIN][entry.entry_id] = udp_client

    for component in ["media_player"]:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    udp_client = hass.data[DOMAIN].pop(entry.entry_id)
    await udp_client.close()
    
    for component in ["media_player"]:
        await hass.config_entries.async_forward_entry_unload(entry, component)

    return True
