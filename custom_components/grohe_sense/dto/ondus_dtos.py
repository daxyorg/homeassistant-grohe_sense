from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import List, Optional

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
    quantity: str
    type: str
    value: int
    enabled: bool


@dataclass_json
@dataclass
class Status:
    type: str
    value: int


@dataclass_json
@dataclass
class Measurement:
    battery: int
    humidity: int
    temperature: float
    timestamp: str


@dataclass_json
@dataclass
class AverageMeasurements:
    temperature: int
    humidity: int


@dataclass_json
@dataclass
class DataLatest:
    measurement: Measurement
    average_measurements: AverageMeasurements


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
class Appliance:
    appliance_id: str
    installation_date: str
    name: str
    serial_number: str
    type: int
    version: str
    tdt: str
    timezone: int
    config: Threshold
    role: str
    registration_complete: bool
    calculate_average_since: Optional[str]
    pressure_notification: Optional[bool]
    snooze_status: Optional[str]
    last_pressure_measurement: Optional[LastPressureMeasurement]
    installer: Optional[Installer]
    command: Optional[Command]
    notifications: Optional[List[Notification]]
    status: Optional[List[Status]]
    data_latest: Optional[DataLatest]


@dataclass_json
@dataclass
class Room:
    id: int
    name: str
    type: int
    room_type: int
    role: str
    appliances: List[Appliance]


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
    rooms: Optional[List[Room]]


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
    flowrate: float
    pressure: float
    temperature_guard: float


@dataclass_json
@dataclass
class Withdrawal:
    date: str
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
