from dataclasses import dataclass
from typing import Optional


@dataclass
class MeasurementDto:
    flow_rate: Optional[float] = None
    pressure: Optional[float] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass
class CoordinatorDto:
    notification: Optional[str] = None
    measurement: Optional[MeasurementDto] = None
    withdrawal: Optional[float] = None
