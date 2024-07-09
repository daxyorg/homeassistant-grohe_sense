from datetime import timedelta
from typing import List

from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

from custom_components.grohe_sense.api.ondus_api import OndusApi
from custom_components.grohe_sense.dto.grohe_device_dto import GroheDevice
from custom_components.grohe_sense.dto.ondus_dtos import Notification

NOTIFICATION_UPDATE_DELAY = timedelta(minutes=1)


class GroheSenseNotificationEntity(Entity):
    def __init__(self, ondus_api: OndusApi, device: GroheDevice):
        self._ondus_api = ondus_api
        self._device = device
        self._notifications: List[Notification] = []

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

        self._notifications = await self._ondus_api.get_appliance_notifications(self._device.location_id,
                                                                                self._device.room_id,
                                                                                self._device.appliance_id)

        self._notifications.sort(key=lambda n: n.timestamp, reverse=True)
