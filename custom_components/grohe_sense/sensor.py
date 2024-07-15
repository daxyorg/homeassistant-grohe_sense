from typing import List
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import (DOMAIN)
from .api.ondus_api import OndusApi
from .dto.grohe_device import GroheDevice
from .entities.configuration.grohe_entity_configuration import GROHE_ENTITY_CONFIG, SensorTypes
from .entities.grohe_sense import GroheSenseEntity
from .entities.grohe_sense_guard import GroheSenseGuardWithdrawalsEntity
from .entities.grohe_sense_notifications import GroheSenseNotificationEntity
from .entities.grohe_update_coordinator import GroheUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    _LOGGER.debug(f'Adding sensor entities from config entry {entry}')

    ondus_api: OndusApi = hass.data[DOMAIN]['session']

    entities: List[GroheSenseNotificationEntity | GroheSenseEntity | GroheSenseGuardWithdrawalsEntity] = []
    devices: List[GroheDevice] = hass.data[DOMAIN]['devices']

    for device in devices:
        coordinator = GroheUpdateCoordinator(hass, device, ondus_api)

        if device.type in GROHE_ENTITY_CONFIG:
            for sensors in GROHE_ENTITY_CONFIG.get(device.type):
                _LOGGER.debug(f'Attaching sensor {sensors} to device {device}')
                if sensors == SensorTypes.WATER_CONSUMPTION:
                    entities.append(GroheSenseGuardWithdrawalsEntity(DOMAIN, coordinator, device, sensors))
                elif sensors == SensorTypes.NOTIFICATION:
                    entities.append(GroheSenseNotificationEntity(DOMAIN, coordinator, device, sensors))
                else:
                    entities.append(GroheSenseEntity(DOMAIN, coordinator, device, sensors))
        else:
            _LOGGER.warning('Unrecognized appliance %s, ignoring.', device)
        await coordinator.async_request_refresh()

    if entities:
        async_add_entities(entities, update_before_add=True)
