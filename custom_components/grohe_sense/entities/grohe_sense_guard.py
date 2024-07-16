from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .configuration.grohe_entity_configuration import SensorTypes, SENSOR_CONFIGURATION
from .grohe_update_coordinator import GroheUpdateCoordinator
from ..dto.grohe_device import GroheDevice


class GroheSenseGuardWithdrawalsEntity(CoordinatorEntity, SensorEntity):
    def __init__(self, domain: str, coordinator: GroheUpdateCoordinator, device: GroheDevice, sensor_type: SensorTypes):
        super().__init__(coordinator)
        self._coordinator = coordinator
        self._device = device
        self._sensor_type = sensor_type
        self._sensor = SENSOR_CONFIGURATION.get(sensor_type)
        self._value: float | None = None
        self._domain = domain

        # Needed for Sensor Entity
        self._attr_device_class = self._sensor.device_class
        self._attr_name = f'{self._device.name} {self._sensor_type.value}'
        self._attr_native_unit_of_measurement = self._sensor.unit_of_measurement
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING

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
        return self._value

    @callback
    def _handle_coordinator_update(self) -> None:
        self._value = self._coordinator.data.withdrawal
        self.async_write_ha_state()


