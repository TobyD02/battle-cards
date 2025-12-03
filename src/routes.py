import random

from fastapi import FastAPI, Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from src.repository.card_base_repository.factory.card_base_repository_factory import card_base_repository_factory
from src.service.new_card_generator_service.factory.new_card_generator_service_factory import \
    new_card_generator_service_factory


def register_routes(app: FastAPI) -> None:
    app.mount("/images", StaticFiles(directory="/images"), name="images")
    app.mount("/static", StaticFiles(directory="./static"), name="static")
    templates = Jinja2Templates(directory="templates")

    @app.get("/generate/{name}")
    async def index(request: Request, name: str):
        preprocessed_name = name.replace(" ", "").lower()
        new_card_generator_service = new_card_generator_service_factory()
        card_base_repository = card_base_repository_factory()

        base_card_id = card_base_repository.get_base_card_id_by_label(preprocessed_name)
        if base_card_id is not None:
            card = card_base_repository.get_card_variant(base_card_id, False, False, False)
            return templates.TemplateResponse("index.html.j2", {"request": request, "card": card})

        base_card_id = new_card_generator_service.generate_new_card(name)
        card = card_base_repository.get_card_variant(base_card_id, False, False, False)
        return templates.TemplateResponse("index.html.j2", {"request": request, "card": card})

    @app.get("/variants/{name}")
    async def variants(request: Request, name: str):
        card_base_repository = card_base_repository_factory()
        base_card_id = card_base_repository.get_base_card_id_by_label(name)

        if base_card_id is None:
            return templates.TemplateResponse("index.html.j2", {"request": request, cards: None})

        variants = card_base_repository.get_all_card_variants(base_card_id)

        return templates.TemplateResponse("all_variants.html.j2", {
            "request": request,
            "cards": variants
        })

    @app.get("/open-pack")
    async def open_pack(request: Request):

        def get_variant():
            card_base_repository = card_base_repository_factory()
            random_base_card_id = card_base_repository.get_random_base_card_id()

            is_holo = True if random.randint(0, 10) == 0 else False
            is_gold = True if random.randint(0, 10) == 0 else False
            is_negative = True if random.randint(0, 10) == 0 else False
            return card_base_repository.get_card_variant(random_base_card_id, is_holo, is_gold, is_negative)

        cards = [get_variant() for i in range(20)]

        return templates.TemplateResponse("open_pack.html.j2", {"request": request, "cards": cards})

    @app.get("/cards")
    async def cards(request: Request):
        card_base_repository = card_base_repository_factory()
        cards = card_base_repository.get_all_cards()
        return templates.TemplateResponse("all_cards.html.j2", {"request": request, "cards": cards})
