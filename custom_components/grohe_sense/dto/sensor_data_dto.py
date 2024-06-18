from dataclasses import dataclass
from typing import List, Optional

from .measurement_guard_dto import MeasurementGuardDTO
from .withdrawals_dto import WithdrawalDTO


@dataclass
class SensorDataDTO:
    group_by: str
    # Measurements do behave (from time perspective) different from withdrawals
    measurement: List[MeasurementGuardDTO]
    withdrawals: Optional[List[WithdrawalDTO]] = None
