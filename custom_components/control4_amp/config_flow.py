"""Config flow for Control4 C4-8AMP1-B."""

from typing import Any, Dict

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant

from .const import DOMAIN

class Control4AmpConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Control4 C4-8AMP1-B."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> dict:
        """Handle the initial step."""
        if user_input is not None:
            # Validate the IP address
            ip_address = user_input.get("ip_address")
            return self.async_create_entry(
                title="Control4 C4-8AMP1-B",
                data={"ip_address": ip_address}
            )

        schema = vol.Schema({
            vol.Required("ip_address"): str
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema
        )
