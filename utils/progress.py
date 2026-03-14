from utils.progress import ProgressTracker
"""
Progress Tracker
----------------

Clase simple para seguimiento de progreso durante imports.

Puede usarse para:

- CLI
- GUI
- logs
- callbacks
"""

import time
from typing import Optional, Callable


class ProgressTracker:

    def __init__(
        self,
        total: Optional[int] = None,
        callback: Optional[Callable] = None
    ):
        """
        total: número total de elementos esperados
        callback: función opcional que recibe updates
        """

        self.total = total
        self.current = 0

        self.start_time = time.time()

        self.callback = callback

    # -----------------------------------------------------

    def update(self, amount: int = 1):

        self.current += amount

        elapsed = time.time() - self.start_time

        rate = self.current / elapsed if elapsed > 0 else 0

        percent = None

        if self.total:
            percent = (self.current / self.total) * 100

        info = {
            "current": self.current,
            "total": self.total,
            "percent": percent,
            "rate": rate,
            "elapsed": elapsed
        }

        if self.callback:
            self.callback(info)

        return info

    # -----------------------------------------------------

    def reset(self):

        self.current = 0
        self.start_time = time.time()

    # -----------------------------------------------------

    def summary(self):

        elapsed = time.time() - self.start_time

        return {
            "processed": self.current,
            "elapsed": elapsed,
            "rate": self.current / elapsed if elapsed else 0
        }
