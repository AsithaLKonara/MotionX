import pytest
import time
from tracker.data_model import TrackedObject
from tracker.motion import MotionAnalyzer
from tracker.behavior import BehaviorEngine

def test_motion_analysis_idle():
    obj = TrackedObject(
        id=1,
        class_name="person",
        confidence=0.9,
        bbox=(0, 0, 10, 10),
        center=(5, 5),
        history=[(5, 5), (5, 5)]  # Not moving
    )
    
    analyzer = MotionAnalyzer(fps=30)
    analyzer.analyze([obj])
    
    assert obj.velocity < 1.0
    assert obj.idle_time > 0
    assert obj.direction == "Unknown" or obj.direction == "North" or obj.direction == "South"

def test_motion_analysis_moving_east():
    obj = TrackedObject(
        id=2,
        class_name="person",
        confidence=0.9,
        bbox=(0, 0, 10, 10),
        center=(10, 5),
        history=[(0, 5), (10, 5)]  # Moving right (East)
    )
    
    analyzer = MotionAnalyzer(fps=30)
    analyzer.analyze([obj])
    
    assert obj.velocity > 1.0
    assert obj.idle_time == 0.0
    assert obj.direction == "East"

def test_behavior_engine():
    # Idle person
    obj1 = TrackedObject(
        id=1, class_name="person", confidence=0.9, bbox=(0,0,10,10), center=(5,5),
        velocity=0.0, idle_time=10.0
    )
    
    # Running person
    obj2 = TrackedObject(
        id=2, class_name="person", confidence=0.9, bbox=(0,0,10,10), center=(5,5),
        velocity=15.0, idle_time=0.0
    )
    
    engine = BehaviorEngine(run_speed_threshold=10.0, loiter_time_threshold=5.0)
    engine.infer([obj1, obj2])
    
    assert obj1.status == "Loitering"
    assert obj2.status == "Running"
