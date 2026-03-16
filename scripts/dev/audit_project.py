import os

EXPECTED_FOLDERS = [
    "app",
    "gui",
    "core",
    "infrastructure",
    "scripts",
    "tests",
    "taps",
]

EXPECTED_FILES = [
    "meltano.yml",
]

CORE_MODULES = [
    "core/services/meltano_service.py",
    "core/services/pipeline_service.py",
    "core/detectors/file_detector.py",
]

def check_path(path):
    return os.path.exists(path)

def audit():
    print("\n=== PROJECT AUDIT ===\n")

    print("Checking folders\n")

    for folder in EXPECTED_FOLDERS:
        if check_path(folder):
            print(f"✔ {folder}")
        else:
            print(f"❌ missing folder: {folder}")

    print("\nChecking critical files\n")

    for file in EXPECTED_FILES:
        if check_path(file):
            print(f"✔ {file}")
        else:
            print(f"❌ missing file: {file}")

    print("\nChecking core modules\n")

    for module in CORE_MODULES:
        if check_path(module):
            print(f"✔ {module}")
        else:
            print(f"❌ missing module: {module}")

    print("\nAudit complete\n")


if __name__ == "__main__":
    audit()