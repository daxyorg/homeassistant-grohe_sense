import datetime
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import List, Optional, Union

from homeassistant.components.persistent_notification import Notification


@dataclass_json
@dataclass
class Address:
    street: str
    city: str
    zipcode: str
    housenumber: str
    country: str
    country_code: str
    additionalInfo: str
    state: str


@dataclass_json
@dataclass
class Threshold:
    type: str
    value: int
    enabled: bool
    quantity: str


@dataclass_json
@dataclass
class Status:
    type: str
    value: int


@dataclass_json
@dataclass
class Measurement:
    timestamp: str
    temperature: Optional[float] = None
    humidity: Optional[int] = None
    flow_rate: Optional[float] = None
    pressure: Optional[float] = None
    temperature_guard: Optional[float] = None
    battery: Optional[int] = None


@dataclass_json
@dataclass
class AverageMeasurements:
    temperature: int
    humidity: int


@dataclass_json
@dataclass
class DataLatest:
    measurement: Measurement
    average_measurements: Optional[AverageMeasurements] = None


@dataclass_json
@dataclass
class PressureCurve:
    fr: float
    pr: float
    tp: int


@dataclass_json
@dataclass
class LastPressureMeasurement:
    id: str
    status: str
    estimated_time_of_completion: str
    start_time: str
    leakage: bool
    level: int
    total_duration: int
    drop_of_pressure: float
    error_message: str
    pressure_curve: List[PressureCurve]


@dataclass_json
@dataclass
class Installer:
    name: str
    email: str
    phone: str


@dataclass_json
@dataclass
class Command:
    temp_user_unlock_on: bool
    reason_for_change: int
    pressure_measurement_running: bool
    buzzer_on: bool
    buzzer_sound_profile: int
    valve_open: bool
    measure_now: bool


@dataclass_json
@dataclass
class ApplianceCommand:
    appliance_id: str
    type: int
    command: Command
    commandb64: str
    timestamp: str


@dataclass_json
@dataclass
class Config:
    thresholds: List[Threshold]
    measurement_period: Optional[int] = None
    action_on_major_leakage: Optional[int] = None
    action_on_minor_leakage: Optional[int] = None
    action_on_micro_leakage: Optional[int] = None
    monitor_frost_alert: Optional[bool] = None
    monitor_lower_flow_limit: Optional[bool] = None
    monitor_upper_flow_limit: Optional[bool] = None
    monitor_lower_pressure_limit: Optional[bool] = None
    monitor_upper_pressure_limit: Optional[bool] = None
    monitor_lower_temperature_limit: Optional[bool] = None
    monitor_upper_temperature_limit: Optional[bool] = None
    monitor_major_leakage: Optional[bool] = None
    monitor_minor_leakage: Optional[bool] = None
    monitor_micro_leakage: Optional[bool] = None
    monitor_system_error: Optional[bool] = None
    monitor_btw_0_1_and_0_8_leakage: Optional[bool] = None
    monitor_withdrawel_amount_limit_breach: Optional[bool] = None
    detection_interval: Optional[int] = None
    impulse_ignore: Optional[int] = None
    time_ignore: Optional[int] = None
    pressure_tolerance_band: Optional[int] = None
    pressure_drop: Optional[int] = None
    detection_time: Optional[int] = None
    action_on_btw_0_1_and_0_8_leakage: Optional[int] = None
    action_on_withdrawel_amount_limit_breach: Optional[int] = None
    withdrawel_amount_limit: Optional[int] = None
    sprinkler_mode_active_monday: Optional[bool] = None
    sprinkler_mode_active_tuesday: Optional[bool] = None
    sprinkler_mode_active_wednesday: Optional[bool] = None
    sprinkler_mode_active_thursday: Optional[bool] = None
    sprinkler_mode_active_friday: Optional[bool] = None
    sprinkler_mode_active_saturday: Optional[bool] = None
    sprinkler_mode_active_sunday: Optional[bool] = None
    sprinkler_mode_start_time: Optional[int] = None
    sprinkler_mode_stop_time: Optional[int] = None
    measurement_transmission_intervall: Optional[int] = None
    measurement_transmission_intervall_offset: Optional[int] = None

@dataclass_json
@dataclass
class Appliance:
    appliance_id: str
    installation_date: str
    name: str
    serial_number: str
    type: int
    version: str
    tdt: str
    timezone: int
    config: Config
    role: str
    registration_complete: bool
    calculate_average_since: Optional[str] = None
    pressure_notification: Optional[bool] = None
    snooze_status: Optional[str] = None
    last_pressure_measurement: Optional[LastPressureMeasurement] = None
    installer: Optional[Installer] = None
    command: Optional[Command] = None
    notifications: Optional[List[Notification]] = None
    status: Optional[List[Status]] = None
    data_latest: Optional[DataLatest] = None


@dataclass_json
@dataclass
class Room:
    id: int
    name: str
    type: int
    room_type: int
    role: str
    appliances: Optional[List[Appliance]] = None


@dataclass_json
@dataclass
class Location:
    id: int
    name: str
    type: int
    role: str
    timezone: str
    water_cost: float
    energy_cost: float
    heating_type: int
    currency: str
    default_water_cost: float
    default_energy_cost: float
    default_heating_type: int
    emergency_shutdown_enable: bool
    address: Address
    rooms: Optional[List[Room]] = None


@dataclass_json
@dataclass
class Locations:
    locations: List[Location]


@dataclass_json
@dataclass
class Notification:
    appliance_id: str
    id: str
    category: int
    is_read: bool
    timestamp: str
    type: int
    threshold_quantity: str
    threshold_type: str


@dataclass_json
@dataclass
class Measurement:
    date: str
    flowrate: Optional[float]
    pressure: Optional[float]
    temperature_guard: Optional[float]
    temperature: Optional[float]
    humidity: Optional[float]


@dataclass_json
@dataclass
class Withdrawal:
    date: Union[datetime, str]
    waterconsumption: float
    hotwater_share: float
    water_cost: float
    energy_cost: float


@dataclass_json
@dataclass
class Data:
    group_by: str
    measurement: List[Measurement]
    withdrawals: List[Withdrawal]


@dataclass_json
@dataclass
class MeasurementData:
    appliance_id: str
    type: int
    data: Data
