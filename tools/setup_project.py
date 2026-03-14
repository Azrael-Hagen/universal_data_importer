from pathlib import Path
import json

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PACKAGE_DIRS = [
    "core",
    "plugins",
    "loaders",
    "gui",
    "utils",
    "tools",
    "config",
]

VSCODE_DIR = PROJECT_ROOT / ".vscode"
LAUNCH_FILE = VSCODE_DIR / "launch.json"


def ensure_init_files():
    print("Checking __init__.py files...\n")

    for package in PACKAGE_DIRS:
        package_path = PROJECT_ROOT / package
        init_file = package_path / "__init__.py"

        if not package_path.exists():
            continue

        if not init_file.exists():
            init_file.touch()
            print(f"Created: {init_file}")
        else:
            print(f"Exists: {init_file}")


def ensure_vscode_launch():
    print("\nSetting up VSCode launch configuration...\n")

    if not VSCODE_DIR.exists():
        VSCODE_DIR.mkdir()

    if LAUNCH_FILE.exists():
        print("launch.json already exists. Skipping.")
        return

    launch_config = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Run Application",
                "type": "python",
                "request": "launch",
                "module": "main",
                "console": "integratedTerminal"
            }
        ]
    }

    with open(LAUNCH_FILE, "w", encoding="utf-8") as f:
        json.dump(launch_config, f, indent=4)

    print(f"Created: {LAUNCH_FILE}")


def main():

    print("Setting up project environment...\n")

    ensure_init_files()
    ensure_vscode_launch()

    print("\nProject setup complete.")


if __name__ == "__main__":
    main()