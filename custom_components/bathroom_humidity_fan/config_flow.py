import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.selector import EntitySelector

from .const import DOMAIN, CONF_SENSOR, CONF_FAN

class BathroomHumidityFanConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Bathroom Humidity Fan."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return BathroomHumidityFanOptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title="Bathroom Humidity Fan", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_SENSOR): EntitySelector(domain="sensor"),
                vol.Required(CONF_FAN): EntitySelector(domain="switch")
            })
        )

class BathroomHumidityFanOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(CONF_SENSOR, default=self.config_entry.data[CONF_SENSOR]): EntitySelector(domain="sensor"),
                vol.Required(CONF_FAN, default=self.config_entry.data[CONF_FAN]): EntitySelector(domain="switch")
            })
        )
