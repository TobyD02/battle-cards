import os
from src.service.database_service.database_service import DatabaseService


def database_service_factory():
    return DatabaseService(os.getenv("DB_PATH"))