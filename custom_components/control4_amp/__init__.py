from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import DOMAIN
from .udp_communication import UDPCommunication

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Control4 Amp from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Setup UDP communication
    udp_comm = UDPCommunication(entry.data['ip_address'], entry.data['port'])
    await udp_comm.start()

    # Store in hass.data for access from platform setup
    hass.data[DOMAIN][entry.entry_id] = udp_comm

    # Forward the setup to the media_player platform
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, 'media_player')
    )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    # Unload the media_player platform
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, 'media_player')

    # Stop UDP communication
    udp_comm = hass.data[DOMAIN].pop(entry.entry_id)
    await udp_comm.stop()

    return unload_ok
