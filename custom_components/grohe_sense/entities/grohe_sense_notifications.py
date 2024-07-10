from datetime import timedelta
from typing import List

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

from custom_components.grohe_sense.api.ondus_api import OndusApi
from custom_components.grohe_sense.dto.grohe_device import GroheDevice
from custom_components.grohe_sense.dto.ondus_dtos import Notification
from custom_components.grohe_sense.entities.configuration.grohe_entity_configuration import SensorTypes

NOTIFICATION_UPDATE_DELAY = timedelta(minutes=1)


class GroheSenseNotificationEntity(Entity):
    def __init__(self, domain: str, api: OndusApi, device: GroheDevice, sensor_type: SensorTypes):
        self._api = api
        self._domain: str = domain
        self._device = device
        self._sensor_type = sensor_type
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
        def truncate_string(l, s):
            if len(s) > l:
                return s[:l - 4] + ' ...'
            return s

        notifications = [notification for notification in self._notifications if notification.is_read is False]

        if len(notifications) > 0:
            return f'{notifications[0].notification_text}'
        else:
            return 'No notifications'

    @Throttle(NOTIFICATION_UPDATE_DELAY)
    async def async_update(self):
        # Reset notifications
        self._notifications = []

        self._notifications = await self._api.get_appliance_notifications(self._device.location_id,
                                                                          self._device.room_id,
                                                                          self._device.appliance_id)

        self._notifications.sort(key=lambda n: n.timestamp, reverse=True)
