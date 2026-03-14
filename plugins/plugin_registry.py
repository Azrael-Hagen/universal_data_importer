# gui/plugins/plugin_registry.py
from .csv_plugin import CSVPlugin
from .excel_plugin import ExcelPlugin
from .json_plugin import JSONPlugin
from .xml_plugin import XMLPlugin

class PluginRegistry:

    _plugins = [CSVPlugin, ExcelPlugin, JSONPlugin, XMLPlugin]

    @classmethod
    def detect_plugin(cls, file_path):
        for plugin_cls in cls._plugins:
            if plugin_cls.detect(file_path):
                return plugin_cls
        return None
