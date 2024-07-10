from homeassistant.components.sensor import SensorEntity
from homeassistant.const import STATE_UNKNOWN, STATE_UNAVAILABLE
from homeassistant.helpers.device_registry import DeviceInfo

from .configuration.grohe_entity_configuration import SensorTypes, SENSOR_CONFIGURATION
from .grohe_sense_guard_reader import GroheSenseGuardReader
from ..dto.grohe_device import GroheDevice


class GroheSenseEntity(SensorEntity):
    def __init__(self, domain: str, reader: GroheSenseGuardReader, device: GroheDevice, sensor_type: SensorTypes):
        super().__init__()
        self._reader = reader
        self._device = device
        self._sensor_type = sensor_type
        self._sensor = SENSOR_CONFIGURATION.get(sensor_type)
        self._domain = domain

        # Needed for Sensor Entity
        self._attr_device_class = self._sensor.device_class
        self._attr_name = f'{self._device.name} {self._sensor_type.value}'
        self._attr_native_unit_of_measurement = self._sensor.unit_of_measurement

    @property
    def device_info(self) -> DeviceInfo | None:
        return DeviceInfo(identifiers={(self._domain, self._device.appliance_id)},
                          name=self._device.name,
                          manufacturer='Grohe',
                          model=self._device.device_name,
                          sw_version=self._device.sw_version)

    @property
    def unique_id(self):
        return f'{self._device.appliance_id}_{self._sensor_type.value}'

    @property
    def native_value(self):
        raw_state = self._reader.measurement(self._sensor_type)
        if raw_state in (STATE_UNKNOWN, STATE_UNAVAILABLE):
            return raw_state
        else:
            # Return the value of the calculation specific for each sensor
            return self._sensor.function(raw_state)

    async def async_update(self):
        await self._reader.async_update()
