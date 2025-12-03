import os
from src.repository.card_base_repository.card_base_repository import CardBaseRepository


def card_base_repository_factory():
    return CardBaseRepository(os.getenv("DB_PATH"))