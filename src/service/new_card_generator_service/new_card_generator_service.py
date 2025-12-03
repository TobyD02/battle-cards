from typing import Union

import requests

from src.entity.card_model import CardModel
from src.service.database_service.database_service import DatabaseService
from src.service.fandom_query_service.fandom_query_service import FandomQueryService
from src.service.llm_service.llm_service import LlmService

from src.model.card_info_model import generate_card_prompt, CardInfoModel

class NewCardGeneratorService:
    def __init__(
            self,
            database_service: DatabaseService,
            fandom_query_service: FandomQueryService,
            llm_service = LlmService,
    ):
        self.database_service = database_service
        self.fandom_query_service = fandom_query_service
        self.llm_service = llm_service

    def check_if_card_exists(self, name: str) -> Union[CardModel, None]:
        preprocessed_name = name.replace(" ", "").lower()
        try:
            found_card = self.database_service.get_card_by_label(preprocessed_name)
            return found_card
        except Exception:
            return None


    def generate_new_card(self, name: str):
        preprocessed_name = name.replace(" ", "").lower()

        results = self.fandom_query_service.get_search_results(name)
        paragraphs = self.fandom_query_service.get_page_paragraphs(results[0])

        card_stats = self.llm_service.prompt(generate_card_prompt(paragraphs, name), CardInfoModel)

        image_url = None
        wiki_url = results[0]
        images = self.fandom_query_service.get_page_image_links(results[0])
        if len(images) > 0:
            response = requests.get(images[0])
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Save to file
            with open("/images/" + name + ".png", "wb") as f:
                f.write(response.content)

            image_url = "/images/" + name + ".png"
        else:
            image_url = "".join(images)

        aggregate_stats = card_stats.strength + card_stats.dexterity + card_stats.constitution \
                          + card_stats.intelligence + card_stats.wisdom

        if aggregate_stats > 400:
            holo = True
        else:
            holo = False

        card_model = CardModel(
            label=preprocessed_name,
            name=card_stats.name,
            strength=card_stats.strength,
            dexterity=card_stats.dexterity,
            wisdom=card_stats.wisdom,
            intelligence=card_stats.intelligence,
            charisma=card_stats.charisma,
            constitution=card_stats.constitution,
            aggregate_stats=aggregate_stats,
            description=card_stats.description,
            image_url=image_url,
            wiki_url=wiki_url,
            holo=holo
        )

        return self.database_service.insert_card(card_model)


