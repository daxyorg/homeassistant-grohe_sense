from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Callable

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import UnitOfTemperature, PERCENTAGE, UnitOfVolumeFlowRate, UnitOfPressure, UnitOfVolume

from custom_components.grohe_sense.enum.ondus_types import GroheTypes


class SensorTypes(Enum):
    TEMPERATURE = 'temperature'
    HUMIDITY = 'humidity'
    FLOW_RATE = 'flow_rate'
    PRESSURE = 'pressure'
    NOTIFICATION = 'notification'
    WATER_CONSUMPTION = 'water_consumption'


@dataclass
class Sensor:
    device_class: SensorDeviceClass
    unit_of_measurement: str
    function: Callable[[float], float]


GROHE_ENTITY_CONFIG: Dict[GroheTypes, List[SensorTypes]] = {
    GroheTypes.GROHE_SENSE: [SensorTypes.TEMPERATURE, SensorTypes.HUMIDITY, SensorTypes.NOTIFICATION],
    GroheTypes.GROHE_SENSE_GUARD: [SensorTypes.TEMPERATURE, SensorTypes.FLOW_RATE, SensorTypes.PRESSURE,
                                   SensorTypes.NOTIFICATION, SensorTypes.WATER_CONSUMPTION],
    GroheTypes.GROHE_BLUE_PROFESSIONAL: [SensorTypes.NOTIFICATION]
}

SENSOR_CONFIGURATION: Dict[SensorTypes, Sensor] = {
    SensorTypes.TEMPERATURE: Sensor(SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS, lambda x: x),
    SensorTypes.HUMIDITY: Sensor(SensorDeviceClass.HUMIDITY, PERCENTAGE, lambda x: x),
    SensorTypes.FLOW_RATE: Sensor(SensorDeviceClass.VOLUME_FLOW_RATE, UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR,
                                  lambda x: x * 3.6),
    SensorTypes.PRESSURE: Sensor(SensorDeviceClass.PRESSURE, UnitOfPressure.BAR, lambda x: x),
    SensorTypes.WATER_CONSUMPTION: Sensor(SensorDeviceClass.WATER, UnitOfVolume.LITERS, lambda x: x),
}


