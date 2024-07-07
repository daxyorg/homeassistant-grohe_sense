import datetime
import json
import string
import urllib.parse
from typing import List, Optional

from custom_components.grohe_sense.dto.ondus_dtos import Locations, Location, Room, Appliance, Notification, Status, \
    ApplianceCommand, MeasurementData
from custom_components.grohe_sense.enum.ondus_types import OndusGroupByTypes
from custom_components.grohe_sense.oauth.oauth_session import OauthSession


class OndusApi:
    __base_url: str = 'https://idp2-apigw.cloud.grohe.com'
    __api_url: str = __base_url + '/v3/iot'

    def __init__(self, session: OauthSession) -> None:
        self._session = session

    async def get_dashboard(self) -> Locations:
        """
        Get the dashboard information.
        These dashboard information include most of the data which can also be queried by the appliance itself

        :return: The locations information obtained from the dashboard.
        :rtype: Locations
        """
        url = f'{self.__api_url}/dashboard'
        data = await self._session.get(url)
        return Locations.from_dict(data)

    async def get_locations(self) -> List[Location]:
        """
        Get a list of locations.

        :return: A list of Location objects.
        :rtype: List[Location]
        """
        url = f'{self.__api_url}/locations'
        data = await self._session.get(url)
        return [Location.from_dict(location) for location in data]

    async def get_rooms(self, location_id: string) -> List[Room]:
        """
        Get the rooms for a given location.

        :param location_id: ID of the location containing the appliance.
        :type location_id: str
        :return: A list of Room objects representing the rooms.
        :rtype: List[Room]
        """
        url = f'{self.__api_url}/locations/{location_id}/rooms'
        data = await self._session.get(url)
        return [Room.from_dict(room) for room in data]

    async def get_appliances(self, location_id: string, room_id: string) -> List[Appliance]:
        """
        Get a list of appliances for a given location and room.

        :param location_id: ID of the location containing the appliance.
        :type location_id: str
        :param room_id: ID of the room containing the appliance.
        :type room_id: str
        :return: A list of Appliance objects representing the appliances in the specified location and room.
        :rtype: List[Appliance]
        """
        url = f'{self.__api_url}/locations/{location_id}/rooms/{room_id}/appliances'
        data = await self._session.get(url)
        return [Appliance.from_dict(appliance) for appliance in data]

    async def get_appliance_info(self, location_id: string, room_id: string, appliance_id: string) -> Appliance:
        """
        Get information about an appliance.

        :param location_id: ID of the location containing the appliance.
        :type location_id: str
        :param room_id: ID of the room containing the appliance.
        :type room_id: str
        :param appliance_id: ID of the appliance to get details for.
        :type appliance_id: str
        :return: The information of the appliance.
        :rtype: Appliance
        """
        url = f'{self.__api_url}/locations/{location_id}/rooms/{room_id}/appliances/{appliance_id}'
        data = await self._session.get(url)
        return Appliance.from_dict(data)

    async def get_appliance_details(self, location_id: string, room_id: string, appliance_id: string) -> Appliance:
        """
        Get details of an appliance by location, room, and appliance IDs.

        :param location_id: ID of the location containing the appliance.
        :type location_id: str
        :param room_id: ID of the room containing the appliance.
        :type room_id: str
        :param appliance_id: ID of the appliance to get details for.
        :type appliance_id: str
        :return: Appliance object containing the details.
        :rtype: Appliance
        """
        url = f'{self.__api_url}/locations/{location_id}/rooms/{room_id}/appliances/{appliance_id}/details'
        data = await self._session.get(url)
        return Appliance.from_dict(data)

    async def get_appliance_status(self, location_id: string, room_id: string, appliance_id: string) -> List[Status]:
        """
        Get the status of an appliance.

        :param location_id: ID of the location containing the appliance.
        :type location_id: str
        :param room_id: ID of the room containing the appliance.
        :type room_id: str
        :param appliance_id: ID of the appliance to get details for.
        :type appliance_id: str
        :return: A list of Status objects representing the current status of the appliance.
        :rtype: List[Status]
        """
        url = f'{self.__api_url}/locations/{location_id}/rooms/{room_id}/appliances/{appliance_id}/status'
        data = await self._session.get(url)
        return [Status.from_dict(state) for state in data]

    async def get_appliance_command(self, location_id: string, room_id: string, appliance_id: string) \
            -> ApplianceCommand:
        """
        Get possible commands for an appliance.

        :param location_id: ID of the location containing the appliance.
        :type location_id: str
        :param room_id: ID of the room containing the appliance.
        :type room_id: str
        :param appliance_id: ID of the appliance to get details for.
        :type appliance_id: str
        :return: The command for the specified appliance.
        :rtype: ApplianceCommand
        """
        url = f'{self.__api_url}/locations/{location_id}/rooms/{room_id}/appliances/{appliance_id}/command'
        data = await self._session.get(url)
        return ApplianceCommand.from_dict(data)

    async def get_appliance_notifications(self, location_id: string, room_id: string, appliance_id: string) \
            -> List[Notification]:
        """
        Returns the notifications associated with a specific appliance in a given room at a specific location.

        :param location_id: ID of the location containing the appliance.
        :type location_id: str
        :param room_id: ID of the room containing the appliance.
        :type room_id: str
        :param appliance_id: ID of the appliance to get details for.
        :type appliance_id: str
        :return: A list of Notification objects.
        :rtype: List[Notification]
        """
        url = f'{self.__api_url}/locations/{location_id}/rooms/{room_id}/appliances/{appliance_id}/notifications'
        data = await self._session.get(url)
        return [Notification.from_dict(notification) for notification in data]

    async def get_appliance_data(self, location_id: string, room_id: string, appliance_id: string,
                                 from_date: Optional[datetime] = None, to_date: Optional[datetime] = None,
                                 group_by: Optional[OndusGroupByTypes] = None) -> MeasurementData:
        """
        Retrieves aggregated data for a specific appliance within a room.

        :param location_id: ID of the location containing the appliance.
        :type location_id: str
        :param room_id: ID of the room containing the appliance.
        :type room_id: str
        :param appliance_id: ID of the appliance to get details for.
        :type appliance_id: str
        :param from_date: (optional) The starting date and time to retrieve data from. Defaults to None.
        :type from_date: datetime
        :param to_date: (optional) The ending date and time to retrieve data to. Defaults to None.
        :type to_date: datetime
        :param group_by: (optional) The time period for grouping the data. Defaults to None.
        :type group_by: OndusGroupByTypes
        :return: The aggregated measurement data for the specified appliance.
        :rtype: MeasurementData
        """
        url = f'{self.__api_url}/locations/{location_id}/rooms/{room_id}/appliances/{appliance_id}/data/aggregated'
        params = dict()

        if from_date is not None:
            params.update({'from': from_date.isoformat()})
        if to_date is not None:
            params.update({'to': to_date.isoformat()})
        if group_by is not None:
            params.update({'groupBy': group_by})

        if params:
            url += '?' + urllib.parse.urlencode(params)

        data = await self._session.get(url)
        return MeasurementData.from_dict(data)
