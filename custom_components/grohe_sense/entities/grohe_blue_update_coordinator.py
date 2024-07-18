import logging
from datetime import timedelta
from typing import List, Tuple
from datetime import datetime

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from custom_components.grohe_sense.api.ondus_api import OndusApi
from custom_components.grohe_sense.dto.grohe_coordinator_dtos import MeasurementSenseDto, CoordinatorDto, \
    MeasurementBlueDto
from custom_components.grohe_sense.dto.grohe_device import GroheDevice
from custom_components.grohe_sense.dto.ondus_dtos import Notification
from custom_components.grohe_sense.enum.ondus_types import GroheTypes

_LOGGER = logging.getLogger(__name__)


class GroheBlueUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, device: GroheDevice, api: OndusApi) -> None:
        super().__init__(hass, _LOGGER, name='Grohe Blue', update_interval=timedelta(seconds=300), always_update=True)
        self._api = api
        self._device = device
        self._last_update = datetime.now()
        self._notifications: List[Notification] = []

    async def _get_measurement_and_notification(self) -> Tuple[MeasurementBlueDto | None, str]:
        """
        This method retrieves the latest measurements and withdrawals for a given device.

        :param self: The current object instance.
        :return: A tuple containing the latest measurement (MeasurementDto object) and the latest withdrawal value
                 (float). If no measurement or withdrawal data is available, the corresponding values will be None.
        :rtype: Tuple[MeasurementSenseDto, float]
        """
        notification: str = 'No notification'
        measurement: MeasurementBlueDto | None = None

        details = await self._api.get_appliance_details(self._device.location_id, self._device.room_id,
                                                        self._device.appliance_id)
        if details.notifications is not None:
            details.notifications.sort(key=lambda n: n.timestamp, reverse=True)
            notifications = [notify for notify in details.notifications if notify.is_read is False]

            if len(notifications) > 0:
                notification = f'{notifications[0].notification_text}'

        if details.data_latest.measurement is not None:
            measurement = MeasurementBlueDto.from_dict(details.data_latest.measurement)

        return measurement, notification

    async def _async_update_data(self) -> CoordinatorDto:
        try:

            data = CoordinatorDto()
            data.measurement, data.notification = await self._get_measurement_and_notification()

            self._last_update = datetime.now()
            return data

        except Exception as e:
            _LOGGER.error("Error updating Grohe Blue data: %s", str(e))
