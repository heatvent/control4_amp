import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN  # Import the DOMAIN constant

class Control4AmpConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="Control4 Amplifier", data=user_input)

        data_schema = vol.Schema({
            vol.Required("host"): str,
            vol.Required("port", default=8750): int,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return Control4AmpOptionsFlowHandler(config_entry)

class Control4AmpOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        data_schema = vol.Schema({
            vol.Required("host", default=self.config_entry.data["host"]): str,
            vol.Required("port", default=self.config_entry.data.get("port", 8750)): int,
        })

        return self.async_show_form(
            step_id="init",
            data_schema=data_schema
        )
