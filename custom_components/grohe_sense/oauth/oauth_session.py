import asyncio
import json
import logging

from aiohttp import ClientSession
from lxml import html

from custom_components.grohe_sense.oauth.oauth_exception import OauthException

_LOGGER = logging.getLogger(__name__)


async def get_refresh_token(session: ClientSession, base_url: str, username: str, password: str):
    try:
        response = await session.get(base_url + 'oidc/login')
    except Exception as e:
        _LOGGER.error('Get Refresh Token Exception %s', str(e))
    else:
        cookie = response.cookies
        tree = html.fromstring(await response.text())

        name = tree.xpath("//html/body/div/div/div/div/div/div/div/form")
        action = name[0].action

        payload = {
            'username': username,
            'password': password,
            'Content-Type': 'application/x-www-form-urlencoded',
            'origin': base_url,
            'referer': base_url + 'oidc/login',
            'X-Requested-With': 'XMLHttpRequest',
        }
        try:
            response = await session.post(url=action, data=payload, cookies=cookie, allow_redirects=False)
        except Exception as e:
            _LOGGER.error('Get Refresh Token Action Exception %s', str(e))
        else:
            ondus_url = response.headers['Location'].replace('ondus', 'https')
            try:
                response = await session.get(url=ondus_url, cookies=cookie)
            except Exception as e:
                _LOGGER.error('Get Refresh Token Response Exception %s', str(e))
            else:
                response_json = json.loads(await response.text())

    return response_json['refresh_token']


class OauthSession:
    def __init__(self, session: ClientSession, base_url: str, username, password, refresh_token):
        self._session = session
        self._base_url = base_url
        self._username = username
        self._password = password
        self._refresh_token = refresh_token
        self._access_token = None
        self._fetching_new_token = None

    @property
    def session(self):
        return self._session

    async def token(self, old_token=None):
        """ Returns an authorization header. If one is supplied as old_token, invalidate that one """
        if self._access_token not in (None, old_token):
            return self._access_token

        if self._fetching_new_token is not None:
            await self._fetching_new_token.wait()
            return self._access_token

        self._access_token = None
        self._fetching_new_token = asyncio.Event()
        data = {'refresh_token': self._refresh_token}
        headers = {'Content-Type': 'application/json'}

        refresh_response = await self._http_request(self._base_url + 'oidc/refresh', 'post', headers=headers, json=data)
        if not 'access_token' in refresh_response:
            _LOGGER.error('OAuth token refresh did not yield access token! Got back %s', refresh_response)
        else:
            self._access_token = 'Bearer ' + refresh_response['access_token']

        self._fetching_new_token.set()
        self._fetching_new_token = None
        return self._access_token

    async def get(self, url, **kwargs):
        return await self._http_request(url, auth_token=self, **kwargs)

    async def post(self, url, json, **kwargs):
        return await self._http_request(url, method='post', auth_token=self, json=json, **kwargs)

    async def _http_request(self, url, method='get', auth_token=None, headers={}, **kwargs):
        _LOGGER.debug('Making http %s request to %s, headers %s', method, url, headers)
        headers = headers.copy()
        tries = 0
        while True:
            if auth_token != None:
                # Cache token so we know which token was used for this request,
                # so we know if we need to invalidate.
                token = await auth_token.token()
                headers['Authorization'] = token
            try:
                async with self._session.request(method, url, headers=headers, **kwargs) as response:
                    _LOGGER.debug('Http %s request to %s got response %d', method, url, response.status)
                    if response.status in (200, 201):
                        return await response.json()
                    elif response.status == 401:
                        if auth_token != None:
                            _LOGGER.debug('Request to %s returned status %d, refreshing auth token', url,
                                          response.status)
                            token = await auth_token.token(token)
                        else:
                            _LOGGER.error(
                                'Grohe sense refresh token is invalid (or expired), please update your configuration with a new refresh token')
                            self._refresh_token = get_refresh_token(self._session, self._username, self._password)
                            token = await self.token(token)
                    else:
                        _LOGGER.debug('Request to %s returned status %d, %s', url, response.status,
                                      await response.text())
            except OauthException as oe:
                raise
            except Exception as e:
                _LOGGER.debug('Exception for http %s request to %s: %s', method, url, e)

            tries += 1
            await asyncio.sleep(min(600, 2 ** tries))
