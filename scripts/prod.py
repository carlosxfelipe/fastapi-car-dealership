import os

if __name__ == "__main__":
    # Using a reasonable fixed number of workers instead of all available cores
    workers = "4"

    print(f"Starting uvicorn in production mode with {workers} workers...")
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
