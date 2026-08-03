# MotionX

MotionX is a lightweight, edge-ready computer vision pipeline designed to detect objects, track their motion over time, and infer basic behaviors (such as walking, running, or loitering) directly from a video stream or webcam.

## Features

- **Object Detection**: Uses the YOLOv11 nano model for extremely fast and accurate bounding box detection.
- **Persistent Tracking**: Utilizes Ultralytics integrated trackers (like ByteTrack/BoT-SORT) to assign reliable, persistent IDs to objects across frames.
- **Motion Analysis**: Processes historical object positions to determine real-time velocity, travel direction, and idle periods.
- **Behavior Inference**: Includes a rule-based behavior engine (without heavy AI overhead) to map motion metrics to actions like "Walking", "Running", "Loitering", or "Standing".
- **Visualizations**: Real-time rendering of bounding boxes, historical motion trails, and telemetry text on the video stream.
- **CLI Interface**: A clean Typer-based command-line interface for executing the pipeline on multiple source types.

## Requirements

- Python 3.12+
- [`uv`](https://github.com/astral-sh/uv) (Extremely fast Python package installer and resolver)

## Installation

```bash
# Clone the repository
git clone https://github.com/AsithaLKonara/MotionX.git
cd MotionX

# Install dependencies using uv
uv sync
```

## Usage

You can run the tracking pipeline from the terminal using the `tracker` module.

```bash
# Run with webcam
uv run python -m tracker.cli run --source 0

# Run on a video file
uv run python -m tracker.cli run --source path/to/video.mp4

# Save output to a file
uv run python -m tracker.cli run --source 0 --save outputs/result.mp4
```

## Project Architecture

The pipeline is intentionally highly modular to allow swapping out individual components:
- `tracker.py`: Tracks object state via YOLO tracking.
- `motion.py`: Computes historical motion vectors and idle times.
- `behavior.py`: Rule-based logic engine mapping data to behavioral states.
- `visualization.py`: Handles all drawing tasks on OpenCV frames.
- `pipeline.py`: The orchestrator that coordinates the lifecycle.
- `cli.py`: Exposes commands to the user.

## Future Roadmap

- Integration with Jetson/Raspberry Pi for Edge deployment.
- Multi-camera Re-identification (ReID).
- Pose estimation and facial recognition plugins.
- REST API and Web Dashboard.
