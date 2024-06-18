from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class MeasurementSenseDTO:
    date: datetime | str
    temperature: float
    humidity: float

