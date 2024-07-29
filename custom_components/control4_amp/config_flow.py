import logging
import ipaddress
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.const import CONF_IP_ADDRESS, CONF_PORT, CONF_NAME
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class Control4AmpConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Manage the Control4 Amp configuration flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user interface."""
        errors = {}
        if user_input is not None:
            try:
                ipaddress.ip_address(user_input[CONF_IP_ADDRESS])
                if user_input[CONF_PORT] <= 0 or user_input[CONF_PORT] > 65535:
                    raise ValueError("Invalid port number.")
                _LOGGER.debug("Processing user input: %s", user_input)
                # Unique ID can be set as IP or another unique identifier
                await self.async_set_unique_id(user_input[CONF_IP_ADDRESS])
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)
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
