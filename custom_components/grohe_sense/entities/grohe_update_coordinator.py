import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from custom_components.grohe_sense.api.ondus_api import OndusApi

_LOGGER = logging.getLogger(__name__)


class GroheUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, api: OndusApi) -> None:
        super().__init__(hass, _LOGGER, name='Grohe Sense', update_interval=timedelta(minutes=5), always_update=True)
        self._api = api
