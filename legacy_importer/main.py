"""
Universal Data Importer
Main entry point
"""

import sys
from core import Schema, ImportResult


def run():
    """
    Punto de entrada principal del sistema
    """

    print("🚀 Universal Data Importer iniciado")

    try:
        # Crear un esquema de ejemplo
        schema = Schema(
            name="example_schema",
            columns=[
                {"name": "id", "type": "int"},
                {"name": "name", "type": "string"},
            ],
        )

        print(f"Schema cargado: {schema.name}")
        print(f"Columnas: {schema.columns}")

        # Resultado de importación
        result = ImportResult()

        # Simulación de proceso de import
        result.add_success(10)
        result.add_failure(2)

        print("\n📊 Resultado de importación")
        print(f"Registros exitosos: {result.success}")
        print(f"Registros fallidos: {result.failed}")

        print("\n✅ Proceso completado correctamente")

    except Exception as e:
        print("\n❌ Error durante la ejecución")
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    run()