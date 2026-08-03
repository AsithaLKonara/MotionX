from typing import List
import cv2
import numpy as np
from .data_model import TrackedObject

class Visualizer:
    def __init__(self):
        self.bbox_color = (0, 255, 0) # Green
        self.trail_color = (255, 0, 0) # Blue
        self.text_color = (0, 255, 255) # Yellow
        
    def draw(self, frame: np.ndarray, objects: List[TrackedObject]) -> np.ndarray:
        out_frame = frame.copy()
        
        for obj in objects:
            x1, y1, x2, y2 = obj.bbox
            
            # Draw bounding box
            cv2.rectangle(out_frame, (x1, y1), (x2, y2), self.bbox_color, 2)
            
            # Draw trail
            if len(obj.history) > 1:
                pts = np.array(obj.history, np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(out_frame, [pts], isClosed=False, color=self.trail_color, thickness=2)
                
            # Draw text
            text = f"ID:{obj.id} {obj.class_name} | {obj.status} | Spd:{obj.velocity:.1f} | Dir:{obj.direction}"
            cv2.putText(out_frame, text, (x1, max(0, y1 - 10)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.text_color, 2)
                        
        return out_frame
