from datetime import datetime, timezone, timedelta

from homeassistant.const import UnitOfVolume
from homeassistant.helpers.entity import Entity

from .grohe_sense_guard_reader import GroheSenseGuardReader


class GroheSenseGuardWithdrawalsEntity(Entity):
    def __init__(self, reader: GroheSenseGuardReader, name, days):
        self._reader = reader
        self._name = name
        self._days = days

    @property
    def name(self):
        return '{} {} day'.format(self._name, self._days)

    @property
    def unit_of_measurement(self):
        return UnitOfVolume.LITERS

    @property
    def state(self):
        if self._days == 1:  # special case, if we're averaging over 1 day, just count since midnight local time
            since = datetime.now(tz=timezone.utc).date()
        else:  # otherwise, it's a rolling X day average
            since = (datetime.now(tz=timezone.utc) - timedelta(self._days)).date()
        return self._reader.get_water_consumption_since(since)

    async def async_update(self):
        await self._reader.async_update()



