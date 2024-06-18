import asyncio
import logging
from datetime import datetime, timezone, timedelta, date
from typing import List

from custom_components.grohe_sense.dto.measurement_guard_dto import MeasurementGuardDTO
from homeassistant.const import STATE_UNKNOWN, STATE_UNAVAILABLE

from custom_components.grohe_sense import BASE_URL
from custom_components.grohe_sense.dto.grohe_device_dto import GroheDeviceDTO
from custom_components.grohe_sense.dto.measurement_sense_dto import MeasurementSenseDTO
from custom_components.grohe_sense.dto.sensor_data_dto import SensorDataDTO
from custom_components.grohe_sense.dto.withdrawals_dto import WithdrawalDTO
from custom_components.grohe_sense.enum.grohe_types import GroheTypes

_LOGGER = logging.getLogger(__name__)


class GroheSenseGuardReader:

    def __init__(self, auth_session, device: GroheDeviceDTO):
        self._auth_session = auth_session
        self._device = device

        self._sensor_data: SensorDataDTO | None = None
        self.poll_from = datetime.now()
        self._fetching_data = None
        self._data_fetch_completed = datetime.min

    @property
    def applianceId(self):
        """ returns the appliance Identifier, looks like a UUID, so hopefully unique """
        return self._device.applianceId

    @property
    def poll_from(self):
        return self._poll_from

    @poll_from.setter
    def poll_from(self, value: datetime):
        # Always get the values for the last seven days
        self._poll_from = value - timedelta(7)

    def __get_last_measurement(self) -> MeasurementGuardDTO | None:
        return self._sensor_data.measurement[0] if self._sensor_data.measurement else None

    async def async_update(self):
        if self._fetching_data is not None:
            await self._fetching_data.wait()
            return

        # XXX: Hardcoded 5 minute interval for now. Would be prettier to set this a bit more dynamically
        # based on the json response for the sense guard, and probably hardcode something longer for the sense.
        if datetime.now() - self._data_fetch_completed < timedelta(minutes=5):
            _LOGGER.debug('Skipping fetching new data, time since last fetch was only %s',
                          datetime.now() - self._data_fetch_completed)
            return

        _LOGGER.debug("Fetching new data for appliance %s with name %s", self._device.applianceId, self._device.name)
        self._fetching_data = asyncio.Event()

        poll_from = self._poll_from.strftime('%Y-%m-%d')

        measurements_response = await self._auth_session.get(
            BASE_URL + f'locations/{self._device.locationId}/rooms/{self._device.roomId}/appliances/{self._device.applianceId}/data/aggregated?from={poll_from}')

        measurements: List[MeasurementGuardDTO | MeasurementSenseDTO] = []
        withdrawals: List[WithdrawalDTO] = []

        if 'measurement' in measurements_response['data'] and measurements_response['data']['measurement'] is not None:
            for measurement in measurements_response['data']['measurement']:
                if self._device.type == GroheTypes.GROHE_SENSE:
                    measurements.append(MeasurementSenseDTO(**measurement))
                elif self._device.type == GroheTypes.GROHE_SENSE_GUARD:
                    measurements.append(MeasurementGuardDTO(**measurement))

            measurements.sort(key=lambda m: m.date, reverse=True)

            for measurement in measurements:
                measurement.date = datetime.strptime(measurement.date, '%Y-%m-%d').astimezone().date()

        if 'withdrawals' in measurements_response['data'] and measurements_response['data']['withdrawals'] is not None:
            for withdrawal in measurements_response['data']['withdrawals']:
                withdrawals.append(WithdrawalDTO(**withdrawal))
            withdrawals.sort(key=lambda m: m.date, reverse=True)

            for withdrawal in withdrawals:
                withdrawal.date = datetime.strptime(withdrawal.date, '%Y-%m-%d').astimezone().date()

        self._sensor_data: SensorDataDTO = SensorDataDTO(group_by=measurements_response['data']['group_by'],
                                                         measurement=measurements, withdrawals=withdrawals)

        _LOGGER.debug('Data read: %s', self._sensor_data)

        self._data_fetch_completed = datetime.now()
        self._fetching_data.set()
        self._fetching_data = None

    def get_water_consumption_since(self, since: date) -> float:
        """
        This function returns the water consumption for the days given by since

        :param since:
        :return:
        """
        # XXX: As self._withdrawals is sorted, we could speed this up by a binary search,
        #      but most likely data sets are small enough that a linear scan is fine.
        if self._sensor_data is not None:
            matched_data: [float] = []

            for w in self._sensor_data.withdrawals:
                if w.date >= since:
                    matched_data.append(w.waterconsumption)

            consumption = sum(matched_data)
            return consumption
        else:
            return STATE_UNAVAILABLE

    def measurement(self, key):
        if self._sensor_data is None:
            return STATE_UNAVAILABLE

        measurement = self.__get_last_measurement()
        if measurement.__dict__.get(key) is not None:
            return measurement.__dict__.get(key)
        return STATE_UNKNOWN
