import typer
from rich.console import Console
from .pipeline import Pipeline

app = typer.Typer(help="MotionX Computer Vision Tracker")
console = Console()

@app.command()
def run(
    source: str = typer.Option("0", "--source", "-s", help="Video source (webcam ID, RTSP URL, or file path)"),
    model: str = typer.Option("yolo11n.pt", "--model", "-m", help="YOLO model path or name"),
    save: str = typer.Option(None, "--save", help="Path to save output video (e.g. output.mp4)"),
    show: bool = typer.Option(True, "--show/--no-show", help="Show video preview window")
):
    """Run the tracking pipeline on a video source."""
    console.print(f"[bold green]Starting MotionX Tracker[/bold green]")
    console.print(f"Source: {source}")
    console.print(f"Model: {model}")
    
    pipeline = Pipeline(model_name=model)
    pipeline.run(source=source, show=show, save_path=save)
    
@app.command()
def stats():
    """Show tracker statistics."""
    console.print("[bold blue]Tracker Statistics[/bold blue]")
    console.print("Not yet implemented for the MVP.")

if __name__ == "__main__":
    app()
