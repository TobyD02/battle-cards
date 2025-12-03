from typing import Union

import requests

from src.entity.card_base_model import CardBaseModel
from src.repository.card_base_repository.card_base_repository import CardBaseRepository
from src.service.fandom_query_service.fandom_query_service import FandomQueryService
from src.service.llm_service.llm_service import LlmService

from src.model.card_info_model import generate_card_prompt, CardInfoModel

class NewCardGeneratorService:
    def __init__(
            self,
            card_base_repository: CardBaseRepository,
            fandom_query_service: FandomQueryService,
            llm_service = LlmService,
    ):
        self.card_base_repository = card_base_repository
        self.fandom_query_service = fandom_query_service
        self.llm_service = llm_service


    def generate_new_card(self, name: str) -> int:
        preprocessed_name = name.replace(" ", "").lower()

        results = self.fandom_query_service.get_search_results(name)
        paragraphs = self.fandom_query_service.get_page_paragraphs(results[0])

        card_stats = self.llm_service.prompt(generate_card_prompt(paragraphs, name), CardInfoModel)

        image_url = None

        images = []

        # print(f"RESULTS: {results}")
        for i in results:
            wiki_url = i
            images = self.fandom_query_service.get_page_image_links(wiki_url)
            if len(images) > 0:
                break

        # print(images, flush=True)
        if len(images) > 0:
            for i in images:
                try:
                    response = requests.get(i)
                    response.raise_for_status()  # Raise an exception for HTTP errors

                    # Save to file
                    with open("/images/" + name + ".png", "wb") as f:
                        f.write(response.content)

                    image_url = "/images/" + name + ".png"
                    break
                except Exception:
                    pass

        else:
            image_url = "".join(images)

        card_model = CardBaseModel(
            label=preprocessed_name,
            name=card_stats.name,
            strength=card_stats.strength,
            dexterity=card_stats.dexterity,
            wisdom=card_stats.wisdom,
            intelligence=card_stats.intelligence,
            charisma=card_stats.charisma,
            constitution=card_stats.constitution,
            description=card_stats.description,
            image_url=image_url,
            wiki_url=wiki_url,
        )

        return self.card_base_repository.insert_card(card_model)


