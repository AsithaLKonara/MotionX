from dataclasses import dataclass, field
from typing import Tuple, List
import time

@dataclass
class TrackedObject:
    id: int
    class_name: str
    confidence: float
    bbox: Tuple[int, int, int, int]  # x1, y1, x2, y2
    center: Tuple[int, int]
    velocity: float = 0.0
    direction: str = "unknown"
    history: List[Tuple[int, int]] = field(default_factory=list)
    last_seen: float = field(default_factory=time.time)
    status: str = "Unknown"
    idle_time: float = 0.0
