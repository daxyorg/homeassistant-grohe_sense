from collections import namedtuple

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import UnitOfTemperature, PERCENTAGE, UnitOfVolume, UnitOfPressure

SensorType = namedtuple('SensorType', ['unit', 'device_class', 'function'])

SENSOR_TYPES = {
    'temperature': SensorType(UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, lambda x: x),
    'humidity': SensorType(PERCENTAGE, SensorDeviceClass.HUMIDITY, lambda x: x),
    'flowrate': SensorType(UnitOfVolume.LITERS, None, lambda x: x * 3.6),
    'pressure': SensorType(UnitOfPressure.BAR, SensorDeviceClass.PRESSURE, lambda x: x),
    'temperature_guard': SensorType(UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, lambda x: x),
}

