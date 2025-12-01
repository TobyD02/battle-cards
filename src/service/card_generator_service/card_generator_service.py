import os

import requests
from ollama import Client
from typing import Type, TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

class CardGeneratorService:
    def __init__(self):
        session = requests.Session()
        session.timeout = 2

        self.client = Client(
            host=os.getenv("OLLAMA_URL"),
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        self.model="gemma3:4b"

    def prompt(self, prompt: str, output_schema: Type[T]) -> T:
        llm_response = self.client.chat(
            model=self.model,
            messages = [{'role': 'user', 'content': prompt}],
            format=output_schema.model_json_schema()
        )

        response = output_schema.model_validate_json(llm_response.message.content)
        return response




