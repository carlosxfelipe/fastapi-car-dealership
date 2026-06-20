import sys
from multiprocessing import cpu_count
from pathlib import Path

import uvicorn

sys.path.insert(0, str(Path(__file__).resolve().parent))
from free_port import free_port

if __name__ == "__main__":
    free_port(8000)
    workers = max(1, min(4, cpu_count()))

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        workers=workers,
        reload=False,
    )
