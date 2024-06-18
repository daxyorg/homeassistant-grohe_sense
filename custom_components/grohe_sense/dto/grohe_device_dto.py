from dataclasses import dataclass

from ..enum.grohe_types import GroheTypes


@dataclass
class GroheDeviceDTO:
    locationId: int
    roomId: int
    applianceId: str
    type: GroheTypes
    name: str
