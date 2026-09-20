PROFILES = {
    "Eco": {
        "priority": "above_normal",
        "description": "Lower-impact mode for weaker PCs.",
        "power_plan": False,
    },
    "Balanced": {
        "priority": "high",
        "description": "Recommended for most gaming PCs.",
        "power_plan": False,
    },
    "Competitive": {
        "priority": "high",
        "description": "High-focus profile for stronger systems.",
        "power_plan": True,
    },
}

def get_profile(name):
    return PROFILES.get(name, PROFILES["Balanced"])

def recommend_profile(info):
    total_ram = float(info.get("memory_total_gb", 0))
    threads = int(info.get("cpu_threads", 1))
    if total_ram >= 16 and threads >= 8:
        return "Competitive"
    if total_ram >= 8 and threads >= 4:
        return "Balanced"
    return "Eco"
