from typing import Dict, List
import time
from ultralytics import YOLO
from .data_model import TrackedObject
from .utils import calculate_center

class ObjectTracker:
    def __init__(self, model_name: str = "yolo11n.pt"):
        self.model = YOLO(model_name)
        self.tracked_objects: Dict[int, TrackedObject] = {}
        
    def process_frame(self, frame) -> List[TrackedObject]:
        # Perform tracking (which includes detection)
        results = self.model.track(frame, persist=True, verbose=False)
        result = results[0]
        
        current_ids = set()
        
        if result.boxes is not None and result.boxes.id is not None:
            boxes = result.boxes.xyxy.cpu().numpy()
            track_ids = result.boxes.id.int().cpu().tolist()
            confs = result.boxes.conf.cpu().tolist()
            class_ids = result.boxes.cls.int().cpu().tolist()
            
            for box, track_id, conf, cls_id in zip(boxes, track_ids, confs, class_ids):
                current_ids.add(track_id)
                x1, y1, x2, y2 = map(int, box)
                bbox = (x1, y1, x2, y2)
                center = calculate_center(bbox)
                class_name = result.names[cls_id]
                
                if track_id in self.tracked_objects:
                    obj = self.tracked_objects[track_id]
                    obj.bbox = bbox
                    obj.center = center
                    obj.confidence = conf
                    obj.history.append(center)
                    # Limit history size to prevent memory leak and keep recent motion
                    if len(obj.history) > 90:
                        obj.history.pop(0)
                    obj.last_seen = time.time()
                else:
                    self.tracked_objects[track_id] = TrackedObject(
                        id=track_id,
                        class_name=class_name,
                        confidence=conf,
                        bbox=bbox,
                        center=center,
                        history=[center],
                        last_seen=time.time()
                    )
                    
        # Optional: cleanup objects not seen for > 5 seconds
        current_time = time.time()
        to_delete = [tid for tid, obj in self.tracked_objects.items() if current_time - obj.last_seen > 5.0]
        for tid in to_delete:
            del self.tracked_objects[tid]
            
        return [self.tracked_objects[tid] for tid in current_ids if tid in self.tracked_objects]
