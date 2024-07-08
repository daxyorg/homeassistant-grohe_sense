import logging
from typing import List

import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from homeassistant.helpers import aiohttp_client
from homeassistant.helpers.discovery import async_load_platform

from custom_components.grohe_sense.api.ondus_api import OndusApi
from custom_components.grohe_sense.dto.grohe_device_dto import GroheDeviceDTO
from custom_components.grohe_sense.enum.ondus_types import GroheTypes

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'grohe_sense'
BASE_URL = 'https://idp2-apigw.cloud.grohe.com/v3/iot/'
CONF_USERNAME = 'username'
CONF_PASSWORD = 'password'

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema({
            vol.Required(CONF_USERNAME): cv.string,
            vol.Required(CONF_PASSWORD): cv.string,
        }),
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass, config):
    _LOGGER.debug("Loading Grohe Sense")

    await initialize_shared_objects(hass, config.get(DOMAIN).get(CONF_USERNAME), config.get(DOMAIN).get(CONF_PASSWORD))

    await async_load_platform(hass, 'sensor', DOMAIN, {}, config)
    await async_load_platform(hass, 'switch', DOMAIN, {}, config)
    return True


async def initialize_shared_objects(hass, username, password):
    session = aiohttp_client.async_get_clientsession(hass)

    ondus_api = OndusApi(session)
    await ondus_api.login(username, password)

    devices: List[GroheDeviceDTO] = []

    hass.data[DOMAIN] = {'session': ondus_api, 'devices': devices}

    locations = await ondus_api.get_locations()

    for location in locations:
        _LOGGER.debug('Found location %s', location)
        rooms = await ondus_api.get_rooms(location.id)
        for room in rooms:
            _LOGGER.debug('Found room %s', room)
            appliances = await ondus_api.get_appliances(location.id, room.id)
            for appliance in appliances:
                _LOGGER.debug('Found appliance %s', appliance)
                devices.append(
                    GroheDeviceDTO(location.id, room.id, appliance.id, GroheTypes(appliance.type), appliance.name))
