"""
Loader Registry
---------------

Sistema central para registrar y recuperar loaders.

Permite que el engine obtenga automáticamente el loader correcto
según el tipo de destino.

Ejemplo:

    loader = LoaderRegistry.create(
        "sqlite",
        connection_string="sqlite:///data/test.db"
    )
"""

from typing import Dict, Type

from core.exceptions import LoaderError


class LoaderRegistry:
    """
    Registro central de loaders disponibles.
    """

    _loaders: Dict[str, Type] = {}

    # ---------------------------------------------------------

    @classmethod
    def register(cls, name: str, loader_class: Type):
        """
        Registra un loader en el sistema.
        """

        name = name.lower()

        if name in cls._loaders:
            raise LoaderError(f"Loader '{name}' ya está registrado")

        cls._loaders[name] = loader_class

    # ---------------------------------------------------------

    @classmethod
    def get(cls, name: str):
        """
        Obtiene la clase loader registrada.
        """

        name = name.lower()

        if name not in cls._loaders:
            raise LoaderError(f"Loader '{name}' no registrado")

        return cls._loaders[name]

    # ---------------------------------------------------------

    @classmethod
    def create(cls, name: str, **kwargs):
        """
        Crea instancia de loader.
        """

        loader_class = cls.get(name)

        return loader_class(**kwargs)

    # ---------------------------------------------------------

    @classmethod
    def list_loaders(cls):
        """
        Lista loaders disponibles.
        """

        return list(cls._loaders.keys())
