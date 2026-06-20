import platform
import subprocess
import time


def free_port(port: int):
    system = platform.system()

    if system in ("Darwin", "Linux"):
        try:
            result = subprocess.run(
                ["sh", "-c", f"lsof -ti :{port}"],
                capture_output=True,
                text=True,
            )
            output = result.stdout.strip()

            if output:
                pids = output.split("\n")
                for pid in pids:
                    if pid:
                        print(
                            f"Port {port} is in use by PID {pid}. Forcing termination..."
                        )
                        subprocess.run(["kill", "-9", pid])
                        print(f"Process {pid} terminated.")
                        time.sleep(0.5)
        except Exception as e:
            print(f"Warning: Error while trying to free port {port}: {e}")

    elif system == "Windows":
        try:
            result = subprocess.run(
                ["cmd", "/c", f"netstat -ano | findstr :{port}"],
                capture_output=True,
                text=True,
            )
            output = result.stdout.strip()

            if output:
                lines = output.split("\n")
                for line in lines:
                    parts = line.strip().split()
                    if len(parts) >= 5:
                        pid = parts[-1]
                        if pid != "0" and pid:
                            print(
                                f"Port {port} is in use by PID {pid}. Forcing termination on Windows..."
                            )
                            subprocess.run(["taskkill", "/F", "/PID", pid])
                            print(f"Process {pid} terminated.")
                            time.sleep(0.5)
        except Exception as e:
            print(f"Warning: Error while trying to free port {port} on Windows: {e}")
