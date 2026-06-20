import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from free_port import free_port

if __name__ == "__main__":
    free_port(8000)

    # Using a reasonable fixed number of workers instead of all available cores
    workers = "4"

    print(f"Starting uvicorn via CLI with {workers} workers...")
    os.execvp(
        "uvicorn",
        [
            "uvicorn",
            "app.main:app",
            "--host",
            "0.0.0.0",
            "--port",
            "8000",
            "--workers",
            workers,
        ],
    )
