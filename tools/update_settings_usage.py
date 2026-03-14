"""
Refactor script to replace hardcoded configuration
values with imports from config.settings.
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ----------------------------------------

REPLACEMENTS = {
    "nrows=200": "nrows=PREVIEW_ROWS",
    "batch_size=500": "batch_size=BATCH_SIZE",
    '"imported_data.db"': "SQLITE_DB_PATH",
    '"import_table"': "DEFAULT_TABLE_NAME",
}

IMPORT_LINE = "from config.settings import PREVIEW_ROWS, BATCH_SIZE, SQLITE_DB_PATH, DEFAULT_TABLE_NAME\n"

# ----------------------------------------

def process_file(file_path):

    text = file_path.read_text(encoding="utf-8")

    modified = False

    for old, new in REPLACEMENTS.items():
        if old in text:
            text = text.replace(old, new)
            modified = True

    if modified:

        if "from config.settings import" not in text:

            lines = text.splitlines()

            insert_index = 0

            # Find last import
            for i, line in enumerate(lines):
                if line.startswith("import") or line.startswith("from"):
                    insert_index = i + 1

            lines.insert(insert_index, IMPORT_LINE.strip())

            text = "\n".join(lines)

        file_path.write_text(text, encoding="utf-8")

        print(f"Updated: {file_path}")


# ----------------------------------------

def scan_project():

    for path in PROJECT_ROOT.rglob("*.py"):

        if "tools" in str(path):
            continue

        process_file(path)


# ----------------------------------------

if __name__ == "__main__":

    print("Scanning project for hardcoded config values...\n")

    scan_project()

    print("\nDone.")