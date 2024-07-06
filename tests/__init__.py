import asyncio

import aiohttp
from dotenv import load_dotenv
import os

from custom_components.grohe_sense.api.ondus_api import OndusApi
from custom_components.grohe_sense.oauth.oauth_session import OauthSession, get_refresh_token

load_dotenv()


async def bootstrap():
    httpclient = aiohttp.ClientSession()

    username = os.getenv("ONDUS_USERNAME")
    password = os.getenv("ONDUS_PASSWORD")
    base_url = 'https://idp2-apigw.cloud.grohe.com/v3/iot/'
    refresh_token = os.getenv('ONDUS_REFRESH_TOKEN')
    # await get_refresh_token(httpclient, base_url, username, password)

    print(refresh_token)

    session = OauthSession(httpclient, base_url, username, password, refresh_token)

    api = OndusApi(session)

    locations = await api.get_locations()
    rooms = await api.get_rooms(locations[0].id)
    appliances = await api.get_appliances(locations[0].id, rooms[1].id)
    dashboard = await api.get_dashboard()

    print(dashboard)

    await httpclient.close()


asyncio.run(bootstrap())
