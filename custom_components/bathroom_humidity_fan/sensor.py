from datetime import timedelta
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity, UpdateFailed
import logging

from .const import DOMAIN, CONF_SENSOR

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the sensor platform."""
    sensor_id = config_entry.data[CONF_SENSOR]

    coordinator = HumidityDataUpdateCoordinator(
        hass,
        sensor_id=sensor_id,
        update_interval=timedelta(minutes=10),
    )
    await coordinator.async_refresh()

    if not coordinator.last_update_success:
        raise UpdateFailed("Failed to fetch data")

    async_add_entities([HumiditySensor(coordinator)], True)

class HumidityDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data."""

    def __init__(self, hass, sensor_id, update_interval):
        """Initialize."""
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=update_interval)
        self.sensor_id = sensor_id

    async def _async_update_data(self):
        """Fetch data."""
        try:
            state = self.hass.states.get(self.sensor_id)
            if state is None:
                raise UpdateFailed(f"Sensor {self.sensor_id} not found")
            return {"humidity": float(state.state)}
        except Exception as exception:
            raise UpdateFailed(f"Error communicating with API: {exception}")

class HumiditySensor(CoordinatorEntity, SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, coordinator):
        """Initialize."""
        super().__init__(coordinator)
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Bathroom Humidity Average"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data["humidity"]
