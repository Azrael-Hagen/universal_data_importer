import os
import shutil

ROOT = os.getcwd()

structure = [
    "app",
    "gui/views",
    "gui/viewmodels",
    "gui/widgets",
    "core/models",
    "core/services",
    "core/detectors",
    "infrastructure",
    "taps",
    "scripts/dev",
    "scripts/setup",
    "tests",
]

files_to_move = {
    "setup_meltano_transition.py": "scripts/dev/",
    "repair_meltano_environment.py": "scripts/dev/",
}

def create_structure():
    print("Creating project structure...")

    for folder in structure:
        path = os.path.join(ROOT, folder)
        os.makedirs(path, exist_ok=True)
        print(f"✔ {folder}")

def move_files():
    print("\nMoving legacy scripts...")

    for file, destination in files_to_move.items():
        src = os.path.join(ROOT, file)

        if os.path.exists(src):
            dst = os.path.join(ROOT, destination, file)
            shutil.move(src, dst)
            print(f"✔ moved {file} -> {destination}")

def create_init_files():
    print("\nCreating __init__.py files...")

    packages = [
        "gui",
        "gui/views",
        "gui/viewmodels",
        "core",
        "core/models",
        "core/services",
        "core/detectors",
        "infrastructure",
    ]

    for pkg in packages:
        path = os.path.join(ROOT, pkg, "__init__.py")
        open(path, "a").close()
        print(f"✔ {path}")

def main():
    print("\n=== UNIVERSAL DATA IMPORTER PROJECT SETUP ===\n")

    create_structure()
    move_files()
    create_init_files()

    print("\nProject structure ready.\n")

if __name__ == "__main__":
    main()