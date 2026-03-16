import os
import subprocess
import shutil

PROJECT_NAME = "universal_data_importer"
LEGACY_FOLDER = "legacy_importer"

def run(cmd):
    print(f"> {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def ensure_meltano():
    try:
        run("meltano --version")
    except:
        print("Instalando Meltano...")
        run("pip install meltano")

def init_meltano():
    if not os.path.exists("meltano.yml"):
        run("meltano init .")

def create_structure():
    folders = [
        "extractors",
        "loaders",
        "transformers",
        "gui",
        "scripts"
    ]

    for f in folders:
        os.makedirs(f, exist_ok=True)

def move_legacy():
    if not os.path.exists(LEGACY_FOLDER):
        os.makedirs(LEGACY_FOLDER)

        for item in os.listdir():
            if item in [
                LEGACY_FOLDER,
                ".git",
                "meltano.yml",
                "__pycache__"
            ]:
                continue

            if os.path.isdir(item) or item.endswith(".py"):
                shutil.move(item, f"{LEGACY_FOLDER}/{item}")

def install_basic_plugins():
    plugins = [
        "tap-csv",
        "tap-json",
        "tap-spreadsheets-anywhere",
        "target-jsonl"
    ]

    for p in plugins:
        try:
            run(f"meltano add extractor {p}")
        except:
            pass

def main():
    print("=== TRANSICIÓN A MELTANO ===")

    ensure_meltano()
    init_meltano()
    create_structure()
    move_legacy()
    install_basic_plugins()

    print("\n✅ Transición inicial completada")

if __name__ == "__main__":
    main()