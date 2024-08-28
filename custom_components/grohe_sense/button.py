import logging
from typing import List

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from . import (DOMAIN)
from .api.ondus_api import OndusApi
from .dto.grohe_device import GroheDevice
from .entities.grohe_sense_guard_button import GroheSenseGuardButton
from .entities.grohe_sense_guard_valve import GroheSenseGuardValve
from .enum.ondus_types import GroheTypes

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    _LOGGER.debug(f'Adding button entities from config entry {entry}')

    ondus_api: OndusApi = hass.data[DOMAIN]['session']
    devices: List[GroheDevice] = hass.data[DOMAIN]['devices']
    entities = []

    for device in filter(lambda d: d.type == GroheTypes.GROHE_SENSE_GUARD, devices):
        entities.append(
            GroheSenseGuardButton(DOMAIN, ondus_api, device))
    if entities:
        async_add_entities(entities)
