import inspect
import pkgutil
import importlib
from pathlib import Path
from typing import List, Optional

from plugins.base_plugin import BasePlugin


# --------------------------------------------------
# Discover plugins dynamically
# --------------------------------------------------

def discover_plugins() -> List[BasePlugin]:

    plugins = []

    package_name = "plugins"

    for _, module_name, _ in pkgutil.iter_modules(["plugins"]):

        if module_name in ["base_plugin", "plugin_registry"]:
            continue

        module = importlib.import_module(f"{package_name}.{module_name}")

        for _, obj in inspect.getmembers(module, inspect.isclass):

            if issubclass(obj, BasePlugin) and obj is not BasePlugin:

                plugins.append(obj())

    return plugins


# --------------------------------------------------
# Load plugins
# --------------------------------------------------

PLUGINS: List[BasePlugin] = discover_plugins()


# --------------------------------------------------
# Detect plugin for a file
# --------------------------------------------------

def detect_plugin(file_path: Path) -> Optional[BasePlugin]:

    for plugin in PLUGINS:

        try:

            if plugin.detect(file_path):
                return plugin

        except Exception:
            continue

    return None


# --------------------------------------------------
# Utility
# --------------------------------------------------

def list_plugins():

    return [plugin.name for plugin in PLUGINS]
