import argparse
from app.monitor import system_snapshot
from app.profiles import recommend_profile

def diagnose():
    info = system_snapshot()
    print("AFX Gaming Mode - Diagnostics")
    print("=" * 31)
    print(f"CPU usage: {info['cpu_percent']}%")
    print(f"RAM usage: {info['memory_percent']}%")
    print(f"RAM total: {info['memory_total_gb']} GB")
    print(f"CPU threads: {info['cpu_threads']}")
    print(f"Suggested profile: {recommend_profile(info)}")

def main():
    parser = argparse.ArgumentParser(description="AFX Gaming Mode")
    parser.add_argument("--diagnose", action="store_true", help="Run gaming diagnostics")
    args = parser.parse_args()

    if args.diagnose:
        diagnose()
        return

    from app.ui import GamingModeApp
    GamingModeApp().run()

if __name__ == "__main__":
    main()
