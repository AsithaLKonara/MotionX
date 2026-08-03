from typing import List
from .data_model import TrackedObject

class BehaviorEngine:
    def __init__(self, run_speed_threshold: float = 10.0, loiter_time_threshold: float = 5.0):
        self.run_speed_threshold = run_speed_threshold
        self.loiter_time_threshold = loiter_time_threshold
        
    def infer(self, objects: List[TrackedObject]) -> None:
        for obj in objects:
            if obj.idle_time > self.loiter_time_threshold:
                obj.status = "Loitering" if obj.class_name == "person" else "Idle"
            elif obj.velocity > self.run_speed_threshold:
                obj.status = "Running" if obj.class_name == "person" else "Fast Moving"
            elif obj.velocity >= 1.0:
                obj.status = "Walking" if obj.class_name == "person" else "Moving"
            else:
                obj.status = "Standing" if obj.class_name == "person" else "Stopped"
