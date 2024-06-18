import logging
import asyncio
import collections
from typing import List

from lxml import html
import json

import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from homeassistant.helpers import aiohttp_client
from homeassistant.helpers.discovery import async_load_platform

from custom_components.grohe_sense.dto.grohe_device_dto import GroheDeviceDTO
from custom_components.grohe_sense.enum.grohe_types import GroheTypes
from custom_components.grohe_sense.oauth.oauth_session import OauthSession, get_refresh_token

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

GROHE_SENSE_TYPE = 101  # Type identifier for the battery powered water detector
GROHE_SENSE_GUARD_TYPE = 103  # Type identifier for sense guard, the water guard installed on your water pipe


async def async_setup(hass, config):
    _LOGGER.debug("Loading Grohe Sense")

    await initialize_shared_objects(hass, config.get(DOMAIN).get(CONF_USERNAME), config.get(DOMAIN).get(CONF_PASSWORD))

    await async_load_platform(hass, 'sensor', DOMAIN, {}, config)
    await async_load_platform(hass, 'switch', DOMAIN, {}, config)
    return True


async def initialize_shared_objects(hass, username, password):
    session = aiohttp_client.async_get_clientsession(hass)

    auth_session = OauthSession(session, BASE_URL, username, password,
                                await get_refresh_token(session, BASE_URL, username, password))

    devices: List[GroheDeviceDTO] = []

    hass.data[DOMAIN] = {'session': auth_session, 'devices': devices}

    locations = await auth_session.get(BASE_URL + f'locations')

    for location in locations:
        _LOGGER.debug('Found location %s', location)
        locationId = location['id']
        rooms = await auth_session.get(BASE_URL + f'locations/{locationId}/rooms')
        for room in rooms:
            _LOGGER.debug('Found room %s', room)
            roomId = room['id']
            appliances = await auth_session.get(BASE_URL + f'locations/{locationId}/rooms/{roomId}/appliances')
            for appliance in appliances:
                _LOGGER.debug('Found appliance %s', appliance)
                applianceId = appliance['appliance_id']
                devices.append(
                    GroheDeviceDTO(locationId, roomId, applianceId, GroheTypes(appliance['type']), appliance['name']))
