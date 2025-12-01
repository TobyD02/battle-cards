from fastapi import FastAPI
import requests

from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from fastapi import Request

from src.model.card_info_model import generate_card_prompt, CardInfoModel
from src.entity.card_model import CardModel
from src.service.card_generator_service.factory.card_generator_service_factory import card_generator_service_factory
from src.service.database_service.factory.database_service_factory import database_service_factory
from src.service.fandom_query_service.factory.fandom_query_service_factory import fandom_query_service_factory


def register_routes(app: FastAPI) -> None:
    app.mount("/images", StaticFiles(directory="/images"), name="images")
    app.mount("/static", StaticFiles(directory="./static"), name="static")
    templates = Jinja2Templates(directory="templates")

    @app.get("/generate/{name}")
    async def index(request: Request, name: str):
        preprocessed_name = name.replace(" ", "").lower()

        database_service = database_service_factory()

        print(f"attempting to find {preprocessed_name}")

        # check if exists in db
        try:
            db_results = database_service.get_card_by_label(preprocessed_name)
        except Exception:
            db_results = None
        print(f"Fetched db results {db_results}")
        if db_results:
            card_data = db_results.model_dump()
            return templates.TemplateResponse("index.html.j2", {"request": request, "card_model": card_data})


        fandom_query_service = fandom_query_service_factory()
        results = fandom_query_service.get_search_results(name)

        paragraphs = fandom_query_service.get_page_paragraphs(results[0])

        card_generator_service = card_generator_service_factory()

        print("Generating card using llm", flush=True)
        card_stats = card_generator_service.prompt(generate_card_prompt(paragraphs, name), CardInfoModel)
        print("Card finished generating", flush=True)


        # Fetch profile picture

        image_url = None
        wiki_url = results[0]
        # for i in results:
        i = results[0]
        images = fandom_query_service.get_page_image_links(i)
        if len(images) > 0:
            response = requests.get(images[0])
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Save to file
            with open("/images/" + name + ".png", "wb") as f:
                f.write(response.content)

            image_url = "/images/" + name + ".png"
        else:
            image_url = "".join(images)

        card_model = CardModel(
            label=preprocessed_name,
            name=card_stats.name,
            strength=card_stats.strength,
            dexterity=card_stats.dexterity,
            wisdom=card_stats.wisdom,
            intelligence=card_stats.intelligence,
            charisma=card_stats.charisma,
            description=card_stats.description,
            image_url=image_url,
            wiki_url=wiki_url,
        )

        card_data = card_model.model_dump()
        print(f"Got card data: {card_data}", flush=True)

        database_service.insert_card(card_model)

        print("inserted card, returning template", flush=True)

        return templates.TemplateResponse("index.html.j2", {"request": request, "card_model": card_data})


    @app.get("/cards")
    async def index3():
        database_service = database_service_factory()
        results = database_service.get_all_cards()
        return results
