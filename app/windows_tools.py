import os
import platform
import subprocess

HIGH_PERFORMANCE = "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"
BALANCED = "381b4222-f694-41f0-9685-ff5bb260df2e"

def set_power_plan(high_performance=True):
    if platform.system() != "Windows":
        return False, "Power plan control is available only on Windows."

    guid = HIGH_PERFORMANCE if high_performance else BALANCED
    try:
        result = subprocess.run(
            ["powercfg", "/setactive", guid],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            return True, "Power plan updated."
        return False, (result.stderr or result.stdout or "Power plan change failed.").strip()
    except Exception as exc:
        return False, str(exc)

def open_game_mode_settings():
    if platform.system() != "Windows":
        return False, "Windows Game Mode settings are available only on Windows."
    try:
        os.startfile("ms-settings:gaming-gamemode")
        return True, "Opened Windows Game Mode settings."
    except Exception as exc:
        return False, str(exc)

def open_task_manager():
    if platform.system() != "Windows":
        return False, "Task Manager is available only on Windows."
    try:
        subprocess.Popen(["taskmgr.exe"])
        return True, "Task Manager opened."
    except Exception as exc:
        return False, str(exc)
