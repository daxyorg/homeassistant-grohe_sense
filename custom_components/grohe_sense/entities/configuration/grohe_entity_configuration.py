from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Callable

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import UnitOfTemperature, PERCENTAGE, UnitOfVolumeFlowRate, UnitOfPressure, UnitOfVolume, \
    UnitOfTime

from custom_components.grohe_sense.enum.ondus_types import GroheTypes


class SensorTypes(Enum):
    TEMPERATURE = 'temperature'
    HUMIDITY = 'humidity'
    FLOW_RATE = 'flow_rate'
    PRESSURE = 'pressure'
    NOTIFICATION = 'notification'
    WATER_CONSUMPTION = 'water_consumption'
    # Sensors for Grohe BLUE
    CLEANING_COUNT = 'cleaning_count'
    DATE_OF_CLEANING = 'date_of_cleaning'
    DATE_OF_CO2_REPLACEMENT = 'date_of_co2_replacement'
    DATE_OF_FILTER_REPLACEMENT = 'date_of_filter_replacement'
    FILTER_CHANGE_COUNT = 'filter_change_count'
    MAX_IDLE_TIME = 'max_idle_time'
    OPEN_CLOSE_CYCLES_CARBONATED = 'open_close_cycles_carbonated'
    OPEN_CLOSE_CYCLES_STILL = 'open_close_cycles_still'
    OPERATING_TIME = 'operating_time'
    POWER_CUT_COUNT = 'power_cut_count'
    PUMP_COUNT = 'pump_count'
    PUMP_RUNNING_TIME = 'pump_running_time'
    REMAINING_CO2 = 'remaining_co2'
    REMAINING_FILTER = 'remaining_filter'
    TIME_SINCE_LAST_WITHDRAWAL = 'time_since_last_withdrawal'
    TIME_SINCE_RESTART = 'time_since_restart'
    TIME_OFFSET = 'time_offset'
    WATER_RUNNING_TIME_CARBONATED = 'water_running_time_carbonated'
    WATER_RUNNING_TIME_MEDIUM = 'water_running_time_medium'
    WATER_RUNNING_TIME_STILL = 'water_running_time_still'
    REMAINING_FILTER_LITERS = 'remaining_filter_liters'
    REMAINING_CO2_LITERS = 'remaining_co2_liters'


@dataclass
class Sensor:
    device_class: SensorDeviceClass | None
    unit_of_measurement: str | None
    function: Callable[[float], float]


GROHE_ENTITY_CONFIG: Dict[GroheTypes, List[SensorTypes]] = {
    GroheTypes.GROHE_SENSE: [SensorTypes.TEMPERATURE,
                             SensorTypes.HUMIDITY,
                             SensorTypes.NOTIFICATION
                             ],
    GroheTypes.GROHE_SENSE_GUARD: [SensorTypes.TEMPERATURE,
                                   SensorTypes.FLOW_RATE,
                                   SensorTypes.PRESSURE,
                                   SensorTypes.NOTIFICATION,
                                   SensorTypes.WATER_CONSUMPTION
                                   ],
    GroheTypes.GROHE_BLUE_PROFESSIONAL: [SensorTypes.NOTIFICATION,
                                         SensorTypes.CLEANING_COUNT,
                                         SensorTypes.DATE_OF_CLEANING,
                                         SensorTypes.DATE_OF_CO2_REPLACEMENT,
                                         SensorTypes.DATE_OF_FILTER_REPLACEMENT,
                                         SensorTypes.FILTER_CHANGE_COUNT,
                                         SensorTypes.MAX_IDLE_TIME,
                                         SensorTypes.OPEN_CLOSE_CYCLES_CARBONATED,
                                         SensorTypes.OPEN_CLOSE_CYCLES_STILL,
                                         SensorTypes.OPERATING_TIME,
                                         SensorTypes.POWER_CUT_COUNT,
                                         SensorTypes.PUMP_COUNT,
                                         SensorTypes.PUMP_RUNNING_TIME,
                                         SensorTypes.REMAINING_CO2,
                                         SensorTypes.REMAINING_FILTER,
                                         SensorTypes.TIME_SINCE_LAST_WITHDRAWAL,
                                         SensorTypes.TIME_SINCE_RESTART,
                                         SensorTypes.WATER_RUNNING_TIME_CARBONATED,
                                         SensorTypes.WATER_RUNNING_TIME_MEDIUM,
                                         SensorTypes.WATER_RUNNING_TIME_STILL,
                                         SensorTypes.REMAINING_FILTER_LITERS,
                                         SensorTypes.REMAINING_CO2_LITERS,
                                         ]
}

