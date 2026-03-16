import os
import shutil
import re

# ==========================
# Configuración
# ==========================
PROJECT_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "universal_data_importer")
CORE_DIR = os.path.join(PROJECT_ROOT, "core")
MODELS_FILE = os.path.join(CORE_DIR, "models.py")
REPORT_FILE = os.path.join(PROJECT_ROOT, "fix_models_report.txt")

report = []

# ==========================
# Paso 1: Respaldar models.py
# ==========================
if os.path.exists(MODELS_FILE):
    backup_file = MODELS_FILE + ".bak"
    shutil.copy2(MODELS_FILE, backup_file)
    report.append(f"Backup de models.py creado en: {backup_file}")
else:
    report.append("models.py no existe, se omite el backup.")

# ==========================
# Paso 2: Crear schema.py y results.py
# ==========================
SCHEMA_FILE = os.path.join(CORE_DIR, "schema.py")
RESULTS_FILE = os.path.join(CORE_DIR, "results.py")
INIT_FILE = os.path.join(CORE_DIR, "__init__.py")

# Contenido de schema.py
schema_content = """class Schema:
    def __init__(self, name, columns=None):
        self.name = name
        self.columns = columns or []

    def add_column(self, column_name, column_type):
        self.columns.append({"name": column_name, "type": column_type})
"""

# Contenido de results.py
results_content = """class ImportResult:
    def __init__(self, success=0, failed=0):
        self.success = success
        self.failed = failed

    def add_success(self, count=1):
        self.success += count

    def add_failure(self, count=1):
        self.failed += count
"""

# Contenido de __init__.py
init_content = """from .schema import Schema
from .results import ImportResult
"""

for file_path, content in [(SCHEMA_FILE, schema_content), (RESULTS_FILE, results_content), (INIT_FILE, init_content)]:
    if os.path.exists(file_path):
        shutil.copy2(file_path, file_path + ".bak")
        report.append(f"Backup creado: {file_path}.bak")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    report.append(f"Archivo creado/actualizado: {file_path}")

# ==========================
# Paso 3: Actualizar imports en todo el proyecto
# ==========================
pattern = re.compile(r'from\s+core\.models\s+import\s+(.+)')

for root, _, files in os.walk(PROJECT_ROOT):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            new_content = pattern.sub(r'from core import \1', content)
            if new_content != content:
                shutil.copy2(path, path + ".bak")
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                report.append(f"Imports actualizados en: {os.path.relpath(path, PROJECT_ROOT)} (backup: {file}.bak)")

# ==========================
# Guardar reporte
# ==========================
with open(REPORT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(report))

print("Proceso de refactorización completado ✅")
print(f"Revisa el reporte en: {REPORT_FILE}")
