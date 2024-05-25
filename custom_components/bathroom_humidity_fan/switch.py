from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, CONF_FAN, CONF_SENSOR

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the switch platform."""
    fan_id = config_entry.data[CONF_FAN]
    sensor_id = config_entry.data[CONF_SENSOR]

    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities([BathroomFanSwitch(coordinator, fan_id, sensor_id)], True)

class BathroomFanSwitch(CoordinatorEntity, SwitchEntity):
    """Representation of a Switch."""

    def __init__(self, coordinator, fan_id, sensor_id):
        """Initialize the switch."""
        super().__init__(coordinator)
        self._fan_id = fan_id
        self._sensor_id = sensor_id
        self._is_on = False

    @property
    def name(self):
        """Return the name of the switch."""
        return "Bathroom Fan"

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self._is_on

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        await self.hass.services.async_call("switch", "turn_on", {"entity_id": self._fan_id})
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        await self.hass.services.async_call("switch", "turn_off", {"entity_id": self._fan_id})
        self._is_on = False
        self.async_write_ha_state()

    async def async_update(self):
        """Update the switch state."""
        await self.coordinator.async_request_refresh()
        humidity = self.coordinator.data["humidity"]
        average_humidity = self.hass.states.get(self._sensor_id).state
        if humidity > (float(average_humidity) + 5):
            await self.async_turn_on()
        elif humidity <= float(average_humidity):
            await self.async_turn_off()
