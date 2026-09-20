import psutil

def system_snapshot():
    memory = psutil.virtual_memory()
    return {
        "cpu_percent": psutil.cpu_percent(interval=0.15),
        "memory_percent": memory.percent,
        "memory_total_gb": round(memory.total / (1024 ** 3), 1),
        "memory_available_gb": round(memory.available / (1024 ** 3), 1),
        "cpu_threads": psutil.cpu_count(logical=True) or 1,
    }

def heavy_background_processes(exclude_pids=None, limit=8):
    exclude = set(exclude_pids or [])
    rows = []

    for proc in psutil.process_iter(["pid", "name", "memory_percent", "cpu_percent"]):
        try:
            if proc.info["pid"] in exclude:
                continue
            rows.append({
                "pid": proc.info["pid"],
                "name": proc.info["name"] or "Unknown",
                "memory_percent": round(proc.info["memory_percent"] or 0.0, 1),
                "cpu_percent": round(proc.info["cpu_percent"] or 0.0, 1),
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    rows.sort(key=lambda x: (x["memory_percent"], x["cpu_percent"]), reverse=True)
    return rows[:limit]
