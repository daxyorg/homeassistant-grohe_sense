from dataclasses import dataclass
from datetime import datetime


@dataclass
class NotificationDto:
    appliance_id: str
    id: str
    category: int
    is_read: bool
    timestamp: str
    type: int
    threshold_quantity: str
    threshold_type: str
