from src.service.llm_service.llm_service import LlmService


def llm_service_factory():
    return LlmService()