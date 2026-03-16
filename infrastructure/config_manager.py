class ConfigManager:

    def __init__(self):
        self.config = {}

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value