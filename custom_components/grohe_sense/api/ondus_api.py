import datetime
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
        url = f'{self.__api_url}/dashboard'
        data = await self._session.get(url)
        return Locations.from_json(data)

    async def get_locations(self) -> List[Location]:
        url = f'{self.__api_url}/locations'
        data = await self._session.get(url)
        locations = []
        for location in data:
            locations.append(Location.from_json(location))
        return locations

    async def get_rooms(self, location_id: string) -> List[Room]:
        url = f'{self.__api_url}/locations/{location_id}/rooms'
        data = await self._session.get(url)
        rooms = []
        for room in data:
            rooms.append(Room.from_json(room))
        return rooms

    async def get_appliances(self, location_id: string, room_id: string) -> List[Appliance]:
        url = f'{self.__api_url}/locations/{location_id}/rooms/{room_id}/appliances'
        data = await self._session.get(url)
        appliances = []
        for appliance in data:
            appliances.append(Appliance.from_json(appliance))
        return appliances

    async def get_appliance_info(self, location_id: string, room_id: string, appliance_id: string) -> Appliance:
        url = f'{self.__api_url}/locations/{location_id}/rooms/{room_id}/appliances/{appliance_id}'
        data = await self._session.get(url)
        return Appliance.from_json(data)

    async def get_appliance_details(self, location_id: string, room_id: string, appliance_id: string) -> Appliance:
        url = f'{self.__api_url}/locations/{location_id}/rooms/{room_id}/appliances/{appliance_id}/details'
        data = await self._session.get(url)
        return Appliance.from_json(data)

    async def get_appliance_status(self, location_id: string, room_id: string, appliance_id: string) -> List[Status]:
        url = f'{self.__api_url}/locations/{location_id}/rooms/{room_id}/appliances/{appliance_id}/status'
        data = await self._session.get(url)
        return [Status.from_json(state) for state in data]

    async def get_appliance_command(self, location_id: string, room_id: string, appliance_id: string) \
            -> ApplianceCommand:
        url = f'{self.__api_url}/locations/{location_id}/rooms/{room_id}/appliances/{appliance_id}/command'
        data = await self._session.get(url)
        return ApplianceCommand.from_json(data)

    async def get_appliance_notifications(self, location_id: string, room_id: string, appliance_id: string) \
            -> List[Notification]:
        url = f'{self.__api_url}/locations/{location_id}/rooms/{room_id}/appliances/{appliance_id}/notifications'
        data = await self._session.get(url)
        notifications = []
        for notification in data:
            notifications.append(Notification.from_json(notification))
        return notifications

    async def get_appliance_data(self, location_id: string, room_id: string, appliance_id: string,
                                 from_date: Optional[datetime] = None, to_date: Optional[datetime] = None,
                                 group_by: Optional[OndusGroupByTypes] = None) -> MeasurementData:
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
        return MeasurementData.from_json(data)
