import random

from fastapi import FastAPI
import requests

from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from fastapi import Request

from src.model.card_info_model import generate_card_prompt, CardInfoModel
from src.entity.card_model import CardModel
from src.service.llm_service.factory.llm_service_factory import llm_service_factory
from src.service.database_service.factory.database_service_factory import database_service_factory
from src.service.fandom_query_service.factory.fandom_query_service_factory import fandom_query_service_factory
from src.service.new_card_generator_service.factory.new_card_generator_service_factory import \
    new_card_generator_service_factory


def register_routes(app: FastAPI) -> None:
    app.mount("/images", StaticFiles(directory="/images"), name="images")
    app.mount("/static", StaticFiles(directory="./static"), name="static")
    templates = Jinja2Templates(directory="templates")

    @app.get("/generate/{name}")
    async def index(request: Request, name: str):
        new_card_generator_service = new_card_generator_service_factory()

        card = new_card_generator_service.check_if_card_exists(name)
        if card:
            return templates.TemplateResponse("index.html.j2", {"request": request, "card": card})

        card = new_card_generator_service.generate_new_card(name)
        return templates.TemplateResponse("index.html.j2", {"request": request, "card": card})

    @app.get("/variants/{name}")
    async def variants(request: Request, name: str):
        new_card_generator_service = new_card_generator_service_factory()

        card = new_card_generator_service.check_if_card_exists(name)

        if not card:
            return templates.TemplateResponse("all_variants.html.j2", {
                "request": request,
                "card": None,
                "negative_card": None,
                "gold_card": None,
                "negative_gold_card": None,
            })

        card_base = card.model_dump()
        card_negative = card_base.copy()
        card_negative["negative"] = True

        card_gold = card_base.copy()
        card_gold["gold"] = True

        card_negative_gold = card_base.copy()
        card_negative_gold["negative"] = True
        card_negative_gold["gold"] = True

        return templates.TemplateResponse("all_variants.html.j2", {
            "request": request,
            "card_base": card_base,
            "card_negative": card_negative,
            "card_gold": card_gold,
            "card_negative_gold": card_negative_gold,
        })

    @app.get("/open-pack")
    async def open_pack(request: Request):
        # Get random card from deck
        # Random chance that it is negative
        # Random chance that it is gold
        database_service = database_service_factory()
        card = database_service.get_random_card().model_dump()

        card["negative"] = True if random.randint(0, 10) > 8 else False
        card["gold"] = True if random.randint(0, 10) > 8 else False

        return templates.TemplateResponse("index.html.j2", {"request": request, "card": card})

    @app.get("/cards")
    async def index3():
        database_service = database_service_factory()
        results = database_service.get_all_cards()
        return results

    @app.get("/cards/count")
    async def index3():
        database_service = database_service_factory()
        result = database_service.get_all_cards_count()
        return {"count": result}
