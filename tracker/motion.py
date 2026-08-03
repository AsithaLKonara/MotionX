from typing import List
from .data_model import TrackedObject
from .utils import calculate_distance

class MotionAnalyzer:
    def __init__(self, fps: float = 30.0):
        self.fps = fps
        
    def analyze(self, objects: List[TrackedObject]) -> None:
        for obj in objects:
            if len(obj.history) < 2:
                obj.velocity = 0.0
                obj.direction = "Unknown"
                obj.idle_time += 1.0 / self.fps
                continue
                
            # Calculate distance between last two points
            p1 = obj.history[-2]
            p2 = obj.history[-1]
            dist = calculate_distance(p1, p2)
            
            # Simple speed proxy (pixels per frame)
            speed = dist
            
            # Smooth velocity with exponential moving average
            obj.velocity = (obj.velocity * 0.7) + (speed * 0.3)
            
            if obj.velocity < 1.0:
                obj.idle_time += 1.0 / self.fps
            else:
                obj.idle_time = 0.0
                
            # Direction calculation
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            
            if obj.velocity >= 1.0:
                if abs(dx) > abs(dy):
                    if dx > 0:
                        obj.direction = "East"
                    else:
                        obj.direction = "West"
                else:
                    if dy > 0:
                        obj.direction = "South" # OpenCV y-axis goes down
                    else:
                        obj.direction = "North"
