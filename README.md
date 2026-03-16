# Universal Data Importer

Universal Data Importer is a modular data ingestion tool designed to import structured data from multiple file formats and process them through configurable pipelines.

The project focuses on clean architecture, extensibility, and maintainability, allowing the system to support multiple data sources, pipeline engines, and execution strategies.

---

# Project Goals

The main goals of this project are:

* Provide a universal interface for importing structured data
* Support multiple file formats
* Execute ingestion pipelines using external tools such as Meltano
* Maintain a clean and extensible architecture
* Allow future support for plugins and new pipeline engines
* Provide a GUI for non-technical users

---

# Architecture

The project follows a layered architecture inspired by Clean Architecture principles.

```
app
core
infrastructure
gui
```

### Layer responsibilities

**App**

Application entrypoints and dependency bootstrapping.

```
app/
 ├ main.py
 └ bootstrap.py
```

---

**Core**

Domain logic and application services.

```
core/
 ├ detectors
 ├ executors
 ├ models
 └ services
```

Responsibilities:

* Data source detection
* Pipeline definition
* Pipeline orchestration
* Execution abstraction

---

**Infrastructure**

External integrations and system utilities.

```
infrastructure/
 ├ config_manager.py
 ├ logger.py
 └ meltano_runner.py
```

Responsibilities:

* Logging
* Configuration
* External tool execution

---

**GUI**

User interface layer.

```
gui/
 ├ viewmodels
 └ views
```

Responsibilities:

* Present data to the user
* Trigger backend services
* Display pipeline execution logs

---

# Execution Flow

```
GUI / CLI
   │
   ▼
PipelineService
   │
   ├ Detect file type
   ├ Build datasource
   ├ Resolve pipeline
   └ Execute pipeline
        │
        ▼
PipelineExecutor
        │
        ▼
MeltanoExecutor
        │
        ▼
MeltanoRunner
```

---

# Supported File Types

Currently supported:

* CSV
* Excel
* JSON

The architecture allows new formats to be added easily.

---

# Pipeline Execution

Pipelines are executed using a pluggable executor system.

Current executor:

```
MeltanoExecutor
```

Future executors may include:

* Airbyte
* Spark
* Custom plugins

---

# Streaming Execution Logs

Pipeline execution streams logs using Python generators.

Example:

```python
for log in pipeline_service.import_file("data.csv"):
    print(log)
```

This allows:

* Real-time progress updates
* GUI integration
* CLI output streaming

---

# Pipeline Results

Pipeline executions generate structured results containing:

* Success status
* Execution time
* Error information
* Future metrics such as processed records

Example:

```
PipelineResult
```

---

# Extensibility

The system is designed to support future extensions such as:

* Plugin-based pipelines
* Additional file detectors
* Multiple execution engines
* DAG-based pipeline workflows
* Remote data sources

---

# Running the Project

Create a virtual environment:

```
python -m venv .venv
```

Activate it:

Windows:

```
.venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

Run the application:

```
python app/main.py
```

---

# Development Principles

This project follows several
