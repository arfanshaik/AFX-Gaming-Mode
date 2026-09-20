import platform
import subprocess
import time
from pathlib import Path

import psutil

from app.windows_tools import set_power_plan

def _set_priority(pid, priority):
    try:
        proc = psutil.Process(pid)
        if platform.system() == "Windows":
            if priority == "high":
                proc.nice(psutil.HIGH_PRIORITY_CLASS)
            else:
                proc.nice(psutil.ABOVE_NORMAL_PRIORITY_CLASS)
        return True, "Game process priority updated."
    except Exception as exc:
        return False, f"Priority change skipped: {exc}"

def launch_game(path, profile, use_high_performance_power=False):
    exe = Path(path)
    if not exe.exists():
        return None, f"Game executable not found: {exe}"

    notes = []

    if use_high_performance_power:
        _, msg = set_power_plan(True)
        notes.append(msg)

    try:
        process = subprocess.Popen([str(exe)], cwd=str(exe.parent))
    except Exception as exc:
        return None, f"Failed to launch game: {exc}"

    time.sleep(0.8)
    _, msg = _set_priority(process.pid, profile.get("priority", "high"))
    notes.append(msg)

    return process, "\n".join([f"Launched {exe.name}."] + notes)

def wait_for_exit(process):
    try:
        return process.wait()
    except Exception:
        return None
