from dataclasses import dataclass

from custom_components.grohe_sense.enum.ondus_types import GroheTypes


@dataclass
class GroheDeviceDTO:
    locationId: int
    roomId: int
    applianceId: str
    type: GroheTypes
    name: str
