from dataclasses import dataclass
from datetime import datetime


@dataclass
class WithdrawalDTO:
    date: datetime | str
    waterconsumption: float
    hotwater_share: float
    water_cost: float
    energy_cost: float


