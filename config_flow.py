import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN

@callback
def configured_instances(hass):
    return set(
        entry.data["ip_address"] for entry in hass.config_entries.async_entries(DOMAIN)
    )

class Control4AMPConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            if user_input["ip_address"] in configured_instances(self.hass):
                errors["base"] = "ip_exists"
            else:
                return self.async_create_entry(title="Control4 AMP", data=user_input)

        data_schema = vol.Schema(
            {
                vol.Required("ip_address"): str,
                vol.Required("port", default=8750): int,
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )
