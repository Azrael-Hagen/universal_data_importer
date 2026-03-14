# Universal Data Importer

**Universal Data Importer** es una herramienta modular para importar datos desde múltiples fuentes hacia distintos destinos de almacenamiento.

El proyecto está diseñado con una arquitectura extensible basada en **plugins**, permitiendo añadir fácilmente nuevos formatos de entrada y nuevos destinos de datos.

Su objetivo es convertirse en un **importador universal de datos**, capaz de manejar pipelines como:

```
CSV → SQLite
CSV → PostgreSQL
JSON → MySQL
API → Data Warehouse
```

---

# Arquitectura del sistema

El proyecto sigue una arquitectura desacoplada basada en **fuente → engine → destino**.

```
SOURCE (Plugin)
      │
      ▼
Import Engine
      │
      ▼
DESTINATION (Loader)
```

Componentes principales:

* **Plugins**
  Encargados de leer datos desde diferentes fuentes.

* **Engine**
  Orquesta el proceso de importación.

* **Loaders**
  Escriben los datos en el destino final.

* **Registries**
  Sistemas que permiten registrar automáticamente plugins y loaders.

---

# Estructura del proyecto

```
universal_data_importer/

core/
    models.py
    exceptions.py
    import_job.py
    engine.py

plugins/
    base_plugin.py
    plugin_registry.py
    csv_plugin.py

loaders/
    loader_registry.py
    sqlite_loader.py

utils/
    progress.py

gui/
    dialogs/

tools/
    bootstrap_architecture.py
```

---

# Conceptos principales

## Plugin

Un **plugin** representa una fuente de datos.

Ejemplos:

* CSV
* Excel
* JSON
* API REST
* Base de datos

Los plugins implementan una interfaz común:

```
read_rows()
read_batches()
```

Esto permite manejar datasets grandes sin cargar todo en memoria.

---

## Loader

Un **loader** representa el destino de los datos.

Ejemplos:

* SQLite
* PostgreSQL
* MySQL
* Parquet
* Data Warehouse

Los loaders reciben filas de datos y las insertan en el destino.

---

## Import Job

Un **ImportJob** define un proceso completo de importación:

```
source_plugin
destination_loader
source_config
destination_config
batch_size
table_name
```

El engine utiliza esta configuración para ejecutar el pipeline.

---

# Ejemplo de uso

Ejemplo simple de importación:

```
CSV → SQLite
```

```python
from core.import_job import ImportJob
from core.engine import ImportEngine

job = ImportJob(
    source_plugin="csv",
    destination_loader="sqlite",
    source_config={
        "file_path": "data/users.csv"
    },
    destination_config={
        "connection_string": "sqlite:///data/test.db"
    },
    table_name="users"
)

engine = ImportEngine()

engine.run(job)
```

---

# Plugins disponibles

Actualmente implementados:

| Plugin | Estado |
| ------ | ------ |
| CSV    | ✔      |

Plugins planeados:

* Excel
* JSON
* API REST
* PostgreSQL source
* Parquet

---

# Loaders disponibles

Actualmente implementados:

| Loader | Estado |
| ------ | ------ |
| SQLite | ✔      |

Loaders planeados:

* PostgreSQL
* MySQL
* DuckDB
* Parquet
* Data Warehouse

---

# Características del proyecto

* Arquitectura modular
* Sistema de plugins extensible
* Procesamiento por batches
* Soporte para datasets grandes
* Seguimiento de progreso
* Preparado para GUI futura

---

# Roadmap

Fases planeadas del proyecto:

### Fase 1

Arquitectura base

* plugin system
* loader system
* import engine
* CSV → SQLite

### Fase 2

Nuevas fuentes

* Excel
* JSON
* APIs

### Fase 3

Nuevos destinos

* PostgreSQL
* MySQL
* DuckDB

### Fase 4

Interfaz gráfica

* GUI de conexión
* selección de fuentes
* monitor de progreso

---

# Desarrollo

Clonar el repositorio:

```
git clone https://github.com/Azrael-Hagen/universal_data_importer.git
```

Entrar al proyecto:

```
cd universal_data_importer
```

Ejecutar pruebas simples:

```
python tools/test_csv_plugin.py
python tools/test_sqlite_loader.py
```

---

# Contribuciones

Las contribuciones son bienvenidas.

Ideas para contribuir:

* nuevos plugins de fuente
* nuevos loaders
* optimizaciones de rendimiento
* mejoras de GUI
* documentación

---

# Licencia

MIT License
