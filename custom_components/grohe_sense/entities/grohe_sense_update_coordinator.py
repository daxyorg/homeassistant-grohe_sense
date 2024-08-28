import logging
from datetime import timedelta
from typing import List, Tuple
from datetime import datetime

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from custom_components.grohe_sense.api.ondus_api import OndusApi
from custom_components.grohe_sense.dto.grohe_coordinator_dtos import MeasurementSenseDto, CoordinatorDto
from custom_components.grohe_sense.dto.grohe_device import GroheDevice
from custom_components.grohe_sense.dto.ondus_dtos import Notification
from custom_components.grohe_sense.enum.ondus_types import GroheTypes

_LOGGER = logging.getLogger(__name__)


class GroheSenseUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, device: GroheDevice, api: OndusApi) -> None:
        super().__init__(hass, _LOGGER, name='Grohe Sense', update_interval=timedelta(seconds=300), always_update=True)
        self._api = api
        self._device = device
        self._last_update = datetime.now()
        self._notifications: List[Notification] = []

    async def _get_notification(self) -> str:
        """
        Get the latest notification for the device.

        :return: The latest notification text. If no notifications are found, returns 'No notifications'.
        :rtype: str
        """
        notifications = await self._api.get_appliance_notifications(self._device.location_id, self._device.room_id,
                                                                    self._device.appliance_id)
        notifications.sort(key=lambda n: n.timestamp, reverse=True)
        notifications = [notification for notification in notifications if notification.is_read is False]

        if len(notifications) > 0:
            return f'{notifications[0].notification_text}'
        else:
            return 'No notifications'

    async def _get_measurements(self) -> Tuple[MeasurementSenseDto, float]:
        """
        This method retrieves the latest measurements and withdrawals for a given device.

        :param self: The current object instance.
        :return: A tuple containing the latest measurement (MeasurementDto object) and the latest withdrawal value
                 (float). If no measurement or withdrawal data is available, the corresponding values will be None.
        :rtype: Tuple[MeasurementSenseDto, float]
        """
        measurements_response = await self._api.get_appliance_data(self._device.location_id, self._device.room_id,
                                                                   self._device.appliance_id,
                                                                   self._last_update, None, None, True)

        withdrawal: float | None = None
        measurement = MeasurementSenseDto()
        if measurements_response is not None:
            if measurements_response.data is not None:
                if measurements_response.data.measurement is not None:
                    """Get the first measurement of the device. This is also the latest measurement"""
                    measurements_response.data.measurement.sort(key=lambda m: m.date, reverse=True)
                    measure = measurements_response.data.measurement[0]

                    measurement.flow_rate = measure.flow_rate
                    measurement.pressure = measure.pressure
                    measurement.humidity = measure.humidity

                    if self._device.type == GroheTypes.GROHE_SENSE:
                        measurement.temperature = measure.temperature
                    elif self._device.type == GroheTypes.GROHE_SENSE_GUARD:
                        measurement.temperature = measure.temperature_guard

                if measurements_response.data.withdrawals is not None:
                    withdrawals = measurements_response.data.withdrawals
                    withdrawals.sort(key=lambda m: m.date, reverse=True)
                    withdrawal = withdrawals[0].waterconsumption if withdrawals else None

        return measurement, withdrawal

    async def _async_update_data(self) -> CoordinatorDto:
        try:

            data = CoordinatorDto()
            data.measurement, data.withdrawal = await self._get_measurements()
            data.notification = await self._get_notification()

            self._last_update = datetime.now()
            return data

        except Exception as e:
            _LOGGER.error("Error updating Grohe Sense data: %s", str(e))
