from plugins.csv_plugin import CSVPlugin
from plugins.json_plugin import JSONPlugin
from plugins.excel_plugin import ExcelPlugin
from plugins.xml_plugin import XMLPlugin


PLUGINS = [
    CSVPlugin(),
    JSONPlugin(),
    ExcelPlugin(),
    XMLPlugin()
]


def detect_plugin(file_path):
    for plugin in PLUGINS:
        if plugin.detect(file_path):
            return plugin
    return None
