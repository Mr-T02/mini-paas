import subprocess
import sys

def list_apps():
    result = subprocess.run(
        ["docker", "ps", "-a", "--format", "{{.Names}}|{{.Status}}|{{.Ports}}"], 
        capture_output=True, text=True
    )
    lines = result.stdout.strip().split("\n")
    print(f"{'NAME':<25} {'STATUS':<25} {'PORTS'}")
    print("-" * 70)
    for line in lines:
        if not line:
            continue
        parts = line.split("|")
        name = parts[0].strip()
        status = parts[1].strip()
        ports = parts[2].strip() if len(parts) > 2 else "-" 
        print(f"{name:<25} {status:<25} {ports}")

def show_logs(app_name):
    result = subprocess.run(
        ["docker", "logs", "--tail", "50", app_name],
        capture_output=True, text=True
    )
    print(f"Logs for {app_name}:\n")
    print(result.stdout)
    if result.stderr:
        print(result.stderr)

def start_app(app_name):
    result = subprocess.run(
            ["docker", "start", app_name],
            capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"✅ Started {app_name}")
    else:
        print(f"⚠️ Could not start {app_name}: {result.stderr.strip()}")

def stop_app(app_name):
    result = subprocess.run(
        ["docker", "stop", app_name],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"✅ Stopped {app_name}")
    else:
        print(f"Could not stop {app_name}: {result.stderr.strip()}")  

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python paas.py [list|logs|stop] <app_name>")
        sys.exit(1)

    command = sys.argv[1]

    if command == "list":
        list_apps()
    elif command == "logs":
        if len(sys.argv) < 3:
            print("Usage: python paas.py logs <app_name>")
        else:
            show_logs(sys.argv[2])
    elif command == "stop":
        if len(sys.argv) < 3:
            print("Usage: python paas.py stop <app_name>")
        else:
            stop_app(sys.argv[2])
    elif command == "start":
        if len(sys.argv) < 3:
            print("Usage: python paas.py start <app_name>")
        else:
            start_app(sys.argv[2])
    else:
        print(f"Unknown command: {command}")












