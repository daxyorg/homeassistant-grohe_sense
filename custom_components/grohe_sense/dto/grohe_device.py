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
    def sw_version(self) -> str:
        return self.appliance.version

    @property
    def stripped_sw_version(self) -> tuple[int, ...]:
        return tuple(map(int, self.appliance.version.split('.')[:2]))

    @property
    def name(self) -> str:
        return self.appliance.name

    @property
    def device_serial(self) -> str:
        return self.appliance.serial_number

    @property
    def type(self) -> GroheTypes:
        return GroheTypes(self.appliance.type)

    @property
    def device_name(self) -> str:
        dev_name = self.type
        if dev_name == GroheTypes.GROHE_SENSE:
            return 'Sense'
        elif dev_name == GroheTypes.GROHE_SENSE_GUARD:
            return 'Sense Guard'
        elif dev_name == GroheTypes.GROHE_SENSE_PLUS:
            return 'Sense Plus'
        elif dev_name == GroheTypes.GROHE_BLUE_PROFESSIONAL:
            return 'Blue Professional'
        else:
            return 'Unknown'

    @staticmethod
    async def get_devices(ondus_api: OndusApi) -> List['GroheDevice']:
        """
        Fetches all devices associated with the provided OndusApi instance.

        :param ondus_api: An instance of the OndusApi class.
        :type ondus_api: OndusApi
        :return: A list of GroheDevice objects representing the discovered devices.
        :rtype: List[GroheDevice]
        """
        _LOGGER.debug(f'Getting all available Grohe devices')
        devices: List[GroheDevice] = []

        locations = await ondus_api.get_locations()

        for location in locations:
            rooms = await ondus_api.get_rooms(location.id)
            for room in rooms:
                appliances = await ondus_api.get_appliances(location.id, room.id)
                for appliance in appliances:
                    _LOGGER.debug(
                        f'Found in location {location.id} and room {room.id} the following appliance: {appliance.id} '
                        f'from type {appliance.type} with name {appliance.name}'
                    )
                    devices.append(GroheDevice(location.id, room.id, appliance))

        return devices