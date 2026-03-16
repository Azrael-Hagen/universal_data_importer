from dataclasses import dataclass
from typing import Optional


@dataclass
class PipelineResult:
    """
    Structured result of a pipeline execution.
    """

    success: bool
    error: Optional[str] = None
    records_processed: Optional[int] = None
    execution_time: Optional[float] = None