from core.engine import ImportEngine
"""
Import Engine
-------------

Orquesta todo el proceso de importación de datos:

PLUGIN → ENGINE → LOADER
"""

from typing import Optional, Callable, List, Dict
from core.import_job import ImportJob
from plugins.plugin_registry import PluginRegistry
from loaders.loader_registry import LoaderRegistry
from utils.progress import ProgressTracker
from core.exceptions import ImporterError

class ImportEngine:
    """
    Motor principal de importación.
    """

    def __init__(
        self,
        progress_callback: Optional[Callable] = None,
        log_callback: Optional[Callable] = None,
    ):
        self.progress_callback = progress_callback
        self.log_callback = log_callback

    # -----------------------------------------------------
    # logging
    # -----------------------------------------------------

    def _log(self, message: str):
        if self.log_callback:
            self.log_callback(message)
        else:
            print(message)

    # -----------------------------------------------------
    # run
    # -----------------------------------------------------

    def run(self, job: ImportJob):
        """
        Ejecuta un ImportJob completo.
        """

        self._log(f"Starting import job: {job.table_name}")

        # Crear instancia del plugin
        plugin = PluginRegistry.create(
            job.source_plugin,
            **job.source_config
        )

        self._log(f"Loaded plugin: {job.source_plugin}")

        # Crear instancia del loader
        loader = LoaderRegistry.create(
            job.destination_loader,
            **job.destination_config
        )

        self._log(f"Loaded loader: {job.destination_loader}")

        # Conectar loader si tiene método connect()
        if hasattr(loader, "connect"):
            loader.connect()

        total_rows = 0
        errors = 0

        # Configurar tracker de progreso
        tracker = ProgressTracker(callback=self.progress_callback)

        # Leer en batches si el plugin lo soporta
        batch_method = getattr(plugin, "read_batches", None)
        if batch_method:
            for batch in plugin.read_batches(job.batch_size):
                try:
                    loader.insert_rows(job.table_name, batch)
                    total_rows += len(batch)
                    tracker.update(len(batch))
                except Exception as e:
                    self._log(f"Error inserting batch: {e}")
                    errors += len(batch)
        else:
            # fallback a read_rows()
            for row in plugin.read_rows():
                try:
                    loader.insert_rows(job.table_name, [row])
                    total_rows += 1
                    tracker.update(1)
                except Exception as e:
                    self._log(f"Error inserting row: {e}")
                    errors += 1

        # cerrar loader si tiene método close()
        if hasattr(loader, "close"):
            loader.close()

        self._log(f"Import completed: {total_rows} rows processed, {errors} errors")

        return total_rows, errors
