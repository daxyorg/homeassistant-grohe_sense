import logging
from typing import List

from custom_components.grohe_sense.api.ondus_api import OndusApi
from custom_components.grohe_sense.dto.ondus_dtos import Appliance
from custom_components.grohe_sense.enum.ondus_types import GroheTypes

_LOGGER = logging.getLogger(__name__)


class GroheDevice:
    def __init__(self, location_id: int, room_id: int, appliance: Appliance):
        self._location_id = location_id
        self._room_id = room_id
        self.appliance = appliance
        GroheTypes(appliance.type)

    @property
    def location_id(self):
        return self._location_id

    @property
    def room_id(self):
        return self._room_id

    @property
    def appliance_id(self) -> str:
        return self.appliance.id

    @property
    def name(self) -> str:
        return self.appliance.name

    @property
    def device_serial(self) -> str:
        return self.appliance.serial_number

    @property
    def type(self) -> GroheTypes:
        return GroheTypes(self.appliance.type)

    @staticmethod
    async def get_devices(ondus_api: OndusApi) -> List['GroheDevice']:
        """
        Fetches all devices associated with the provided OndusApi instance.

        :param ondus_api: An instance of the OndusApi class.
        :type ondus_api: OndusApi
        :return: A list of GroheDevice objects representing the discovered devices.
        :rtype: List[GroheDevice]
        """
        devices: List[GroheDevice] = []

        locations = await ondus_api.get_locations()

        for location in locations:
            _LOGGER.debug('Found location %s', location)
            rooms = await ondus_api.get_rooms(location.id)
            for room in rooms:
                _LOGGER.debug('Found room %s', room)
                appliances = await ondus_api.get_appliances(location.id, room.id)
                for appliance in appliances:
                    _LOGGER.debug('Found appliance %s', appliance)
                    devices.append(GroheDevice(location.id, room.id, appliance))

        return devices
