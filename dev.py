import subprocess
import sys

from free_port import free_port

free_port(8000)
subprocess.run([sys.executable, "-m", "fastapi", "dev", "main.py"])
