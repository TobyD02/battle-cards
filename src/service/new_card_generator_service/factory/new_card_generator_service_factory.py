from src.service.database_service.factory.database_service_factory import database_service_factory
from src.service.fandom_query_service.factory.fandom_query_service_factory import fandom_query_service_factory
from src.service.llm_service.factory.llm_service_factory import llm_service_factory
from src.service.new_card_generator_service.new_card_generator_service import NewCardGeneratorService


def new_card_generator_service_factory():
    return NewCardGeneratorService(
        database_service = database_service_factory(),
        fandom_query_service = fandom_query_service_factory(),
        llm_service = llm_service_factory(),
    )