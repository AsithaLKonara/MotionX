import cv2
from loguru import logger
from .tracker import ObjectTracker
from .motion import MotionAnalyzer
from .behavior import BehaviorEngine
from .visualization import Visualizer

class Pipeline:
    def __init__(self, model_name: str = "yolo11n.pt", fps: float = 30.0):
        self.tracker = ObjectTracker(model_name=model_name)
        self.motion_analyzer = MotionAnalyzer(fps=fps)
        self.behavior_engine = BehaviorEngine()
        self.visualizer = Visualizer()
        
    def run(self, source: str, show: bool = True, save_path: str = None):
        try:
            source_id = int(source)
            cap = cv2.VideoCapture(source_id)
        except ValueError:
            cap = cv2.VideoCapture(source)
            
        if not cap.isOpened():
            logger.error(f"Failed to open video source: {source}")
            return
            
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps <= 0:
            fps = 30.0
            
        self.motion_analyzer.fps = fps
        
        out = None
        if save_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(save_path, fourcc, fps, (width, height))
            
        logger.info(f"Starting pipeline on source: {source}")
        frame_idx = 0
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                    
                frame_idx += 1
                
                # Tracking
                objects = self.tracker.process_frame(frame)
                
                # Analysis
                self.motion_analyzer.analyze(objects)
                self.behavior_engine.infer(objects)
                
                # Visualization
                vis_frame = self.visualizer.draw(frame, objects)
                
                # Save
                if out:
                    out.write(vis_frame)
                    
                # Show
                if show:
                    cv2.imshow("MotionX Tracker", vis_frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                        
                # CLI Output
                if frame_idx % int(fps) == 0:
                    print(f"--- Frame {frame_idx} ---")
                    for obj in objects:
                        print(f"ID:{obj.id} {obj.class_name.capitalize()} | {obj.status} | Spd:{obj.velocity:.1f} | Pos:{obj.center}")
                        
        except KeyboardInterrupt:
            logger.info("Pipeline stopped by user.")
        finally:
            cap.release()
            if out:
                out.release()
            cv2.destroyAllWindows()
            logger.info("Pipeline finished.")
