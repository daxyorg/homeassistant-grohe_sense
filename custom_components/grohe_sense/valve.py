import logging
from datetime import (timedelta)
from typing import List

from homeassistant.components.valve import ValveEntity, ValveDeviceClass, ValveEntityFeature

from homeassistant.util import Throttle
from homeassistant.const import (STATE_UNKNOWN)

from . import (DOMAIN)
from .api.ondus_api import OndusApi
from .dto.grohe_device_dto import GroheDevice
from .enum.ondus_types import GroheTypes, OndusCommands

_LOGGER = logging.getLogger(__name__)

VALVE_UPDATE_DELAY = timedelta(minutes=1)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    _LOGGER.debug("Starting Grohe Sense valve switch")
    ondus_api: OndusApi = hass.data[DOMAIN]['session']
    devices: List[GroheDevice] = hass.data[DOMAIN]['devices']
    entities = []

    for device in filter(lambda d: d.type == GroheTypes.GROHE_SENSE_GUARD, devices):
        entities.append(
            GroheSenseGuardValve(ondus_api, device))
    if entities:
        async_add_entities(entities)


class GroheSenseGuardValve(ValveEntity):
    def __init__(self, auth_session: OndusApi, device: GroheDevice):
        self._auth_session = auth_session
        self._device = device
        self._is_closed = STATE_UNKNOWN

        # Needed for ValveEntity
        self._attr_icon = 'mdi:water'
        self._attr_name = f'{self._device.name} valve'
        self._attr_device_info = {
            'identifiers': {(DOMAIN, self._device.appliance_id)},
            'name': f'{self._device.name} valve',
            'manufacturer': 'Grohe',
            'model': 'Sense Guard',
        }
        self._attr_supported_features = ValveEntityFeature.OPEN | ValveEntityFeature.CLOSE
        self._attr_device_class = ValveDeviceClass.WATER

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

        if command_response.command.valve_open is not None:
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
