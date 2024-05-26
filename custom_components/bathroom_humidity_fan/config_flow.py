import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

@callback
def configured_instances(hass):
    """Return a set of configured instances."""
    return set(entry.title for entry in hass.config_entries.async_entries(DOMAIN))

class BathroomHumidityFanConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Bathroom Humidity Fan."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        _LOGGER.debug("Starting async_step_user with input: %s", user_input)
        errors = {}
        if user_input is not None:
            if user_input["name"] in configured_instances(self.hass):
                errors["base"] = "name_exists"
            else:
                _LOGGER.debug("Creating entry with data: %s", user_input)
                return self.async_create_entry(title=user_input["name"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("name"): str,
                vol.Required("sensor_entity_id"): str,
                vol.Required("fan_entity_id"): str,
            }),
            errors=errors,
            description_placeholders={
                "name": "Nom de cette instance de ventilateur d'humidité",
                "sensor_entity_id": "ID de l'entité du capteur d'humidité (par ex. sensor.salle_de_bain_humidite)",
                "fan_entity_id": "ID de l'entité du ventilateur (par ex. switch.salle_de_bain_ventilateur)"
            }
        )
