from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN
from .media_player import async_setup_entry as setup_media_player
from .udp_communication import UDPCommunication

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Control4 Amp from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    udp_comm = UDPCommunication(entry.data['ip_address'], entry.data['port'])
    await udp_comm.start()

    hass.data[DOMAIN][entry.entry_id] = {
        "udp_comm": udp_comm
    }

    await setup_media_player(hass, entry)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, 'media_player')
    udp_comm = hass.data[DOMAIN][entry.entry_id]['udp_comm']
    await udp_comm.stop()
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
