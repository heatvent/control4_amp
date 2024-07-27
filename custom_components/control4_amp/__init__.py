from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN
from .media_player import async_setup_entry as async_setup_media_player
from .udp_communication import UDPCommunication

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Control4 Amp from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    udp_comm = UDPCommunication(entry.data['ip_address'], entry.data['port'])
    await udp_comm.start()

    # Save the communication instance to be used by other components
    hass.data[DOMAIN][entry.entry_id] = udp_comm

    # Setup media player platform and pass the communication instance
    await async_setup_media_player(hass, entry, lambda entities: hass.add_entities(entities))

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    udp_comm = hass.data[DOMAIN].pop(entry.entry_id)
    await udp_comm.stop()
    return True
