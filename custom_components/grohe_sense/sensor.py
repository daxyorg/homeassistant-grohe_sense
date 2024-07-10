import logging
from typing import List

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import (DOMAIN)
from .api.ondus_api import OndusApi
from .dto.grohe_device import GroheDevice
from .entities.configuration.grohe_entity_configuration import GROHE_ENTITY_CONFIG, SensorTypes

from .entities.grohe_sense import GroheSenseEntity
from .entities.grohe_sense_guard import GroheSenseGuardWithdrawalsEntity
from .entities.grohe_sense_guard_reader import GroheSenseGuardReader
from .entities.grohe_sense_notifications import GroheSenseNotificationEntity
from .enum.ondus_types import GroheTypes

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    _LOGGER.debug(f'Adding sensor entities from config entry {entry}')

    if DOMAIN not in hass.data or 'devices' not in hass.data[DOMAIN]:
        _LOGGER.error(
            "Did not find shared objects. You may need to update your configuration (this module should no longer be "
            "configured under sensor).")
        return

    ondus_api: OndusApi = hass.data[DOMAIN]['session']

    entities: List[GroheSenseNotificationEntity | GroheSenseEntity | GroheSenseGuardWithdrawalsEntity] = []
    devices: List[GroheDevice] = hass.data[DOMAIN]['devices']

    for device in devices:
        reader = GroheSenseGuardReader(ondus_api, device)
        await reader.async_update()

        if device.type in GROHE_ENTITY_CONFIG:
            for sensors in GROHE_ENTITY_CONFIG.get(device.type):
                _LOGGER.debug(f'Attaching sensor {sensors} to device {device}')
                if sensors == SensorTypes.WATER_CONSUMPTION:
                    entities.append(GroheSenseGuardWithdrawalsEntity(DOMAIN, reader, device, sensors, 1))
                    entities.append(GroheSenseGuardWithdrawalsEntity(DOMAIN, reader, device, sensors, 7))
                elif sensors == SensorTypes.NOTIFICATION:
                    entities.append(GroheSenseNotificationEntity(DOMAIN, ondus_api, device, sensors))
                else:
                    entities.append(GroheSenseEntity(DOMAIN, reader, device, sensors))
        else:
            _LOGGER.warning('Unrecognized appliance %s, ignoring.', device)
    if entities:
        async_add_entities(entities)
