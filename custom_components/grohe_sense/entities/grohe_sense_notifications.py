from datetime import timedelta
from typing import List

from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

from custom_components.grohe_sense import BASE_URL
from custom_components.grohe_sense.dto.grohe_device_dto import GroheDeviceDTO
from custom_components.grohe_sense.dto.ondus_dtos import Notification

NOTIFICATION_UPDATE_DELAY = timedelta(minutes=1)

NOTIFICATION_TYPES = {
    # The protocol returns notification information as a (category, type) tuple, this maps to strings
    (10, 60): 'Firmware update available',
    (10, 460): 'Firmware update available',
    (20, 11): 'Battery low',
    (20, 12): 'Battery empty',
    (20, 20): 'Below temperature threshold',
    (20, 21): 'Above temperature threshold',
    (20, 30): 'Below humidity threshold',
    (20, 31): 'Above humidity threshold',
    (20, 40): 'Frost warning',
    (20, 80): 'Lost wifi',
    (20, 320): 'Unusual water consumption (water shut off)',
    (20, 321): 'Unusual water consumption (water not shut off)',
    (20, 330): 'Micro leakage',
    (20, 340): 'Frost warning',
    (20, 380): 'Lost wifi',
    (20, 381): 'Possible leakage.',
    (20, 385): 'Possible leakage. Leakage has increased',
    (30, 0): 'Flooding',
    (30, 310): 'Pipe break',
    (30, 400): 'Maximum volume reached',
    (30, 430): 'Sense detected water (water shut off)',
    (30, 431): 'Sense detected water (water not shut off)',
}


class GroheSenseNotificationEntity(Entity):
    def __init__(self, auth_session, device: GroheDeviceDTO):
        self._auth_session = auth_session
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
            return NOTIFICATION_TYPES.get((notifications[0].category, notifications[0].type),
                                          'Unknown notification: {}'.format(notifications[0]))
        else:
            return 'No notifications'

    @Throttle(NOTIFICATION_UPDATE_DELAY)
    async def async_update(self):
        # Reset notifications
        self._notifications = []

        notifications = await self._auth_session.get(
            BASE_URL + f'locations/{self._device.locationId}/rooms/{self._device.roomId}/appliances/{self._device.applianceId}/notifications')

        for notification in notifications:
            self._notifications.append(Notification(**notification))

        self._notifications.sort(key=lambda n: n.timestamp, reverse=True)
