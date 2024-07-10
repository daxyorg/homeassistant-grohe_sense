import logging
from typing import List

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import aiohttp_client
from custom_components.grohe_sense.api.ondus_api import OndusApi
from custom_components.grohe_sense.const import DOMAIN, CONF_USERNAME, CONF_PASSWORD, CONF_PLATFORM
from custom_components.grohe_sense.dto.grohe_device import GroheDevice
from custom_components.grohe_sense.enum.ondus_types import GroheTypes

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    _LOGGER.debug("Loading Grohe Sense")

    session = aiohttp_client.async_get_clientsession(hass)

    api = OndusApi(session)
    state = await api.login(entry.data[CONF_USERNAME], entry.data[CONF_PASSWORD])

    devices: List[GroheDevice] = await GroheDevice.get_devices(api)

    hass.data[DOMAIN] = {'session': api, 'devices': devices}

    await hass.config_entries.async_forward_entry_setups(entry, CONF_PLATFORM)

    return state
