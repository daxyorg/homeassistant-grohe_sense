from datetime import timedelta
from typing import List

from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import Throttle

from custom_components.grohe_sense.api.ondus_api import OndusApi
from custom_components.grohe_sense.dto.grohe_device import GroheDevice
from custom_components.grohe_sense.dto.ondus_dtos import Notification
from custom_components.grohe_sense.entities.configuration.grohe_entity_configuration import SensorTypes
from custom_components.grohe_sense.entities.grohe_update_coordinator import GroheUpdateCoordinator

NOTIFICATION_UPDATE_DELAY = timedelta(minutes=1)


class GroheSenseNotificationEntity(CoordinatorEntity, Entity):
    def __init__(self, domain: str, coordinator: GroheUpdateCoordinator, device: GroheDevice, sensor_type: SensorTypes):
        super().__init__(coordinator)

        self._coordinator = coordinator
        self._domain: str = domain
        self._device = device
        self._sensor_type = sensor_type
        self._value: str | None = None
        self._notifications: List[Notification] = []

        self._attr_name = f'{self._device.name} {self._sensor_type.value}'

    @property
    def device_info(self) -> DeviceInfo | None:
        return DeviceInfo(identifiers={(self._domain, self._device.appliance_id)},
                          name=self._device.name,
                          manufacturer='Grohe',
                          model=self._device.device_name,
                          sw_version=self._device.sw_version)

    @property
    def name(self):
        return f'{self._device.name} notifications'

    @property
    def state(self):
        return self._value

    @callback
    def _handle_coordinator_update(self) -> None:
        self._value = self._coordinator.data.notification
        self.async_write_ha_state()

