import subprocess
import os
import shutil
import sys
import yaml
import stat

REQUIRED_PLUGINS = [
    "tap-csv",
    "tap-excel",
    "target-jsonl"
]

PROJECT_FILE = "meltano.yml"


def run(cmd):
    print(f"\n> {cmd}")
    result = subprocess.run(cmd, shell=True)
    return result.returncode


def meltano_installed():
    try:
        subprocess.run(
            ["meltano", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        return True
    except Exception:
        return False


def ensure_project():
    if not os.path.exists(PROJECT_FILE):
        print("⚠️ No meltano project detected. Initializing...")
        run("meltano init .")


def load_project_plugins():
    if not os.path.exists(PROJECT_FILE):
        return []

    try:
        with open(PROJECT_FILE, "r") as f:
            data = yaml.safe_load(f)
    except Exception:
        return []

    plugins = []

    if not data:
        return plugins

    p = data.get("plugins", {})

    for section in ["extractors", "loaders"]:
        if section in p:
            for plugin in p[section]:
                plugins.append(plugin["name"])

    return plugins


def remove_broken_installations():

    base = ".meltano"

    if not os.path.exists(base):
        return

    broken = [
        "tap-spreadsheets-anywhere",
    ]

    for root, dirs, _ in os.walk(base):

        for d in dirs:

            if d in broken:

                path = os.path.join(root, d)

                print(f"Removing broken plugin: {path}")

                try:
                    shutil.rmtree(path)
                except PermissionError:

                    def onerror(func, path, exc_info):
                        os.chmod(path, stat.S_IWRITE)
                        func(path)

                    shutil.rmtree(path, onerror=onerror)


def add_missing_plugins(installed):

    for plugin in REQUIRED_PLUGINS:

        if plugin not in installed:
            print(f"Installing plugin: {plugin}")
            run(f"meltano add {plugin}")
        else:
            print(f"✔ Already installed: {plugin}")


def install_dependencies():

    print("\nInstalling plugin dependencies...")
    run("meltano install")


def test_pipeline():

    print("\nTesting Meltano invocation...")
    run("meltano invoke tap-csv --help")


def main():

    print("\n===== MELTANO ENVIRONMENT CHECK =====\n")

    if not meltano_installed():
        print("❌ Meltano is not installed.")
        print("Install with: pip install meltano")
        sys.exit(1)

    print("✔ Meltano detected")

    ensure_project()

    remove_broken_installations()

    installed = load_project_plugins()

    print("\nDetected plugins:")
    print(installed)

    add_missing_plugins(installed)

    install_dependencies()

    test_pipeline()

    print("\n✅ Meltano environment ready.")


if __name__ == "__main__":
    main()