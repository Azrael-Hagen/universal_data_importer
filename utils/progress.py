class ProgressTracker:

    def __init__(self):
        self.current = 0
        self.total = 0

    def start(self, total: int):
        self.total = total
        self.current = 0

    def update(self, step: int = 1):
        self.current += step

    def percent(self):
        if self.total == 0:
            return 0
        return (self.current / self.total) * 100
