from loaders.sqlite_loader import SQLiteLoader
from loaders.mysql_loader import MySQLLoader
from loaders.postgres_loader import PostgresLoader


LOADERS = {
    "sqlite": SQLiteLoader,
    "mysql": MySQLLoader,
    "postgres": PostgresLoader
}


def get_loader(loader_type: str):
    return LOADERS.get(loader_type)