SENSOR_CONFIGURATION: Dict[SensorTypes, Sensor] = {
    SensorTypes.TEMPERATURE: Sensor(SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS, lambda x: x),
    SensorTypes.HUMIDITY: Sensor(SensorDeviceClass.HUMIDITY, PERCENTAGE, lambda x: x),
    SensorTypes.FLOW_RATE: Sensor(SensorDeviceClass.VOLUME_FLOW_RATE, UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR,
                                  lambda x: x * 3.6),
    SensorTypes.PRESSURE: Sensor(SensorDeviceClass.PRESSURE, UnitOfPressure.BAR, lambda x: x),
    SensorTypes.WATER_CONSUMPTION: Sensor(SensorDeviceClass.WATER, UnitOfVolume.LITERS, lambda x: x),
    # From here Blue Sensors are configured
    SensorTypes.CLEANING_COUNT: Sensor(None, UnitOfVolume.LITERS, lambda x: x),
    SensorTypes.DATE_OF_CLEANING: Sensor(SensorDeviceClass.TIMESTAMP, None, lambda x: x),
    SensorTypes.DATE_OF_CO2_REPLACEMENT: Sensor(SensorDeviceClass.TIMESTAMP, None, lambda x: x),
    SensorTypes.DATE_OF_FILTER_REPLACEMENT: Sensor(SensorDeviceClass.TIMESTAMP, None, lambda x: x),
    SensorTypes.FILTER_CHANGE_COUNT: Sensor(None, None, lambda x: x),
    SensorTypes.MAX_IDLE_TIME: Sensor(SensorDeviceClass.DURATION, UnitOfTime.MINUTES, lambda x: x),
    SensorTypes.OPEN_CLOSE_CYCLES_CARBONATED: Sensor(None, None, lambda x: x),
    SensorTypes.OPEN_CLOSE_CYCLES_STILL: Sensor(None, None, lambda x: x),
    SensorTypes.OPERATING_TIME: Sensor(SensorDeviceClass.DURATION, UnitOfTime.MINUTES, lambda x: x),
    SensorTypes.POWER_CUT_COUNT: Sensor(None, None, lambda x: x),
    SensorTypes.PUMP_COUNT: Sensor(None, None, lambda x: x),
    SensorTypes.PUMP_RUNNING_TIME: Sensor(SensorDeviceClass.DURATION, UnitOfTime.MINUTES, lambda x: x),
    SensorTypes.REMAINING_CO2: Sensor(SensorDeviceClass.BATTERY, PERCENTAGE, lambda x: x),
    SensorTypes.REMAINING_FILTER: Sensor(SensorDeviceClass.BATTERY, PERCENTAGE, lambda x: x),
    SensorTypes.TIME_SINCE_LAST_WITHDRAWAL: Sensor(SensorDeviceClass.DURATION, UnitOfTime.MINUTES, lambda x: x),
    SensorTypes.TIME_SINCE_RESTART: Sensor(SensorDeviceClass.DURATION, UnitOfTime.MINUTES, lambda x: x),
    SensorTypes.TIME_OFFSET: Sensor(SensorDeviceClass.DURATION, UnitOfTime.MINUTES, lambda x: x),
    SensorTypes.WATER_RUNNING_TIME_CARBONATED: Sensor(SensorDeviceClass.DURATION, UnitOfTime.MINUTES, lambda x: x),
    SensorTypes.WATER_RUNNING_TIME_MEDIUM: Sensor(SensorDeviceClass.DURATION, UnitOfTime.MINUTES, lambda x: x),
    SensorTypes.WATER_RUNNING_TIME_STILL: Sensor(SensorDeviceClass.DURATION, UnitOfTime.MINUTES, lambda x: x),
    SensorTypes.REMAINING_FILTER_LITERS: Sensor(SensorDeviceClass.VOLUME, UnitOfVolume.LITERS, lambda x: x),
    SensorTypes.REMAINING_CO2_LITERS: Sensor(SensorDeviceClass.VOLUME, UnitOfVolume.LITERS, lambda x: x),
}


