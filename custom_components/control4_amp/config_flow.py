import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN

@callback
def configured_instances(hass):
    """Return a set of configured Control4 AMP instances."""
    return set(entry.data["host"] for entry in hass.config_entries.async_entries(DOMAIN))

class Control4AMPConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title=user_input["name"], data=user_input)

        data_schema = vol.Schema({
            vol.Required("name"): str,
            vol.Required("host"): str,
            vol.Required("port"): int,
        })

        return self.async_show_form(
            step_id="user", data_schema=data_schema
        )
