from datetime import datetime, timezone, timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.device_registry import DeviceInfo

from .configuration.grohe_entity_configuration import SensorTypes, SENSOR_CONFIGURATION
from .grohe_sense_guard_reader import GroheSenseGuardReader
from ..dto.grohe_device import GroheDevice


class GroheSenseGuardWithdrawalsEntity(SensorEntity):
    def __init__(self, domain: str, reader: GroheSenseGuardReader, device: GroheDevice, sensor_type: SensorTypes,
                 days: int = 7):
        super().__init__()
        self._reader = reader
        self._device = device
        self._sensor_type = sensor_type
        self._sensor = SENSOR_CONFIGURATION.get(sensor_type)
        self._domain = domain
        self._days = days

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
        return f'{self._device.appliance_id}_{self._sensor_type.value}_{self._days}'

    @property
    def native_value(self):
        if self._days == 1:  # special case, if we're averaging over 1 day, just count since midnight local time
            since = datetime.now(tz=timezone.utc).date()
        else:  # otherwise, it's a rolling X day average
            since = (datetime.now(tz=timezone.utc) - timedelta(self._days)).date()
        return self._reader.get_water_consumption_since(since)

    async def async_update(self):
        await self._reader.async_update()



