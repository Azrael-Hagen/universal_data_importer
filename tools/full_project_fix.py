import os
import re
import shutil

# ============================================
# Configuración
# ============================================
PROJECT_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "universal_data_importer")
REPORT_FILE = os.path.join(PROJECT_ROOT, "full_fix_report.txt")

# Patrón para detectar cualquier import desde core.models
pattern = re.compile(r'from\s+core\.models\s+import\s+(.+)', re.MULTILINE)

report = []

# ============================================
# Función para crear backup y escribir cambios
# ============================================
def backup_and_write(file_path, new_content):
    backup_file = file_path + ".bak"
    shutil.copy2(file_path, backup_file)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    return backup_file

# ============================================
# Recorrer proyecto
# ============================================
for root, _, files in os.walk(PROJECT_ROOT):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            new_content = pattern.sub(r'from core import \1', content)

            if new_content != content:
                backup_file = backup_and_write(path, new_content)
                report.append(f"Actualizado imports en: {os.path.relpath(path, PROJECT_ROOT)}")
                report.append(f"Backup creado: {os.path.relpath(backup_file, PROJECT_ROOT)}")

# ============================================
# Guardar reporte
# ============================================
with open(REPORT_FILE, "w", encoding="utf-8") as f:
    if report:
        f.write("\n".join(report))
    else:
        f.write("No se realizaron cambios.\n")

print("\nProceso de full fix completado ✅")
print(f"Revisa el reporte en: {REPORT_FILE}")
print("Todos los imports problemáticos de core.models han sido reemplazados por from core import ...")
