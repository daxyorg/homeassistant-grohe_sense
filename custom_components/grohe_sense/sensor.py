import logging
from typing import List

from . import (DOMAIN)
from .api.ondus_api import OndusApi
from .dto.grohe_device_dto import GroheDeviceDTO

from .entities.grohe_sense import GroheSenseEntity
from .entities.grohe_sense_guard import GroheSenseGuardWithdrawalsEntity
from .entities.grohe_sense_guard_reader import GroheSenseGuardReader
from .entities.grohe_sense_notifications import GroheSenseNotificationEntity
from .enum.grohe_sense_sensor_types_per_unit import SENSOR_TYPES_PER_UNIT
from .enum.ondus_types import GroheTypes
from .oauth.oauth_session import OauthSession

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    _LOGGER.debug("Starting Grohe Sense sensor")

    if DOMAIN not in hass.data or 'devices' not in hass.data[DOMAIN]:
        _LOGGER.error(
            "Did not find shared objects. You may need to update your configuration (this module should no longer be "
            "configured under sensor).")
        return

    auth_session: OauthSession = hass.data[DOMAIN]['session']
    ondus_api = OndusApi(auth_session)

    entities: List[GroheSenseNotificationEntity | GroheSenseEntity | GroheSenseGuardWithdrawalsEntity] = []
    devices: List[GroheDeviceDTO] = hass.data[DOMAIN]['devices']

    for device in devices:
        reader = GroheSenseGuardReader(ondus_api, device)
        entities.append(GroheSenseNotificationEntity(ondus_api, device))

        if device.type in SENSOR_TYPES_PER_UNIT:
            for info in SENSOR_TYPES_PER_UNIT.get(device.type, []):
                entities.append(GroheSenseEntity(reader, device.name, info))

            if device.type == GroheTypes.GROHE_SENSE_GUARD:  # The sense guard also gets sensor entities for water flow
                entities.append(GroheSenseGuardWithdrawalsEntity(reader, device.name, 1))
                entities.append(GroheSenseGuardWithdrawalsEntity(reader, device.name, 7))
        else:
            _LOGGER.warning('Unrecognized appliance %s, ignoring.', device)
    if entities:
        async_add_entities(entities)
