from dataclasses import dataclass
from datetime import datetime


@dataclass
class MeasurementGuardDTO:
    date: datetime | str
    flowrate: float
    pressure: float
    temperature_guard: float
