from homeassistant.const import STATE_UNKNOWN, STATE_UNAVAILABLE
from homeassistant.helpers.entity import Entity

from .grohe_sense_guard_reader import GroheSenseGuardReader
from ..enum.grohe_sense_sensor_types import SENSOR_TYPES


class GroheSenseEntity(Entity):
    def __init__(self, reader: GroheSenseGuardReader, name: str, key: str):
        self._reader = reader
        self._name = name
        self._key = key

    @property
    def name(self):
        return '{} {}'.format(self._name, self._key)

    @property
    def unit_of_measurement(self):
        return SENSOR_TYPES[self._key].unit

    @property
    def device_class(self):
        return SENSOR_TYPES[self._key].device_class

    @property
    def state(self):
        raw_state = self._reader.measurement(self._key)
        if raw_state in (STATE_UNKNOWN, STATE_UNAVAILABLE):
            return raw_state
        else:
            return SENSOR_TYPES[self._key].function(raw_state)

    async def async_update(self):
        await self._reader.async_update()
