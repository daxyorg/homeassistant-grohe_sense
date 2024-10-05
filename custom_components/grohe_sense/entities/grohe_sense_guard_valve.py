import logging
from datetime import timedelta

from homeassistant.components.valve import ValveEntity, ValveEntityFeature, ValveDeviceClass
from homeassistant.const import STATE_UNKNOWN
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.util import Throttle

from custom_components.grohe_sense.api.ondus_api import OndusApi
from custom_components.grohe_sense.dto.grohe_device import GroheDevice
from custom_components.grohe_sense.enum.ondus_types import OndusCommands

_LOGGER = logging.getLogger(__name__)

VALVE_UPDATE_DELAY = timedelta(minutes=1)


class GroheSenseGuardValve(ValveEntity):
    def __init__(self, domain: str, auth_session: OndusApi, device: GroheDevice):
        self._auth_session = auth_session
        self._device = device
        self._domain = domain
        self._is_closed = STATE_UNKNOWN

        # Needed for ValveEntity
        self._attr_icon = 'mdi:water'
        self._attr_name = f'{self._device.name} valve'
        self._attr_supported_features = ValveEntityFeature.OPEN | ValveEntityFeature.CLOSE
        self._attr_device_class = ValveDeviceClass.WATER

    @property
    def unique_id(self):
        return f'{self._device.appliance_id}_valve'

    @property
    def device_info(self) -> DeviceInfo | None:
        return DeviceInfo(identifiers={(self._domain, self._device.appliance_id)},
                          name=self._device.name,
                          manufacturer='Grohe',
                          model='Sense Guard',
                          sw_version=self._device.sw_version)

    @property
    def reports_position(self) -> bool:
        return False

    @property
    def is_closed(self) -> bool:
        return self._is_closed

    @Throttle(VALVE_UPDATE_DELAY)
    async def async_update(self):
        command_response = await self._auth_session.get_appliance_command(self._device.location_id,
                                                                          self._device.room_id,
                                                                          self._device.appliance_id)

        if command_response and command_response.command and command_response.command.valve_open is not None:
            _LOGGER.debug(f'Valve_open state: {command_response.command.valve_open} for appliance '
                          f'{self._device.appliance_id}')
            self._is_closed = not command_response.command.valve_open
        else:
            _LOGGER.error('Failed to parse out valve_open from commands response: %s', command_response)

    async def _set_state(self, state):
        command_response = await self._auth_session.set_appliance_command(self._device.location_id,
                                                                          self._device.room_id,
                                                                          self._device.appliance_id,
                                                                          OndusCommands.OPEN_VALVE, state)
        if command_response.command.valve_open is not None:
            self._is_closed = not command_response.command.valve_open
        else:
            _LOGGER.warning('Got unknown response back when setting valve state: %s', command_response)

    async def async_open_valve(self) -> None:
        _LOGGER.info('Turning on water for %s', self._device.name)
        await self._set_state(True)

    async def async_close_valve(self, **kwargs):
        _LOGGER.info('Turning off water for %s', self._device.name)
        await self._set_state(False)
