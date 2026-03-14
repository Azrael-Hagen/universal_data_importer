from core.import_job import ImportJob
"""
Import Job
----------

Representa una ejecución de importación de datos.

Contiene toda la información necesaria para ejecutar
un proceso completo:

    Fuente (plugin)
    Destino (loader)
    Configuración
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from datetime import datetime


@dataclass
class ImportJob:
    """
    Representa un job de importación de datos.
    """

    source_plugin: str
    destination_loader: str

    source_config: Dict[str, Any]
    destination_config: Dict[str, Any]

    table_name: Optional[str] = None

    batch_size: int = 1000

    created_at: datetime = field(default_factory=datetime.utcnow)

    metadata: Dict[str, Any] = field(default_factory=dict)

    # ---------------------------------------------------------

    def describe(self) -> Dict[str, Any]:
        """
        Devuelve una descripción serializable del job.
        """

        return {
            "source_plugin": self.source_plugin,
            "destination_loader": self.destination_loader,
            "table_name": self.table_name,
            "batch_size": self.batch_size,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata,
        }
