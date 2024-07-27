import logging
import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class Control4AmpConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Manage the Control4 Amp configuration flow."""

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user interface."""
        _LOGGER.debug("User step called with input: %s", user_input)
        errors = {}
        if user_input is not None:
            _LOGGER.debug("Processing user input: %s", user_input)
            return self.async_create_entry(title="Control4 Amp", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("name"): str,
                vol.Required("ip_address"): str,
                vol.Required("port", default=8750): int,
            }),
            errors=errors
        )
