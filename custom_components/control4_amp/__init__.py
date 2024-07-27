import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import HomeAssistantType

from .const import DOMAIN
from .udp_communication import UDPCommunication

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config):
    """Set up configured Control4 Amp."""
    return True

async def async_setup_entry(hass: HomeAssistantType, entry: ConfigEntry):
    """Set up Control4 Amp from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    udp_comm = UDPCommunication(entry.data["ip_address"], entry.data["port"])
    await udp_comm.start()
    hass.data[DOMAIN][entry.entry_id] = udp_comm

    # Load platforms
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setups(entry, ["media_player"])
    )
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["media_player"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
