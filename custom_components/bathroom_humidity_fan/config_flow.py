import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN

@callback
def configured_instances(hass):
    """Return a set of configured instances."""
    return set(entry.title for entry in hass.config_entries.async_entries(DOMAIN))

class BathroomHumidityFanConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Bathroom Humidity Fan."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            if user_input["name"] in configured_instances(self.hass):
                errors["name"] = "name_exists"
            else:
                return self.async_create_entry(title=user_input["name"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("name"): str,
                vol.Required("sensor_entity_id"): str,
                vol.Required("fan_entity_id"): str,
            }),
            errors=errors,
        )
