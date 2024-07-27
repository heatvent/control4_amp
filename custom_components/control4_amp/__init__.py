from homeassistant.core import HomeAssistant

DOMAIN = "control4_amp"

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Control4 Amplifier component."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry):
    """Set up Control4 Amplifier from a config entry."""
    hass.async_add_job(hass.config_entries.async_forward_entry_setup(entry, "media_player"))
    return True

async def async_unload_entry(hass: HomeAssistant, entry):
    """Unload a config entry."""
    await hass.config_entries.async_forward_entry_unload(entry, "media_player")
    return True
