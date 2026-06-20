import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from free_port import free_port

free_port(8000)
subprocess.run([sys.executable, "-m", "fastapi", "dev", "app/main.py"])
