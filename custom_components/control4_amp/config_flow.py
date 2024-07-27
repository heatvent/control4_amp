import logging
import ipaddress
import voluptuous as vol
from homeassistant import config_entries, exceptions
from homeassistant.core import callback
from homeassistant.const import CONF_IP_ADDRESS, CONF_PORT, CONF_NAME
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class Control4AmpConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Manage the Control4 Amp configuration flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return OptionsFlow(config_entry)

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user interface."""
        errors = {}
        if user_input is not None:
            try:
                ipaddress.ip_address(user_input[CONF_IP_ADDRESS])
                if user_input[CONF_PORT] <= 0 or user_input[CONF_PORT] > 65535:
                    raise ValueError("Invalid port number.")
                _LOGGER.debug("Processing user input: %s", user_input)
                return self.async_create_entry(title="Control4 Amp", data=user_input)
            except ValueError as e:
                _LOGGER.error("Validation error: %s", e)
                errors["base"] = "invalid_input"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_NAME): str,
                vol.Required(CONF_IP_ADDRESS): str,
                vol.Required(CONF_PORT, default=8750): int,
            }),
            errors=errors
        )

class InvalidInput(exceptions.HomeAssistantError):
    """Error to indicate the input is invalid."""

class OptionsFlow(config_entries.OptionsFlow):
    """Handle an options flow for Control4 Amp."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Optional(CONF_IP_ADDRESS, default=self.config_entry.options.get(CONF_IP_ADDRESS)): str,
                vol.Optional(CONF_PORT, default=self.config_entry.options.get(CONF_PORT)): int,
            })
        )
